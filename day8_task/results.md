# Day 8 Task — Results Report

## 1. Project Configuration

- **LLM provider:** Groq
- **Model:** `openai/gpt-oss-120b`
- **Embedding provider:** FastEmbed
- **Embedding model:** `BAAI/bge-small-en-v1.5`
- **Maximum retrieval distance:** `0.4`
- **Handbook files:** 6 Markdown files
- **Chunks indexed:** 27
- **Vector dimension:** 384

## 2. Retrieval Results

The following scores were observed during the earlier search tests:

| Query | Top retrieval scores | Expected behavior |
|---|---|---|
| Placement eligibility | 0.177, 0.236, 0.284 | Relevant results retained |
| France capital | 0.573, 0.573, 0.577 | Results rejected by distance threshold |
| Late fee | 0.197, 0.299, 0.333 | Relevant results retained |
| 70% attendance | 0.247, 0.332, 0.338 | Relevant results retained |

Only results with distance scores less than or equal to `MAX_DISTANCE` are retained.

## 3. Eligibility Tool Tests

| Attendance | Expected result |
|---:|---|
| 82% | ELIGIBLE |
| 70% | CONDONATION; Rs. 500 per course |
| 50% | NOT ELIGIBLE |
| 120% | ERROR for an invalid value |

## 4. Five Agent Questions

| Test | Question or task | Observed result |
|---|---|---|
| 1 | Placement eligibility | Correctly retrieved the requirement of CGPA 6.5 or above and no standing arrears |
| 2 | Attendance of 70% | Condonation required at Rs. 500 per course |
| 3 | Course fees for CS101 and AI202, including maximum late fee | Total Rs. 32,000 |
| 4 | Follow-up: pay only 5 days late | Used prior fee-question context; total Rs. 30,500 |
| 5 | Capital of France | Returned `NO_MATCH: this is not covered in the college handbook.` |

## 5. Summary

The previously shared test output showed all five agent tests passing. The relevance guard rejected the unrelated France query, and the follow-up fee question used the earlier conversation context.

**Evidence note:** This report is reconstructed from previously shared terminal results. The original `run_log.txt` was not available when this report was recreated. Rerun the agent and save its actual output before submitting if your task requires a run log.
