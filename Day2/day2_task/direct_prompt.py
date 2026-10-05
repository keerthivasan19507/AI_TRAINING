import os
from openai import OpenAI

MODEL = "openai/gpt-oss-20b"
QUESTION = "What is artificial intelligence?"

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def main():
    response = client.responses.create(
        model=MODEL,
        input=QUESTION
    )

    print(response.output_text)

if __name__ == "__main__":
    main()