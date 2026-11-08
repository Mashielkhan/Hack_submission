
# ============================================================
# flow1_memegen.py
# AI-Powered Meme Advertisement Idea Generator
# ============================================================

import os
import json
import requests

from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

from langgraph.graph import StateGraph
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.vectorstores import Chroma
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.docstore.document import Document
from langchain.llms.base import LLM


# ============================================================
# 1. ENVIRONMENT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

APIFY_DATASET_ID = os.getenv(
    "APIFY_DATASET_ID",
    "qpC2dJykxgb3cxl1Q"
)

APIFY_URL = (
    f"https://api.apify.com/v2/datasets/"
    f"{APIFY_DATASET_ID}/items"
)

MISTRAL_API_URL = (
    "https://api.mistral.ai/v1/chat/completions"
)

TRENDS_FILE = BASE_DIR / "meme_trends.json"
CHROMA_DIR = BASE_DIR / "chroma"


# ============================================================
# 2. MISTRAL LLM WRAPPER
# ============================================================

class ChatMistralAPI(LLM):

    api_key: Optional[str] = None
    api_url: Optional[str] = None

    @property
    def _llm_type(self) -> str:
        return "mistral-api"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> str:

        if not self.api_key:
            raise ValueError(
                "MISTRAL_API_KEY is missing from backend/.env"
            )

        response = requests.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-tiny",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.8
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]


# ============================================================
# 3. FETCH LIVE MEME TRENDS FROM APIFY
# ============================================================

def fetch_live_trends():

    if not APIFY_API_TOKEN:
        print(
            "Warning: APIFY_API_TOKEN not configured. "
            "Continuing without live trends."
        )
        return []

    try:
        response = requests.get(
            APIFY_URL,
            headers={
                "Authorization": f"Bearer {APIFY_API_TOKEN}"
            },
            timeout=30
        )

        response.raise_for_status()

        trends = response.json()

        if not isinstance(trends, list):
            print("Unexpected response format from Apify.")
            return []

        print(
            f"Successfully fetched {len(trends)} live trends."
        )

        return trends

    except requests.RequestException as error:

        print(
            "Live trend fetch failed:",
            error
        )

        return []

    except ValueError as error:

        print(
            "Unable to parse Apify response:",
            error
        )

        return []


# ============================================================
# 4. LOAD LOCAL AND LIVE TREND DOCUMENTS
# ============================================================

