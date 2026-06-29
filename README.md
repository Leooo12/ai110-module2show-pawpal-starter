# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- **Pet management** — add pets with name, species, and optional breed/age/notes to an owner, and list them.
- **Task management** — create care tasks with duration, priority, and optional category/fixed time, then assign them to a pet.
- **Sorting by time** — order tasks chronologically by fixed time, with flexible (no-time) tasks last.
- **Priority scheduling** — order and select tasks High → Medium → Low (`3/2/1`), tie-breaking by time, so the most important tasks claim the time budget first.
- **Filtering** — filter tasks by completion status or by pet name.
- **Recurring tasks** — completing a `"daily"`/`"weekly"` task spawns the next occurrence with its due date rolled forward.
- **Conflict warnings** — flag tasks that share the same fixed time (read-only; never alters the schedule).
- **Daily plan generation** — resolve conflicts, sort by priority, fit tasks to the owner's time budget, assign start times, and explain the result.
- **Streamlit UI** (`app.py`) — add pets/tasks with success messages, view a pet's tasks in a time-sorted table, and see live conflict warnings.
- **CLI demo** (`python main.py`) — builds sample data and prints sorted/filtered task lists, a recurrence demo, conflict warnings, and the full daily schedule.
- **Automated tests** (`pytest`) — `tests/test_pawpal.py` covers task lifecycle, recurrence, sorting, and conflict detection.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python main.py` produces the following CLI output:

```
====================================================
  TODAY'S SCHEDULE
  Owner: Sam   |   Budget: 90 min
====================================================
  08:00   Morning walk        30 min   (walk)
  08:30   Breakfast           10 min   (feeding)
  08:40   Feed                10 min   (feeding)
  18:00   Evening walk        25 min   (walk)
  18:25   Brush coat          15 min   (grooming)
----------------------------------------------------
  Time used: 90 / 90 min

  Why this plan:
    Scheduled 5 task(s) using 90 of 90 available minutes.
====================================================
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

### What the tests cover

The suite in `tests/test_pawpal.py` verifies the core scheduling behaviors:

- **Task completion** — a new task starts incomplete and `mark_complete()` marks it done.
- **Task addition** — `Pet.add_task()` adds a task to a pet's list.
- **Recurrence logic** — completing a `"daily"` task returns a new task with its `due_date` rolled forward one day.
- **Sorting correctness** — `Scheduler.sort_by_time()` returns out-of-order tasks in chronological order.
- **Priority scheduling** — `Scheduler.sort_by_priority()` orders High → Medium → Low and tie-breaks by time, and `generate_plan()` keeps the higher-priority task when the budget only fits one.
- **Conflict detection** — `Scheduler.detect_conflicts()` warns when two tasks share the same scheduled time.

### Successful output

```
============================= test session starts ==============================
platform darwin -- Python 3.10.15, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/leo/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 5 items

tests/test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.01s ===============================
```

### Confidence Level

⭐⭐⭐⭐☆ (4/5)

All 5 tests pass and cover the most important scheduling behaviors (sorting, recurrence, conflict detection, task lifecycle). Held back from 5/5 because some edge cases remain untested — e.g. pets with no tasks, duplicate-time handling during `generate_plan()`, and weekly recurrence.

## 📐 Smarter Scheduling

PawPal+ adds a small algorithmic layer on top of the basic planner:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns a new list ordered by `fixed_time`; flexible (no-time) tasks go last. |
| Priority sorting | `Scheduler.sort_by_priority()` | Orders tasks High → Medium → Low (priority `3 → 2 → 1`), tie-breaking by time (the same rule as `sort_by_time`). Drives task selection in `generate_plan()`. |
| Filtering | `Scheduler.filter_by_completion()`, `Scheduler.filter_by_pet_name()` | Filter tasks by completion status, or by a pet's name via the `Owner → Pet → tasks` chain. |
| Conflict detection | `Scheduler.detect_conflicts()` | Returns warning strings for tasks sharing the same `fixed_time`; read-only, never raises. |
| Recurring tasks | `Task.mark_complete()` (with `Task.frequency` and `Task.due_date`) | Completing a `"daily"`/`"weekly"` task returns the next occurrence with its `due_date` rolled forward. |

