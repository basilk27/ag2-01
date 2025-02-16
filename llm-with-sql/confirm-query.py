from typing_extensions import TypedDict

## NOTE: you need to set the OPENAI_API_KEY environment variable
## Also NOTE: I am not using LangSmith here, just OpenAI's API
##      So we will see LangSmith errors

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

import getpass
import os

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

from langchain import hub

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

## get the sql prompt for the llm
assert len(query_prompt_template.messages) == 1
# query_prompt_template.messages[0].pretty_print()

from typing_extensions import Annotated

class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

from langchain_community.utilities import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

# result =execute_query({"query": "SELECT COUNT(EmployeeId) AS EmployeeCount FROM Employee;"})
# print(f"actualSQL: {result['result']}")

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

from langgraph.graph import START, StateGraph

graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()

from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

# Add thread_id configuration for the checkpointer
graph = graph_builder.compile(
    checkpointer=memory, 
    interrupt_before=["execute_query"]
)

answer = None
config = {"configurable": {"thread_id": "sql_query_thread"}}
query = "What are the employees first names, sorted alphabetically?"
print("Query:", query)
for step in graph.stream(
    {"question": query}, 
    config=config,  # Add thread_id in the stream config
    stream_mode="updates"
):
    answer = step

try:
    user_approval = input("Do you want to go to execute query? (yes/no): ")
except Exception:
    user_approval = "no"

if user_approval.lower() == "yes":
    # If approved, continue the graph execution
    for step in graph.stream(None, config, stream_mode="updates"):
        answer = step
else:
    print("Operation cancelled by user.")

# print("Answer:", answer)
print("Answer:", answer["generate_answer"]["answer"])

