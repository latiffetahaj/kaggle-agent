# Step 1: Define tools and model
import os
import json
from langchain.tools import tool
from langsmith import traceable
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_community import GoogleSearchAPIWrapper
from kaggle.api.kaggle_api_extended import KaggleApi
from langchain.messages import (
    HumanMessage,
)
from dotenv import load_dotenv
from tools.get_kaggle_dataset import fetch_kaggle_dataset
from tools.search_web import web_search
from tools.execute_code_locally import execute_python_code_locally
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")




agent = create_agent(model=model, tools=[web_search, fetch_kaggle_dataset, execute_python_code_locally])

user_input = {
    "task": "Extract the data from the Kaggle dataset and generate appropriate 1-3 graphs that will help to predict the prices. Save the running python code and save graphs in a /graphs directory. Generate a summary text file explaining your graph choices and findings.",
    "dataset_link": "https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset"
}

message = HumanMessage(content=str(user_input))

MAX_ATTEMPTS = 3
for attempt in range(MAX_ATTEMPTS):
    try:
        result = agent.invoke(
            {"messages": [message]},
            config={"tags": ["debug", "local"], "metadata": {"run_purpose": "demo"}}
        )
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt == MAX_ATTEMPTS - 1:
            raise

print(result)
