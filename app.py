import streamlit as st

from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


### Streamlit App

st.set_page_config(page_title="Langchain:- Chat with SQL DB", page_icon="🦜", layout="wide")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCAL_DB"
MYSQL = "USE_MYSQL_DB"

radio_opts = ["Use SQLite3 Database (student.db)", "Connect to MySQL Database"]

selected_opt = st.sidebar.radio(label="Choose the Database to which you want to chat", options=radio_opts, index=0)

if radio_opts.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL database")
else:
    db_uri = LOCALDB


api_key = st.sidebar.text_input("Enter Your GROQ API Key :-", type="password")

if not api_key:
    st.info("Please provide your GROQ API Key to continue.")


## LLM Model
if api_key:
    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name="llama3-8b-8192",
        streaming=True
    )
else:
    st.stop()


@st.cache_resource(ttl="2 hours")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        db_file_path = (Path(__file__).parent/"student.db").absolute()
        print(db_file_path)
        creator = lambda: sqlite3.connect(f"file:{db_file_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine(f"sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
            st.warning("Please provide all MySQL connection details!")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

    
if db_uri == LOCALDB:
    db = configure_db(db_uri)
elif db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)


## Agent Toolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)


if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])


user_query = st.chat_input(placeholder="Ask anything from the database...")

if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.write(response)

