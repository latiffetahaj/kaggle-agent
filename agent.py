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
import logging_config
from tools.get_kaggle_dataset import fetch_kaggle_dataset
from tools.search_web import web_search

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")




agent = create_agent(model=model, tools=[web_search, fetch_kaggle_dataset])

user_input = {
    "task": "Extract the data from the Kaggle dataset and save it to a CSV file.",
    "dataset_link": "https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset"
}

message = HumanMessage(content=str(user_input))


result = agent.invoke(
    {"messages": [message]},
    config={"tags": ["debug", "local"], "metadata": {"run_purpose": "demo"}}
)

print(result)
