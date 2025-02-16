
%%capture --no-stderr
%pip install --upgrade --quiet langchain-community langchainhub langgraph

# Comment out the below to opt-out of using LangSmith in this notebook. Not required.
# if not os.environ.get("LANGSMITH_API_KEY"):
#     os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
#     os.environ["LANGSMITH_TRACING"] = "true"

curl -s https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql | sqlite3 Chinook.db

