# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_community.llms import Bedrock
import streamlit as st


def main():
    template = """
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's data.
        Based on uploaded file, question, write a natural language response.

        Conversation History: {chat_history}
        User question: {user_question}
        Response: {response}
        """

    prompt = ChatPromptTemplate.from_template(template)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage("Hello! I am a SQL assistant. Ask me anything about your database.")
        ]

    load_dotenv()
    st.set_page_config(page_title="Ask your CSV a question")
    st.header("Ask your CSV a question")

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV: ")

        llm = ChatOpenAI()
        #llm =  Bedrock(model_id="mistral.mixtral-8x7b-instruct-v0:1", region_name="us-west-2")
        agent = create_csv_agent(llm, user_csv, verbose=True, prompt=prompt)

        if user_question is not None and user_question != "":
            st.session_state.chat_history.append(HumanMessage(content=user_question))
            response = agent.run(user_question)
            st.session_state.chat_history.append(AIMessage(content=response))
            st.write(response)

if __name__ == "__main__":
    main()