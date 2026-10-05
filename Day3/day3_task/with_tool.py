import json

from config import client, MODEL
from tool import calculate_marks


MARKS_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_marks",
        "description": (
            "Calculate the total marks and percentage for a list "
            "of subject marks. Each subject has a maximum of 20 marks."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "marks": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "description": (
                        "List of marks obtained in each subject."
                    )
                }
            },
            "required": ["marks"]
        }
    }
}


QUESTION = """
I scored the following marks in eight subjects:

18, 17, 19, 16, 20, 15, 18, 17

Calculate my total marks and percentage.

Use the calculate_marks tool to perform the calculation.
"""


def main():

    print("=" * 60)
    print("DAY 3 - LLM WITH ONE TOOL")
    print("=" * 60)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a college marks assistant. "
                "Use the calculate_marks tool when marks "
                "need to be calculated."
            )
        },
        {
            "role": "user",
            "content": QUESTION
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[MARKS_TOOL],
        tool_choice="auto",
        temperature=0
    )

    assistant_message = response.choices[0].message

    print("\nQUESTION")
    print(QUESTION)

    if assistant_message.tool_calls:

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name
            arguments = json.loads(
                tool_call.function.arguments
            )

            print("\nTOOL CALL")
            print("Function:", function_name)
            print("Arguments:", arguments)

            if function_name == "calculate_marks":

                tool_result = calculate_marks(
                    arguments["marks"]
                )

            else:

                tool_result = "Unknown tool"

            print("\nTOOL RESULT")
            print(tool_result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0
        )

        final_answer = (
            final_response.choices[0]
            .message
            .content
        )

        print("\nFINAL ANSWER")
        print(final_answer)

    else:

        print("\nNo tool was called.")

        print("\nFINAL ANSWER")
        print(assistant_message.content)


if __name__ == "__main__":
    main()