# Example tool: simple calculator
def calculate():
    pass

add_numbers = {
    "name": "add_numbers",
    "description": "Add two numbers together.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
}
weather_tool_schema = {
    "name": "get_current_weather",
    "description": "Retrieve current weather information for a specified location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name, e.g., 'Mumbai'"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit"
            }
        },
        "required": ["location"]
    }
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": weather_tool_schema
    }
]