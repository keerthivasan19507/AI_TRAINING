import os
import json

from dotenv import load_dotenv
from groq import Groq

from tools import (
    get_expenses,
    get_budgets,
    calculate_category_totals,
    compare_budgets
)


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# TOOLS AVAILABLE TO THE AI AGENT
# ============================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_expenses",
            "description": (
                "Get the user's private expense records "
                "from the local expense database."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_budgets",
            "description": (
                "Get the user's private monthly budget "
                "for each spending category."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_category_totals",
            "description": (
                "Calculate the total amount spent "
                "in each expense category."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expenses": {
                        "type": "array",
                        "description": (
                            "List of private expense records."
                        )
                    }
                },
                "required": ["expenses"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "compare_budgets",
            "description": (
                "Compare category spending against "
                "the corresponding category budgets."
            ),
            "parameters": {
                "type": "object",
                "properties": {

                    "totals": {
                        "type": "object",
                        "description": (
                            "Total spending for each category."
                        )
                    },

                    "budget": {
                        "type": "object",
                        "description": (
                            "Budget amount for each category."
                        )
                    }
                },
                "required": [
                    "totals",
                    "budget"
                ]
            }
        }
    }
]


# ============================================================
# EXECUTE A TOOL
# ============================================================

def execute_tool(tool_name, arguments):

    if tool_name == "get_expenses":

        return get_expenses()

    elif tool_name == "get_budgets":

        return get_budgets()

    elif tool_name == "calculate_category_totals":

        expenses = arguments["expenses"]

        return calculate_category_totals(
            expenses
        )

    elif tool_name == "compare_budgets":

        totals = arguments["totals"]
        budget = arguments["budget"]

        return compare_budgets(
            totals,
            budget
        )

    else:

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )


# ============================================================
# DISPLAY TOOL OBSERVATION
# ============================================================

def display_observation(tool_name, result):

    print()
    print("   OBSERVATION")
    print("   " + "-" * 50)

    # -----------------------------------------
    # Expense tool
    # -----------------------------------------

    if tool_name == "get_expenses":

        print(
            f"   ✓ Retrieved {len(result)} "
            f"private expense records."
        )

    # -----------------------------------------
    # Budget tool
    # -----------------------------------------

    elif tool_name == "get_budgets":

        print(
            f"   ✓ Retrieved {len(result)} "
            f"category budgets."
        )

    # -----------------------------------------
    # Calculation tool
    # -----------------------------------------

    elif tool_name == "calculate_category_totals":

        print(
            "   ✓ Category spending totals calculated:"
        )

        for category, amount in result.items():

            print(
                f"      • {category:<15} ₹{amount}"
            )

    # -----------------------------------------
    # Budget comparison tool
    # -----------------------------------------

    elif tool_name == "compare_budgets":

        print(
            "   ✓ Budget comparison completed:"
        )

        for category, data in result.items():

            if data["status"] == "OVER BUDGET":

                print(
                    f"      • {category:<15} "
                    f"OVER by ₹{data['difference']}"
                )

            else:

                print(
                    f"      • {category:<15} "
                    f"₹{abs(data['difference'])} remaining"
                )


# ============================================================
# DISPLAY FINAL ANSWER
# ============================================================

def display_final_answer(answer):

    print()
    print("=" * 65)
    print("                       FINAL ANSWER")
    print("=" * 65)

    print(answer)

    print("=" * 65)


# ============================================================
# AI AGENT LOOP
# ============================================================

def run_agent(user_question):

    messages = [

        {
            "role": "system",

            "content": """
You are an AI agent for analyzing a student's
private expense and budget information.

The private data can ONLY be accessed through
the provided tools.

Your job is to:

1. Understand the user's request.
2. Decide which tool is required.
3. Call the appropriate tool.
4. Observe the tool result.
5. Decide whether another tool is needed.
6. Continue the loop until enough information is available.
7. Provide a structured final answer.

Do not invent or assume private financial information.

For the final answer:

- Use clear headings.
- Show spending for every category.
- Show the budget for every category.
- Identify categories that are over budget.
- Show the exact amount over budget.
- Identify categories within budget.
- Show the remaining amount.
- Keep the answer concise and easy to read.
"""
        },

        {
            "role": "user",
            "content": user_question
        }

    ]

    step = 1

    # ========================================================
    # AGENT LOOP
    # ========================================================

    while True:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=messages,

            tools=TOOLS,

            tool_choice="auto",

            temperature=0.1
        )

        assistant_message = response.choices[0].message

        # ----------------------------------------------------
        # If the LLM does not request another tool,
        # the agent has enough information.
        # ----------------------------------------------------

        if not assistant_message.tool_calls:

            display_final_answer(
                assistant_message.content
            )

            return


        # ----------------------------------------------------
        # Store the assistant's tool request
        # ----------------------------------------------------

        messages.append(
            assistant_message
        )


        # ----------------------------------------------------
        # Execute selected tools
        # ----------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
                or "{}"
            )


            # ------------------------------------------------
            # STEP INFORMATION
            # ------------------------------------------------

            print()
            print(f"[STEP {step}]")

            print(
                f"   TOOL SELECTED : {tool_name}"
            )

            print(
                "   ACTION        : Executing tool..."
            )


            # ------------------------------------------------
            # EXECUTE TOOL
            # ------------------------------------------------

            result = execute_tool(
                tool_name,
                arguments
            )


            # ------------------------------------------------
            # DISPLAY OBSERVATION
            # ------------------------------------------------

            display_observation(
                tool_name,
                result
            )


            # ------------------------------------------------
            # SEND RESULT BACK TO LLM
            # ------------------------------------------------

            messages.append(
                {
                    "role": "tool",

                    "tool_call_id":
                        tool_call.id,

                    "content":
                        json.dumps(result)
                }
            )


            step += 1


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 65)

    print(
        "              AI AGENT - EXPENSE ANALYZER"
    )

    print("=" * 65)


    print()
    print("PRIVATE-DATA SCENARIO")
    print("-" * 65)

    print(
        "Student expense and monthly budget analysis"
    )


    print()
    print("USER REQUEST")
    print("-" * 65)

    print(
        "Analyze my spending this month and compare "
        "it with my budget."
    )


    print()
    print("AGENT EXECUTION")
    print("-" * 65)


    question = """
Analyze my spending this month.

Tell me:

1. How much I spent in each category.
2. Which categories are over budget.
3. How much I exceeded each budget by.
4. Which categories are still within budget.
"""


    run_agent(question)