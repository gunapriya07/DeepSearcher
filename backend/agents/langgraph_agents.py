"""
Multi-Agent System using LangGraph.

Agents:
  - summarizer_agent   → concise notes
  - quiz_agent         → MCQ generation
  - explainer_agent    → explains hard concepts
  - research_agent     → cross-document connections
  - citation_agent     → source references
  - qa_agent           → RAG question answering
"""

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

# ---------- Shared LLM ----------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.google_api_key,
    temperature=0.3,
)


# ---------- Agent State ----------

class AgentState(TypedDict):
    task: str                     # "qa" | "summarize" | "quiz" | "topics" | "compare"
    context_chunks: List[str]
    question: Optional[str]
    style: Optional[str]
    num_questions: Optional[int]
    result: Optional[str]
    citations: Optional[List[str]]
    quiz_questions: Optional[List[dict]]


# ---------- Individual Agents ----------

def qa_agent(state: AgentState) -> AgentState:
    context = "\n\n---\n\n".join(state["context_chunks"])
    prompt = f"""You are a precise question-answering assistant.
Answer ONLY using the provided context. If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question: {state["question"]}

Provide a clear, accurate answer with references to specific parts of the context."""

    response = llm.invoke(prompt)
    state["result"] = response.content
    state["citations"] = state["context_chunks"][:3]   # top 3 chunks as citations
    return state


def summarizer_agent(state: AgentState) -> AgentState:
    context = "\n\n".join(state["context_chunks"])
    style = state.get("style", "concise")

    style_instructions = {
        "concise": "Write a concise summary in 3-5 sentences.",
        "detailed": "Write a detailed summary covering all key points.",
        "bullet": "Summarise using clear bullet points grouped by topic.",
    }
    instruction = style_instructions.get(style, style_instructions["concise"])

    prompt = f"""You are an expert summariser.
{instruction}

Document content:
{context}"""

    response = llm.invoke(prompt)
    state["result"] = response.content
    return state


def quiz_agent(state: AgentState) -> AgentState:
    context = "\n\n".join(state["context_chunks"])
    n = state.get("num_questions", 5)

    prompt = f"""You are a quiz generator. Create exactly {n} multiple-choice questions based ONLY on the document below.

Format your response as valid JSON (no markdown fences) with this exact structure:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A) ..."
  }}
]

Document:
{context}"""

    response = llm.invoke(prompt)
    import json, re
    raw = response.content.strip()
    # Strip markdown fences if present
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        questions = json.loads(raw)
    except Exception:
        questions = []
    state["quiz_questions"] = questions
    state["result"] = "quiz_generated"
    return state


def explainer_agent(state: AgentState) -> AgentState:
    context = "\n\n".join(state["context_chunks"])

    prompt = f"""You are an expert teacher. Identify the most difficult or technical concept in the text below and explain it clearly as if the reader is a first-year college student. Use analogies where helpful.

Document:
{context}"""

    response = llm.invoke(prompt)
    state["result"] = response.content
    return state


def research_agent(state: AgentState) -> AgentState:
    context = "\n\n".join(state["context_chunks"])

    prompt = f"""You are a research analyst. Identify key themes, connections, and insights from the following text. Highlight anything that connects to broader academic or industry trends.

Document:
{context}"""

    response = llm.invoke(prompt)
    state["result"] = response.content
    return state


def citation_agent(state: AgentState) -> AgentState:
    """Wraps QA output with formatted source citations."""
    chunks = state.get("citations") or state["context_chunks"][:3]
    formatted = []
    for i, chunk in enumerate(chunks, 1):
        preview = chunk[:200].replace("\n", " ").strip()
        formatted.append(f"[{i}] ...{preview}...")
    state["citations"] = formatted
    return state


def topics_agent(state: AgentState) -> AgentState:
    context = "\n\n".join(state["context_chunks"])

    prompt = f"""Extract the 8-12 most important topics/concepts from the document below.
Return only a JSON array of short topic strings (no markdown, no preamble):
["topic1", "topic2", ...]

Document:
{context}"""

    response = llm.invoke(prompt)
    import json, re
    raw = re.sub(r"```json|```", "", response.content).strip()
    try:
        topics = json.loads(raw)
    except Exception:
        topics = [line.strip("- ").strip() for line in raw.split("\n") if line.strip()]
    state["result"] = json.dumps(topics)
    return state


def compare_agent(state: AgentState) -> AgentState:
    context = "\n\n---\n\n".join(state["context_chunks"])
    aspect = state.get("style", "general")

    prompt = f"""You are a document comparison expert.
Compare the following document excerpts focusing on: {aspect}.
Highlight similarities, differences, and unique insights from each document.

Documents:
{context}"""

    response = llm.invoke(prompt)
    state["result"] = response.content
    return state


# ---------- Router ----------

def route(state: AgentState) -> str:
    task_map = {
        "qa": "qa_agent",
        "summarize": "summarizer_agent",
        "quiz": "quiz_agent",
        "explain": "explainer_agent",
        "research": "research_agent",
        "topics": "topics_agent",
        "compare": "compare_agent",
    }
    return task_map.get(state["task"], "qa_agent")


# ---------- Build Graph ----------

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("qa_agent", qa_agent)
    g.add_node("summarizer_agent", summarizer_agent)
    g.add_node("quiz_agent", quiz_agent)
    g.add_node("explainer_agent", explainer_agent)
    g.add_node("research_agent", research_agent)
    g.add_node("citation_agent", citation_agent)
    g.add_node("topics_agent", topics_agent)
    g.add_node("compare_agent", compare_agent)

    # All QA paths through citation enrichment
    g.add_conditional_edges("__start__", route)
    g.add_edge("qa_agent", "citation_agent")
    g.add_edge("citation_agent", END)

    # All other agents go straight to END
    for node in ["summarizer_agent", "quiz_agent", "explainer_agent",
                 "research_agent", "topics_agent", "compare_agent"]:
        g.add_edge(node, END)

    return g.compile()


graph = build_graph()


# ---------- Public runner ----------

def run_agent(task: str, context_chunks: list, **kwargs) -> AgentState:
    initial_state: AgentState = {
        "task": task,
        "context_chunks": context_chunks,
        "question": kwargs.get("question"),
        "style": kwargs.get("style", "concise"),
        "num_questions": kwargs.get("num_questions", 5),
        "result": None,
        "citations": None,
        "quiz_questions": None,
    }
    return graph.invoke(initial_state)