from config import client, MODEL


QUESTIONS = [
    "What is the difference between a quiz and an assignment?",
    
    "If I scored 18 out of 20, what percentage did I get?",
    
    """
    I scored the following marks in eight subjects:

    18, 17, 19, 16, 20, 15, 18, 17

    Calculate my total marks and percentage out of 160.
    """
]


def main():

    print("=" * 60)
    print("DAY 3 - PLAIN LLM (NO TOOL)")
    print("=" * 60)

    for number, question in enumerate(QUESTIONS, start=1):

        print(f"\nQUESTION {number}")
        print("-" * 60)
        print(question)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful college assistant. "
                        "Answer using only your own knowledge and "
                        "reasoning. You do not have access to tools."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        print("\nANSWER")
        print(answer)


if __name__ == "__main__":
    main()