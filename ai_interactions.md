# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

This covers the **Data Persistence** challenge, which the agent implemented in this
session. (Priority-Based Scheduling landed in an earlier session and is summarized
at the end.)

**Files modified**

- `pawpal_system.py` — agent added `to_dict()`/`from_dict()` to `Task`, `Pet`, and `Owner`, plus `Owner.save_to_json()` and `Owner.load_from_json()`.
- `main.py` — agent added load-on-startup (`Owner.load_from_json("data.json") or build_owner()`) and a `demo_persistence()` round-trip step.
- `tests/test_pawpal.py` — agent added three tests: `Task` round-trip, `Owner` save/load round-trip, and the missing-file case.
- `.gitignore` — agent added `data.json`.
- `README.md` — I wrote the "Optional Challenges" prose; the agent supplied the verified CLI output and added the `tests`/`.gitignore` entries to the files-modified list.
- `ai_interactions.md` — this log.

**What I asked the agent to do**

- First plan JSON persistence only (no edits): inspect the classes and recommend the simplest serialization, preferring custom `to_dict`/`from_dict` over a library unless clearly necessary.
- Then implement it: `save_to_json`/`load_from_json`, persist `Owner`/`Pet`/`Task` to `data.json` and load them back into real objects, standard library only, no databases, update `main.py`/`app.py` only as needed, and add tests if practical.
- Document the Priority and Data Persistence challenges in `README.md` using real method names and real CLI output, without inventing output.

**What the agent completed**

- Custom `to_dict`/`from_dict` on all three models plus `save_to_json`/`load_from_json` on `Owner`, using only the stdlib `json`. `Task.due_date` is stored as an ISO `YYYY-MM-DD` string and parsed back on load.
- Wired `main.py` to load on startup and to save/reload as a round-trip demo.
- Added the three persistence tests; full suite passes (11 passed).
- Captured README CLI samples from clean `python main.py` runs and deleted the generated `data.json` afterward rather than leaving an artifact.

**Manual corrections / decisions I made**

- Required the first turn to be plan-only (no edits) before approving implementation.
- Chose custom `to_dict`/`from_dict` over a serialization library, stdlib-only, and no database.
- Decided `data.json` stores a single owner at the root (matching the one-owner model) and that persistence did **not** need wiring into `app.py` — the `main.py` demo was sufficient.
- Wrote the README challenge prose myself; corrected the agent's initial omission of the test and `.gitignore` files from the modified-files list.

**Earlier session — Priority-Based Scheduling**

- Agent added `Scheduler.sort_by_priority()` (High → Medium → Low, tie-broken by time), routed `generate_plan()` through it, added `demo_priority()` to `main.py`, and added priority tests.
- My decisions there: kept `priority` as plain ints (3/2/1) instead of an enum, and chose the "priority-first, then time" tie-break.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
