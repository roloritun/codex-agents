import re
from dotenv import find_dotenv, load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAI, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI



import os
import openai
import yaml
import json
import requests
from urllib.parse import urlparse


class Llm:
    def __init__(self):
        pass

    @staticmethod
    def get_llm():

        _ = load_dotenv(find_dotenv())  # read local .env file

        # openai.api_key = os.environ["OPENAI_API_KEY"]
        # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        llm = AzureChatOpenAI(
            azure_deployment="16_deploy",
            verbose=True,
        )
        #llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        return llm




def fetch_openapi_spec(spec_url):
    parsed_url = urlparse(spec_url)

    if parsed_url.scheme in ["http", "https"]:
        response = requests.get(spec_url)
        response.raise_for_status()
        temp = json.loads(response.content)
        return yaml.load(yaml.dump(temp), Loader=yaml.FullLoader)
    elif parsed_url.scheme == "file" or parsed_url.scheme == "":
        file_path = parsed_url.path
        with open(file_path, "r") as file:
            if spec_url.endswith(".yaml") or spec_url.endswith(".yml"):
               return  yaml.load(file, Loader=yaml.FullLoader)
            elif spec_url.endswith(".json"):
                return yaml.load(yaml.dump(json.load(file)), Loader=yaml.FullLoader)
    else:
        return yaml.load(spec_url, Loader=yaml.FullLoader)


