from config import client, MODEL

QUESTION = """
Solve the following questions carefully.

1. My class starts at 9:30 AM.
   Travel takes 45 minutes.
   I need a 15-minute safety buffer.
   What time should I leave?

2. I have three study sessions.
   Each session is 50 minutes.
   There is a 10-minute break between sessions.
   What is the total duration?

3. What is the current weather in Chennai?

Think through the calculations carefully before answering.
Do not use external tools or browsing.

Give only the final answers with short explanations.
For question 3, clearly state that current weather information
cannot be confirmed without access to current weather data.
"""


def main():
    response = client.responses.create(
        model=MODEL,
        input=QUESTION
    )

    print("=" * 60)
    print("CHAIN-OF-THOUGHT PROMPTING")
    print("=" * 60)
    print(response.output_text)


if __name__ == "__main__":
    main()