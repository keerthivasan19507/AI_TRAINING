import json

from config import client, MODEL
from tools import get_weather


TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": (
            "Get current weather information for a supported city. "
            "Use this when the user asks about current weather."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city"
                }
            },
            "required": ["city"],
            "additionalProperties": False
        },
        "strict": True
    }
]


QUESTION = """
I am a college student in Chennai.

Answer these questions:

1. My class starts at 9:30 AM.
   Travel takes 45 minutes and I need a 15-minute buffer.
   When should I leave?

2. I have three study sessions of 50 minutes each,
   with a 10-minute break between sessions.
   What is the total duration?

3. What is the current weather in Chennai?

Use the weather tool when current weather information is needed.
Then provide a clear final answer.
"""


def main():

    print("=" * 60)
    print("REACT AGENT")
    print("=" * 60)

    # Keep conversation history manually
    conversation = [
        {
            "role": "user",
            "content": QUESTION
        }
    ]

    while True:

        response = client.responses.create(
            model=MODEL,
            input=conversation,
            tools=TOOLS
        )

        tool_called = False

        for item in response.output:

            if item.type == "function_call":

                tool_called = True

                print("\n[REACT ACTION]")
                print(f"Tool: {item.name}")
                print(f"Arguments: {item.arguments}")

                arguments = json.loads(item.arguments)

                if item.name == "get_weather":
                    result = get_weather(arguments["city"])
                else:
                    result = {"error": "Unknown tool"}

                print("[REACT OBSERVATION]")
                print(result)

                # Add assistant's tool call to history
                conversation.extend(response.output)

                # Add tool result to history
                conversation.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result)
                    }
                )

                break

        if not tool_called:
            break

    print("\n[REACT FINAL ANSWER]")
    print(response.output_text)


if __name__ == "__main__":
    main()