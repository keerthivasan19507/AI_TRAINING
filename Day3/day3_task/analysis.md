# Day 3 – From Prompt to Action: LLMs, Tools and Agents

## 1. Scenario

For this experiment, I selected a college marks scenario.

The scenario contains simple questions that a Large Language Model can
reason about by itself and a numerical calculation that can be
performed using an external tool.

The purpose of the experiment is to compare a plain LLM prompt with
the same LLM when it is given access to one tool.

The tool used in this project is called `calculate_marks`. It receives
a list of marks, calculates the total and percentage, and returns the
result to the language model.

---

## 2. What is a Large Language Model?

A Large Language Model, or LLM, is an AI model trained on a very large
amount of text so that it can understand and generate natural
language.

In this experiment, the LLM can answer general questions such as the
difference between a quiz and an assignment using its learned
knowledge.

It can also perform simple reasoning. For example, if a student scores
18 out of 20, the LLM can calculate that the percentage is 90 percent.

However, an LLM by itself does not automatically have access to new
external information or to arbitrary programs on the user's computer.
Its answer is generated from the information available to it through
the model's knowledge and the current prompt.

This becomes important when a task requires a reliable external
operation or information that the model should not be expected to know
from memory.

---

## 3. What is an Agent?

An agent is an LLM-based system that can use additional capabilities,
such as tools, to complete a task.

A plain chat response mainly follows this pattern:

User question -> LLM -> answer

An agent can follow a larger process:

User question -> LLM -> decide whether a tool is needed -> tool call
-> tool result -> LLM -> final answer

In this project, the tool-enabled program behaves like a small agent
because the language model is given access to a function and can
request that function when it is useful for answering the question.

The important difference is that the plain LLM only generates the
answer, while the tool-enabled system can interact with an external
function before producing its final response.

---

## 4. What is a Tool?

A tool is an external function or capability that an LLM can request
when it needs information or an operation that should be performed
outside the language model itself.

In this project, the tool is:

`calculate_marks`

It accepts a list of marks and calculates the total and percentage.

For example, the input can be:

`[18, 17, 19, 16, 20, 15, 18, 17]`

The tool returns:

`Total marks: 140/160`

and:

`Percentage: 87.50%`

The tool is implemented as normal Python code.

---

## 5. What is a Tool Call?

A tool call is a structured request from the language model asking the
application to execute a particular tool with particular arguments.

In this experiment, the model can request:

`calculate_marks`

with arguments similar to:

`{"marks": [18, 17, 19, 16, 20, 15, 18, 17]}`

The Python application receives this request, executes the
`calculate_marks` function, and sends the result back to the model.

The model then uses that result to produce the final answer.

---

## 6. Why Does the Tool Need a Schema?

The language model needs a description of the tool before it can
decide whether to use it correctly.

The tool schema contains three important parts.

First, the name identifies the function. In this project the name is
`calculate_marks`.

Second, the description explains what the function does. The
description tells the model that the function calculates total marks
and percentage.

Third, the parameters describe what information the function expects.
The tool in this project expects a list of marks.

Without the schema, the model would not have a reliable structured
description of which function exists, when it should be used, or what
arguments it should provide.

---

## 7. Step-by-Step Tool Call Flow

The tool-enabled experiment follows these steps.

First, the user asks the model to calculate the total and percentage
for a list of marks.

Second, the model receives the question together with the definition
of the `calculate_marks` tool.

Third, the model determines that the calculation tool can be used for
the requested calculation.

Fourth, the model produces a structured tool call containing the tool
name and the marks as arguments.

Fifth, the Python application receives the tool call and executes the
`calculate_marks` function.

Sixth, the function calculates the total marks and percentage.

For the marks used in this experiment:

18 + 17 + 19 + 16 + 20 + 15 + 18 + 17 = 140

There are eight subjects and each has a maximum of 20 marks, so the
maximum is 160.

Therefore:

140 / 160 x 100 = 87.50 percent.

Seventh, the application sends the tool result back to the language
model.

