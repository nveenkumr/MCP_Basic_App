# mcp_client/client.py
import os
import requests
from dotenv import load_dotenv
from functions_schema import TOOL_SCHEMAS

load_dotenv()
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

class MCPClient:
    def __init__(self):
        self.messages = []

    def send(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        payload = {"messages": self.messages, "functions": TOOL_SCHEMAS}
        resp = requests.post(f"{MCP_SERVER_URL}/chat", json=payload)
        print("resp is ", resp , resp.text)
        data = resp.json()
        # Append assistant response or handle function_call
        if data.get("content"):
            self.messages.append({"role": "assistant", "content": data["content"]})
            return data["content"]
        elif data.get("function_call"):
            # In a full app, you'd route this. Here we just print.
            return f"Function call requested: {data['function_call']}"
        return ""

if __name__ == "__main__":
    client = MCPClient()
    while True:
        msg = input("You: ")
        if msg.lower() in ("exit", "quit"): break
        print("Bot:", client.send(msg))