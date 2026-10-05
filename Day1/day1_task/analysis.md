# Agentic AI: Foundations and Open-Source Practice

## 1. Scenario

The project compares a **Plain Chatbot, Rule-Based Workflow, and AI Agent** using a student expense and budget analysis scenario. Private expense and budget data are stored locally in JSON files.

## 2. Plain Chatbot

A plain chatbot mainly uses an LLM to generate responses from the information provided in the conversation.

**Limitation:** It cannot automatically access the student's private JSON data unless the data is provided to it.

## 3. Rule-Based Workflow

The workflow uses predefined Python steps:

```text
Read Data → Calculate Totals → Compare Budget → Display Result
```

It does not use an LLM. It is predictable and reliable for fixed tasks but has limited flexibility.

## 4. AI Agent

The AI agent combines:

```text
LLM + Tools + Loop
```

It understands the request, selects tools, executes them, observes the results, and decides whether another tool is needed.

## 5. Tools Used

The agent has four tools:

* `get_expenses()` – retrieves private expenses.
* `get_budgets()` – retrieves budgets.
* `calculate_category_totals()` – calculates category spending.
* `compare_budgets()` – compares spending with budgets.

## 6. Comparison

| Feature          | Chatbot      | Workflow      | AI Agent          |
| ---------------- | ------------ | ------------- | ----------------- |
| Flexibility      | Medium       | Low           | High              |
| Decision-making  | LLM response | Fixed rules   | LLM + tools       |
| Tool usage       | No           | Predefined    | Dynamic           |
| Private data     | Manual input | Direct access | Tool-based access |
| Multi-step tasks | Limited      | Fixed         | Adaptive          |

## 7. Test Result

For the sample data:

| Category      |  Spent | Budget | Status         |
| ------------- | -----: | -----: | -------------- |
| Food          | ₹1,050 | ₹1,000 | ₹50 over       |
| Transport     |   ₹230 |   ₹500 | ₹270 remaining |
| Entertainment |   ₹850 |   ₹600 | ₹250 over      |
| Education     |   ₹600 | ₹1,000 | ₹400 remaining |

## 8. Suitability

The **chatbot** is useful for simple conversations. The **rule-based workflow** is useful for predictable and repetitive tasks. The **AI agent** is useful for multi-step tasks where the system needs to select tools and adapt based on results.

## 9. Conclusion

This project demonstrates the difference between simple text generation, fixed automation, and agentic AI.

The key concept is:

```text
AI Agent = LLM + Tools + Loop
```

The AI agent can access private data through controlled tools, perform multiple steps, observe results, and produce a final answer.
