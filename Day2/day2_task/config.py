import os
from openai import OpenAI

MODEL = "openai/gpt-oss-20b"

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)