def load_trend_docs():

    base_trends = []

    if TRENDS_FILE.exists():

        try:
            with open(
                TRENDS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                base_trends = json.load(file)

            if not isinstance(base_trends, list):
                raise ValueError(
                    "meme_trends.json must contain a JSON list."
                )

        except (OSError, ValueError) as error:

            print(
                "Failed to load local meme trends:",
                error
            )

            base_trends = []

    else:

        print(
            f"Local trend file not found: {TRENDS_FILE}"
        )

    live_trends = fetch_live_trends()

    all_trends = base_trends + live_trends

    documents = []

    for trend in all_trends:

        if not isinstance(trend, dict):
            continue

        if (
            "description" not in trend
            or "title" not in trend
        ):
            continue

        description = trend["description"]
        title = trend["title"]

        if not isinstance(description, str):
            continue

        if not description.strip():
            continue

        documents.append(
            Document(
                page_content=description,
                metadata={
                    "title": str(title)
                }
            )
        )

    print(
        f"Loaded {len(documents)} meme trend documents."
    )

    return documents


# ============================================================
# 5. INITIALIZE MISTRAL EMBEDDINGS AND CHROMADB
# ============================================================

if not MISTRAL_API_KEY:
    raise ValueError(
        "MISTRAL_API_KEY is missing. "
        "Add it to backend/.env."
    )

EMBED_MODEL = MistralAIEmbeddings(
    api_key=MISTRAL_API_KEY
)

trend_documents = load_trend_docs()

if not trend_documents:
    raise ValueError(
        "No valid meme trends available. "
        "Add trends to backend/meme_trends.json "
        "or configure Apify."
    )

VECTOR_DB = Chroma.from_documents(
    documents=trend_documents,
    embedding=EMBED_MODEL,
    persist_directory=str(CHROMA_DIR)
)

retriever = VECTOR_DB.as_retriever(
    search_kwargs={
        "k": 3
    }
)


# ============================================================
# 6. AI PROMPT TEMPLATE
# ============================================================

TEMPLATE = """
You are an expert in meme marketing and creative advertising.

Your task is to generate exactly 3 creative meme advertisement
ideas based on the provided product information.

Each idea must contain:

1. idea:
   A short, memorable meme concept title.

2. audio_script:
   A funny, engaging narration suitable for a short advertisement.

3. video_prompt:
   A detailed visual description suitable for AI video generation.

Relevant meme trends:
{context}

Product Information:

Product Name:
{name}

Product Description:
{description}

Important requirements:

- Make the ideas creative and engaging.
- Ensure the concepts are relevant to the product.
- Use humor appropriately.
- Keep the ideas suitable for short-form video content.
- Return exactly 3 ideas.
- Return a valid JSON array only.
- Do not include Markdown code fences or additional commentary.

Expected JSON structure:

[
  {{
    "idea": "Meme concept title",
    "audio_script": "Funny narration",
    "video_prompt": "Detailed visual description"
  }}
]
"""

PROMPT = PromptTemplate.from_template(
    TEMPLATE
)

llm = ChatMistralAPI(
    api_key=MISTRAL_API_KEY,
    api_url=MISTRAL_API_URL
)


# ============================================================
# 7. LANGGRAPH WORKFLOW STATE
# ============================================================

class InputState(dict):
    pass


# ============================================================
# 8. MEME IDEA GENERATION NODE
# ============================================================

def meme_node(state):

    raw = ""

    try:

        product_name = state["name"]
        product_description = state["description"]

        # Retrieve relevant meme trends
        documents = retriever.invoke(
            product_description
        )

        context = "\n".join(
            document.page_content
            for document in documents
        )

        # Build the AI prompt
        prompt = PROMPT.format(
            name=product_name,
            description=product_description,
            context=context
        )

        # Generate response from Mistral
        raw = llm.invoke(prompt)

        print(
            "Mistral AI response received."
        )

        # Clean optional Markdown formatting
        cleaned_response = raw.strip()

        if cleaned_response.startswith("```"):

            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        # Parse JSON response
        ideas = json.loads(cleaned_response)

        if not isinstance(ideas, list):
            raise ValueError(
                "AI response must be a JSON list."
            )

        if len(ideas) != 3:
            raise ValueError(
                "AI must generate exactly 3 meme ideas."
            )

        required_keys = {
            "idea",
            "audio_script",
            "video_prompt"
        }

        for idea in ideas:

            if not isinstance(idea, dict):
                raise ValueError(
                    "Each meme idea must be a JSON object."
                )

            if not required_keys.issubset(idea):
                raise ValueError(
                    "A meme idea is missing required fields."
                )

        print(
            "Successfully generated 3 meme ideas."
        )

    except Exception as error:

        print(
            "Error generating meme ideas:",
            error
        )

        ideas = [
            {
                "idea": "Generation Error",
                "audio_script": (
                    "Unable to generate meme ideas. "
                    "Please try again."
                ),
                "video_prompt": "N/A"
            }
        ]

    return {
        **state,
        "ideas": ideas
    }


# ============================================================
# 9. BUILD LANGGRAPH WORKFLOW
# ============================================================

builder = StateGraph(InputState)

builder.add_node(
    "start",
    RunnableLambda(
        lambda state: state
    )
)

builder.add_node(
    "meme_node",
    RunnableLambda(meme_node)
)

builder.set_entry_point("start")

builder.add_edge(
    "start",
    "meme_node"
)

builder.set_finish_point(
    "meme_node"
)

flow = builder.compile()


# ============================================================
# 10. PUBLIC API
# ============================================================

def generate_meme_ideas(
    product_name: str,
    product_description: str,
    image_path: str
) -> List[dict]:

    if not product_name.strip():
        raise ValueError(
            "Product name cannot be empty."
        )

    if not product_description.strip():
        raise ValueError(
            "Product description cannot be empty."
        )

    result = flow.invoke(
        {
            "name": product_name,
            "description": product_description,
            "image_path": image_path
        }
    )

    if "ideas" not in result:
        raise ValueError(
            "The workflow did not return meme ideas."
        )

    ideas = result["ideas"]

    if not isinstance(ideas, list):
        raise ValueError(
            "Invalid meme ideas response."
        )

    return ideas
