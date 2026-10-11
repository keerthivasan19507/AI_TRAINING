"""Day 8 task: college helpdesk agent with attendance tool and relevance guard."""
import ast
import operator
import os

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import EMBED_PROVIDER, get_model, get_vectorstore

COURSE_FEES = {"CS101": 12000, "AI202": 18000, "DS303": 15000}
# The task sheet suggests 0.6 for hash embeddings. Measure scores with your own
# embedding model and set MAX_DISTANCE accordingly (or set it in .env).
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "0.6"))
store = get_vectorstore()


@tool
def search_handbook(query: str) -> str:
    """Search college handbook policies and return only sufficiently relevant passages."""
    results = store.similarity_search_with_score(query, k=3)
    kept = [(doc, score) for doc, score in results if score <= MAX_DISTANCE]
    if not kept:
        return "NO_MATCH: this is not covered in the college handbook."
    return "\n\n".join(
        f"[{doc.metadata.get('source', 'unknown')}] (cosine distance={score:.3f}) {doc.page_content}"
        for doc, score in kept
    )


@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee in rupees for a course code such as CS101, AI202 or DS303."""
    normalized = course_code.strip().upper()
    fee = COURSE_FEES.get(normalized)
    return f"{normalized} fee is Rs. {fee}" if fee is not None else f"Unknown course code {course_code}"


@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check if a student with this attendance percentage (0-100) may write the end-semester exam."""
    if not 0 <= attendance_percent <= 100:
        return "ERROR: attendance percentage must be between 0 and 100."
    if attendance_percent >= 75:
        return "ELIGIBLE: attendance is 75% or above; you may write the end-semester exam."
    if attendance_percent >= 65:
        return "CONDONATION: attendance is 65% to below 75%; condonation is required at Rs. 500 per course."
    return "NOT ELIGIBLE: attendance below 65%; you may not write the end-semester exam."


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


@tool
def calculator(expression: str) -> str:
    """Evaluate simple arithmetic such as '12000 + 18000 + 500'."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.left), ev(node.right))
        raise ValueError("only + - * / on numbers are allowed")
    try:
        return str(ev(ast.parse(expression, mode="eval").body))
    except Exception as exc:
        return f"Error: {exc}"


tools = [search_handbook, get_course_fee, check_exam_eligibility, calculator]
model = get_model().bind_tools(tools)
SYSTEM = (
    "You are the Greenfield College helpdesk. Use search_handbook for handbook rules/policies; "
    "get_course_fee for course fees; check_exam_eligibility for exam attendance percentages; "
    "and calculator for arithmetic. If search_handbook returns a result beginning with NO_MATCH, "
    "say exactly that you don't know because the question is not covered in the college handbook. "
    "Do not guess or use outside knowledge. Answer briefly and name source files when available. "
    "Use the conversation history to resolve follow-up questions."
)


def agent(state: MessagesState):
    reply = model.invoke([("system", SYSTEM)] + state["messages"])
    return {"messages": [reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
graph = builder.compile(checkpointer=InMemorySaver())


def ask(question, thread_id="task-run"):
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 12}
    print(f"\n[{thread_id}] USER: {question}")
    for step in graph.stream({"messages": [("user", question)]}, config, stream_mode="updates"):
        for node, update in step.items():
            for msg in update.get("messages", []):
                if getattr(msg, "tool_calls", None):
                    for call in msg.tool_calls:
                        print(f"   {node:6} -> call {call['name']}({call['args']})")
                elif node == "tools":
                    print(f"   {node:6} -> {msg.name} returned {str(msg.content)[:160]!r}")
                else:
                    print(f"   {node:6} -> ANSWER: {msg.content}")


if __name__ == "__main__":
    print(f"Model provider configured in .env; embedding provider: {EMBED_PROVIDER}; MAX_DISTANCE={MAX_DISTANCE}")
    print("Direct eligibility tool checks:")
    for value in (82, 70, 50, 120):
        print(f"attendance={value}: {check_exam_eligibility.invoke({'attendance_percent': value})}")

    # Required five questions, all in the same thread so Q4 can use Q3 context.
    ask("What CGPA do I need to be eligible for placements?", "task-run")
    ask("My attendance is 70%. Can I write the exam?", "task-run")
    ask("What is the total of the CS101 fee, the AI202 fee and the maximum late fee?", "task-run")
    ask("And if I pay only 5 days late instead?", "task-run")
    ask("What is the capital of France?", "task-run")
