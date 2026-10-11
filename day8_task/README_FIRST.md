# Day 8 Task Support Files

This folder contains the exact new placement policy document from the task sheet, a results report template, and a safe `.gitignore`.

## Important
These are support files, not a replacement for your working `PSLevel_1_Class` lab. The task requires preserving the existing course-fee tools, calculator, graph/memory setup, and all six original handbook data files. Because the original lab source files were not included with the task sheet, do not replace `lc_config.py`, `1_ingest.py`, `2_search.py`, or `5_agentic_rag.py` with guessed versions.

## Put the files in your existing `day8_task` folder
1. Copy `data/placement_policy.md` into `day8_task/data/`.
2. Copy `results.md` into `day8_task/`.
3. Merge the `.gitignore` entries into the existing `.gitignore` (do not remove other needed entries).
4. Copy the original working lab files from `PSLevel_1_Class` into `day8_task`: `lc_config.py`, `1_ingest.py`, `2_search.py`, and the six existing files in `data/`.
5. Copy `5_agentic_rag.py` to `task_agent.py`; edit only `task_agent.py` for Parts B–D.
6. Run `python 1_ingest.py`, then update `2_search.py` with the placement query and capture actual outputs.
7. Add the eligibility tool, score-based relevance guard, and five-question test loop to `task_agent.py` using the existing project's APIs.
8. Run `python task_agent.py > run_log.txt` from `day8_task`, then inspect `run_log.txt` and complete `results.md` with actual observed results.
9. Verify `.env` and `chroma_db/` are not tracked, then commit and push the `day8_task` folder/repository as your course instructions require.

## Tool rules from the task sheet
- `check_exam_eligibility`: invalid values outside 0–100 return an error string; 75+ eligible; 65 to below 75 requires condonation at Rs. 500 per course; below 65 not eligible.
- `search_handbook`: call `store.similarity_search_with_score(query, k=3)`, retain only scores `<= MAX_DISTANCE`, and return exactly `NO_MATCH: this is not covered in the college handbook.` if nothing remains.
- System prompt: when `search_handbook` returns `NO_MATCH`, the agent must say it does not know.
- Five questions must run in one thread with `thread_id="task-run"`; the fourth question should rely on the prior fee-question context.