Finally, the language model uses the tool result to produce the final
answer for the user.

The complete flow is:

User question
-> LLM
-> tool decision
-> tool call
-> Python function
-> tool result
-> LLM
-> final answer

---

## 8. Why Should a Tool Return Text Even When It Fails?

A tool should preferably return its result as a value that can be
passed back to the model, including a readable error message when
something goes wrong.

For example, instead of crashing the entire program, a tool can return:

`Tool error: invalid marks`

The model can then see the failure and respond appropriately.

If the function instead raises an unhandled error and stops the
program, the model may never receive the result and the conversation
can terminate unexpectedly.

Returning an error as text keeps the tool failure inside the
agent's communication flow and gives the model an opportunity to
explain the problem or ask for corrected information.

---

## 9. Comparison Table

| Basis for comparison | Plain LLM prompt (no tool) | LLM with one tool |
|---|---|---|
| Source of the answer | Model's learned knowledge and its reasoning from the prompt | Model's knowledge plus the result returned by the external tool |
| Can it fetch or compute information outside its own memory? | No external function is available | Yes, it can request the provided calculation function |
| Reliability on factual or numeric questions | Suitable for simple questions and calculations, but the model itself performs the reasoning | More reliable for the specific calculation because the Python function performs it |
| Transparency | The final answer is visible, but there is no external operation to inspect | The tool call, arguments and tool result can be displayed before the final answer |
| Speed / cost of getting an answer | Usually simpler and faster because there is only one model request | Requires a tool call and another model step, so it can take more processing and time |

---

## 10. Observation

I tested three questions using the college marks scenario.

### Question 1

The first question asked:

"What is the difference between a quiz and an assignment?"

The plain LLM could answer this without any tool. The tool-enabled
system also did not need the marks calculation tool because the
question was conceptual.

This shows that not every question requires a tool.

### Question 2

The second question asked:

"If I scored 18 out of 20, what percentage did I get?"

The plain LLM could calculate the answer as 90 percent.

This question also does not genuinely require the external tool
because it is a small calculation that the model can reasonably
perform itself.

This demonstrates that adding a tool does not mean the tool has to be
used for every possible question.

### Question 3

The third question used eight subject marks:

18, 17, 19, 16, 20, 15, 18, 17.

The required calculation was the total and percentage out of 160.

The plain LLM produced an answer using its own reasoning.

In the tool-enabled version, the model produced a tool call to
`calculate_marks`. The Python function received the marks and returned:

`Total marks: 140/160`

and:

`Percentage: 87.50%`

The final model response then used the tool result.

Therefore, the third question demonstrates the main difference between
the two approaches: the tool-enabled system can delegate a specific
operation to an external function and then use the result in its final
answer.

---

## 11. Suitability Analysis

The plain LLM was sufficient for the conceptual question about quizzes
and assignments and for the simple 18-out-of-20 percentage
calculation.

For those questions, introducing a tool would add complexity without
providing much benefit.

The single calculation tool became useful when the task involved a
larger marks calculation that could be delegated to a deterministic
Python function.

The main advantage of the tool-enabled approach is that the
calculation is performed by the Python function rather than relying
only on generated text.

The tool also makes the process observable because the program can
print the function name, arguments and returned result.

However, the tool-enabled approach has additional complexity because
the application must define the tool, execute the requested function
and send the result back to the model.

---

## 12. Conclusion

A plain LLM prompt is appropriate when the question is based on
general knowledge, explanation, writing or simple reasoning that the
model can reasonably perform from the information already available.

A tool becomes useful when the problem requires an external operation,
current information, a database lookup, a file operation, or a
calculation where using a deterministic program can improve
reliability.

The main difference demonstrated by this experiment is that the
plain LLM generates an answer directly, while the tool-enabled system
can recognise that an external operation is useful, request a tool
call, receive the result and then use that result to construct the
final answer.

Therefore, tools extend an LLM beyond text generation. They allow the
LLM to interact with functions and external resources while still
using the language model to understand the user's request and explain
the final result.