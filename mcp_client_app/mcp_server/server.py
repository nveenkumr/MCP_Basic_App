# mcp_server/server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
# import openai
import os,requests,json

from dotenv import load_dotenv
from pathlib import Path
import os

# Simulate your actual server.py location
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=dotenv_path)

from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
azure_openai_key = os.getenv("Azure_OPENAI_API_KEY")
azure_endpoint = os.getenv("Azure_OPENAI_ENDPOINT")

azure_openai_client =AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=azure_endpoint,
    api_key= azure_openai_key
)

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    functions: List[Dict[str, Any]]

def get_current_weather(location: str, unit: str = "celsius") -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    print(api_key)
    endpoint = f"http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key, 
        "q": location,
        "aqi": "no"
    }
    response = requests.get(endpoint, params=params)
    print("weather response" , response , response.text)
    if response.status_code == 200:
        data = response.json()
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        condition = data["current"]["condition"]["text"]
        temperature = temp_c if unit == "celsius" else temp_f
        return f"The current temperature in {location} is {temperature}°{unit[0].upper()} with {condition}."
    else:
        return f"Unable to retrieve weather data for {location}."


@app.post("/chat")
def chat(req: ChatRequest):
    response = azure_openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[m.model_dump() for m in req.messages],
        tools=req.functions,
        tool_choice="auto"
    )
    choice = response.choices[0].message
    if choice.tool_calls:
        for tool_call in choice.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if function_name == "get_current_weather":
                result = get_current_weather(**arguments)
                return {"content": result}
    return {"content": choice.content}