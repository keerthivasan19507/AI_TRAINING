import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_expenses():
    with open(DATA_DIR / "expenses.json", "r") as file:
        return json.load(file)


def load_budget():
    with open(DATA_DIR / "budget.json", "r") as file:
        return json.load(file)


def calculate_category_totals(expenses):
    totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category not in totals:
            totals[category] = 0

        totals[category] += amount

    return totals


def compare_with_budget(totals, budget):
    results = {}

    for category, spent in totals.items():

        category_budget = budget.get(category, 0)

        difference = spent - category_budget

        if difference > 0:
            status = "OVER BUDGET"
        else:
            status = "WITHIN BUDGET"

        results[category] = {
            "spent": spent,
            "budget": category_budget,
            "difference": difference,
            "status": status
        }

    return results


def generate_report(results):

    lines = []

    lines.append("MONTHLY EXPENSE REPORT")
    lines.append("=" * 40)

    for category, data in results.items():

        lines.append(
            f"{category}: "
            f"Spent ₹{data['spent']} / "
            f"Budget ₹{data['budget']} "
            f"→ {data['status']}"
        )

    return "\n".join(lines)


def run_workflow():

    print("=" * 60)
    print("RULE-BASED WORKFLOW")
    print("=" * 60)

    # Step 1: Read private data
    expenses = load_expenses()
    budget = load_budget()

    # Step 2: Calculate totals
    totals = calculate_category_totals(expenses)

    # Step 3: Compare against predefined rules
    results = compare_with_budget(totals, budget)

    # Step 4: Generate report
    report = generate_report(results)

    print()
    print(report)


if __name__ == "__main__":
    run_workflow()