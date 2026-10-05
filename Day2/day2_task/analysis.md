# Day 2 – Reasoning and Acting: Direct Prompting, Chain-of-Thought and ReAct

## 1. Scenario

For this experiment, I selected a college day planning scenario. The
scenario contains both reasoning-based questions and a question that
requires current external information.

The reasoning questions involve calculating a suitable departure time
and calculating the duration of a study block. The external-information
question asks for the current weather in Chennai.

The same scenario was tested using direct prompting, Chain-of-Thought
prompting and a ReAct agent.

---

## 2. Direct Prompting

Direct prompting sends the user's question directly to the language
model and asks it to provide an answer. There is no external tool in
this approach.

In this experiment, the model could solve the departure-time problem
because it only required arithmetic. The class starts at 9:30 AM,
travel requires 45 minutes, and the required buffer is 15 minutes.
Therefore, the student needs 60 minutes in total and should leave at
8:30 AM.

The study calculation also only requires reasoning. Three 50-minute
sessions require 150 minutes. Two 10-minute breaks add another
20 minutes, giving a total of 170 minutes.

However, the current-weather question is different. Current weather
is external and time-dependent information. Since the direct prompting
program did not have a weather tool, it could not reliably retrieve
the current weather.

Therefore, direct prompting is suitable for simple questions and
reasoning tasks where the required information is already available
to the model, but it is limited when current external information is
required.

---

## 3. Chain-of-Thought Prompting

Chain-of-Thought prompting asks the model to reason through a problem
carefully before producing the final answer.

In this experiment, the model was instructed to reason carefully about
the calculations while not using external tools.

For the departure-time problem, the reasoning is based on adding the
45-minute travel time and the 15-minute buffer to obtain 60 minutes.
Counting backward 60 minutes from 9:30 AM gives 8:30 AM.

For the study schedule, three 50-minute sessions give 150 minutes.
There are two breaks between three sessions, so the breaks contribute
20 minutes. The complete block therefore takes 170 minutes.

Chain-of-Thought can improve performance on multi-step reasoning
because the model is encouraged to work through intermediate steps.
However, reasoning alone does not provide access to live information.

Therefore, the model still cannot reliably determine current Chennai
weather without an external information source.

For this experiment, private internal reasoning was not printed in the
program output. Only the final answer and short explanation were
displayed.

---

## 4. ReAct Agent

ReAct combines reasoning with actions. Instead of answering every
question directly, the agent can determine whether it needs an
external tool.

The ReAct implementation in this project contains a custom
`get_weather` tool.

The process is:

1. The user provides the college planning question.
2. The model identifies the information needed to answer the question.
3. For the current-weather question, it selects the weather tool.
4. The Python program executes the tool.
5. The tool retrieves current weather information.
6. The tool result is returned to the model as an observation.
7. The model uses the observation together with the reasoning-based
   information to produce the final answer.

The cycle can be represented as:

`Thought → Action → Observation → Thought → Final Answer`

The ReAct agent therefore solves both the reasoning part and the
external-information part of the scenario.

Its main limitation is that tool calls introduce additional processing,
network dependency and possible tool errors. The final answer also
depends on the quality and availability of the external tool.

---

## 5. Comparison Table

| Basis for comparison | Direct prompting | Chain-of-Thought | ReAct agent |
|---|---|---|---|
| Reasoning depth | Low to moderate | Higher for multi-step problems | Higher because reasoning and actions are combined |
| Tool usage | No tool | No tool in this experiment | Uses a weather tool when external information is required |
| Reliability on multi-step questions | Can solve simple multi-step questions but may make mistakes | Generally better for carefully structured reasoning | Can combine reasoning with external observations |
| Transparency | Final answer is visible, but reasoning process is not | Final answer is visible; private reasoning is not exposed | Tool actions and observations can be displayed |
| Speed / cost | Usually fastest and simplest | May require more reasoning tokens | Usually slower because it may involve tool calls |
| Consistency across repeated runs | Can vary when temperature is non-zero | Can also vary at non-zero temperature | Can vary because both model decisions and external information may change |

---

## 6. Self-Consistency Observation

For the self-consistency experiment, I used the following reasoning
question:

"A college class starts at 9:30 AM. The student's travel time is
45 minutes and the student wants a 15-minute safety buffer. What time
should the student leave?"

The calculation gives a correct answer of 8:30 AM.

I ran the question five times using a non-zero temperature of 0.8.
The wording of the answers could vary between runs, but the majority
answer in my experiment was:

**8:30 AM**

The majority answer was correct.

I then repeated the experiment with temperature set to 0. The outputs
were more consistent and repeatedly produced the same answer.

This experiment demonstrates that non-zero temperature can introduce
variation between repeated generations, while temperature 0 makes the
generation more deterministic for this experiment.

---

## 7. Suitability Analysis

The ReAct approach is suitable for this particular scenario because
the scenario contains both reasoning questions and a question requiring
current external information.

Direct prompting is sufficient for the arithmetic questions, but it
does not have a mechanism to retrieve current weather information.

Chain-of-Thought improves the handling of multi-step reasoning, but
the experiment shows that reasoning alone cannot provide information
that is not available in the model's input or knowledge.

The ReAct agent can combine reasoning with an external weather tool.
It can identify that current weather is needed, call the tool, observe
the returned information, and then use that information to construct
the final answer.

The self-consistency experiment also shows that repeated model
generation can vary when temperature is non-zero. Therefore,
repeating a reasoning task can help observe whether the answer remains
stable, although repeated generation does not automatically guarantee
correctness.

---

## 8. Limitations

The direct prompting implementation does not have access to live
external data.

The Chain-of-Thought implementation also does not use external tools,
so its answer to time-sensitive questions is limited by the
information available to the model.

The ReAct implementation depends on the availability and correctness
of the weather service. Network failures, incorrect tool results or
incorrect tool selection can affect the final answer.

The experiments also use a small scenario. A larger real-world agent
could require multiple tools, more reasoning steps and stronger error
handling.

---

## 9. General Conclusion

Direct prompting is appropriate when the question is simple and the
model already has the information needed to answer it. It is useful
when low latency and simplicity are important.

Chain-of-Thought prompting is useful for problems that require several
reasoning steps, calculations or logical connections. It can improve
the model's ability to work through a problem, but reasoning does not
automatically provide access to new external information.

ReAct is appropriate when a problem requires both reasoning and
interaction with external tools. The agent can determine what
information it needs, perform an action such as calling a tool,
observe the result and continue reasoning before producing the final
answer.

Therefore, the main difference demonstrated by this experiment is
that direct prompting produces an immediate answer, Chain-of-Thought
focuses on deeper step-by-step problem solving without tool access,
and ReAct combines reasoning with actions and observations to solve
problems that require external information.