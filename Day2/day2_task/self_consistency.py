from config import client, MODEL


QUESTION = """
A college class starts at 9:30 AM.
The student's travel time is 45 minutes.
The student also wants a 15-minute safety buffer.

What time should the student leave?

Calculate carefully and give the final time.
"""


def ask_model(temperature):
    response = client.responses.create(
        model=MODEL,
        input=QUESTION,
        temperature=temperature
    )

    return response.output_text


def main():
    print("=" * 60)
    print("SELF-CONSISTENCY EXPERIMENT")
    print("=" * 60)

    print("\nTemperature = 0.8")
    print("-" * 60)

    for i in range(1, 6):
        answer = ask_model(0.8)
        print(f"\nRun {i}:")
        print(answer)

    print("\n" + "=" * 60)
    print("Temperature = 0")
    print("=" * 60)

    for i in range(1, 4):
        answer = ask_model(0)
        print(f"\nRun {i}:")
        print(answer)


if __name__ == "__main__":
    main()