## 🏆 Optional Challenges

Two optional challenges have been implemented on top of the base project.

### Priority-Based Scheduling

**Method:** `Scheduler.sort_by_priority(tasks)`

**How priority affects sorting.** Each `Task` carries an integer `priority` where
`3 = High`, `2 = Medium`, `1 = Low`. `sort_by_priority()` returns a new list
ordered by priority descending — High before Medium before Low — and breaks ties
by time using the same rule as `sort_by_time()`: fixed-time tasks first (ascending
by `HH:MM`), then flexible (no-time) tasks. `generate_plan()` calls this method to
decide which tasks claim the time budget first, so when time runs short the
higher-priority task is kept and the lower-priority one is skipped.

**Sample CLI output** (from `python main.py`):

```
====================================================
  TASKS BY PRIORITY (High -> Low, then time)        
----------------------------------------------------
  [HIGH  ]  08:00   Morning walk        30 min
  [HIGH  ]  08:30   Breakfast           10 min
  [MEDIUM]  18:00   Evening walk        25 min
  [MEDIUM]    --   Feed                10 min
  [LOW   ]    --   Brush coat          15 min
====================================================
```

### Data Persistence

**Methods:** `Owner.save_to_json(path="data.json")` and
`Owner.load_from_json(path="data.json")` (a classmethod), backed by
`to_dict()` / `from_dict()` on `Owner`, `Pet`, and `Task`.

**`data.json` workflow.** `save_to_json()` serializes the full
`Owner → Pet → Task` tree to a JSON file (the `due_date` `date` is stored as an
ISO `YYYY-MM-DD` string). `load_from_json()` reads it back into live objects, or
returns `None` when the file is missing so first-run callers can fall back to
fresh demo data. In `main.py`, startup does exactly that:
`Owner.load_from_json("data.json") or build_owner()`, and a `demo_persistence()`
step saves the owner and reloads it to confirm the round-trip.

> Note: re-running `python main.py` reloads the saved `data.json`, so the demo's
> added tasks accumulate across runs. Delete `data.json` to start from fresh demo
> data. `data.json` is listed in `.gitignore` and is not committed.

**Files modified:**

- `pawpal_system.py` — added `to_dict()` / `from_dict()` to `Task`, `Pet`, and
  `Owner`, plus `Owner.save_to_json()` / `Owner.load_from_json()`.
- `main.py` — load from `data.json` on startup and added a `demo_persistence()` step.
- `tests/test_pawpal.py` — added round-trip tests for `Task` and `Owner` save/load, plus the missing-file case.
- `.gitignore` — added `data.json`.
- `data.json` — generated at runtime (gitignored, not tracked).

**Sample CLI output** (from `python main.py`):

```
====================================================
  PERSISTENCE (save -> load data.json)              
----------------------------------------------------
  Saved owner 'Sam' to data.json
  Reloaded owner 'Sam' with 2 pet(s) and 10 task(s)
====================================================
```

## Demo Walkthrough

### Main UI features (`streamlit run app.py`)

- Enter owner and pet details, then **Add pet** (a success message confirms each addition).
- Add tasks with a title, duration, priority, and optional fixed time, assigned to a chosen pet.
- The selected pet's tasks render in a **time-sorted table** (time, task, duration, priority, done).
- **Conflict warnings** appear automatically when two tasks share the same fixed time.

### Example workflow: add pet → add task → view schedule

1. **Add a pet** — e.g. `Mochi` (dog). The pet appears under "Current pets".
2. **Add a task** — e.g. `Morning walk`, 20 min, high priority, fixed time `08:00`, assigned to Mochi.
3. **View the schedule** — the task list updates to a time-sorted table, and any same-time clashes show as conflict warnings. For the full prioritized daily plan (with budget filtering and reasoning), run the CLI demo below.

### Scheduler behaviors

- **Sorting** — `sort_by_time()` arranges tasks by their fixed time; flexible tasks fall to the end.
- **Filtering** — `filter_by_completion()` (todo vs. done) and `filter_by_pet_name()` (tasks for one pet).
- **Recurring tasks** — completing a `"daily"`/`"weekly"` task returns the next occurrence with its due date advanced.
- **Conflict warnings** — `detect_conflicts()` reports tasks competing for the same fixed time slot.

