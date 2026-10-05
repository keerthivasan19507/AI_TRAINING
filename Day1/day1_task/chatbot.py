import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful student finance chatbot.

You do NOT have access to the user's private expense records,
budget files, bank account, or any other private data.

If the user asks about their actual expenses or budget,
clearly explain that you cannot access their private data.

You can still provide general financial guidance.
"""


def chatbot(user_message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("=" * 60)
    print("PLAIN CHATBOT")
    print("=" * 60)

    question = (
        "Analyze my expenses this month and tell me "
        "which categories are over budget."
    )

    print(f"\nUser: {question}")

    answer = chatbot(question)

    print(f"\nChatbot: {answer}")