### Sample CLI output (`python main.py`)

```
====================================================
  ALL TASKS (as entered, unsorted)                  
----------------------------------------------------
  18:00   [todo]  Evening walk        25 min   (walk)
  08:00   [todo]  Morning walk        30 min   (walk)
  08:30   [done]  Morning meds         5 min   (meds)
  08:30   [todo]  Breakfast           10 min   (feeding)
    --   [todo]  Brush coat          15 min   (grooming)
    --   [todo]  Feed                10 min   (feeding)
====================================================

====================================================
  ALL TASKS (sorted by time)                        
----------------------------------------------------
  08:00   [todo]  Morning walk        30 min   (walk)
  08:30   [done]  Morning meds         5 min   (meds)
  08:30   [todo]  Breakfast           10 min   (feeding)
  18:00   [todo]  Evening walk        25 min   (walk)
    --   [todo]  Brush coat          15 min   (grooming)
    --   [todo]  Feed                10 min   (feeding)
====================================================

====================================================
  INCOMPLETE TASKS ONLY                             
----------------------------------------------------
  08:00   [todo]  Morning walk        30 min   (walk)
  08:30   [todo]  Breakfast           10 min   (feeding)
  18:00   [todo]  Evening walk        25 min   (walk)
    --   [todo]  Brush coat          15 min   (grooming)
    --   [todo]  Feed                10 min   (feeding)
====================================================

====================================================
  TASKS FOR REX                                     
----------------------------------------------------
  08:00   [todo]  Morning walk        30 min   (walk)
  08:30   [done]  Morning meds         5 min   (meds)
  08:30   [todo]  Breakfast           10 min   (feeding)
  18:00   [todo]  Evening walk        25 min   (walk)
====================================================

====================================================
  REX — BEFORE completing recurring task            
----------------------------------------------------
  18:00   [todo]  Evening walk        25 min   (walk)
  08:00   [todo]  Morning walk        30 min   (walk)
  08:30   [done]  Morning meds         5 min   (meds)
  08:30   [todo]  Breakfast           10 min   (feeding)
    --   [todo]  Brush teeth          5 min   (grooming)
====================================================

  Auto-created next 'Brush teeth' due 2026-06-29 (was 2026-06-28, now completed=True)

====================================================
  REX — AFTER completing recurring task             
----------------------------------------------------
  18:00   [todo]  Evening walk        25 min   (walk)
  08:00   [todo]  Morning walk        30 min   (walk)
  08:30   [done]  Morning meds         5 min   (meds)
  08:30   [todo]  Breakfast           10 min   (feeding)
    --   [done]  Brush teeth          5 min   (grooming)
    --   [todo]  Brush teeth          5 min   (grooming)
====================================================

====================================================
  CONFLICT WARNINGS                                 
----------------------------------------------------
  - Conflict at 08:00: Rex's 'Morning walk', Rex's 'Vet check', Mia's 'Morning pill'
  - Conflict at 08:30: Rex's 'Morning meds', Rex's 'Breakfast'
====================================================

====================================================
  TODAY'S SCHEDULE                                  
  Owner: Sam   |   Budget: 90 min                   
====================================================
  08:00   Morning walk        30 min   (walk)
  08:30   Morning meds         5 min   (meds)
  18:00   Evening walk        25 min   (walk)
  18:25   Brush teeth          5 min   (grooming)
  18:30   Brush teeth          5 min   (grooming)
  18:35   Feed                10 min   (feeding)
----------------------------------------------------
  Time used: 80 / 90 min

  Skipped:
    - Breakfast
    - Vet check
    - Morning pill
    - Brush coat

  Why this plan:
    Scheduled 6 task(s) using 80 of 90 available minutes.
    Skipped 'Breakfast': time conflict with a higher-priority task.
    Skipped 'Vet check': time conflict with a higher-priority task.
    Skipped 'Morning pill': time conflict with a higher-priority task.
    Skipped 'Brush coat': not enough time left in the budget.
====================================================
```
