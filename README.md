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
| Filtering | `Scheduler.filter_by_completion()`, `Scheduler.filter_by_pet_name()` | Filter tasks by completion status, or by a pet's name via the `Owner → Pet → tasks` chain. |
| Conflict detection | `Scheduler.detect_conflicts()` | Returns warning strings for tasks sharing the same `fixed_time`; read-only, never raises. |
| Recurring tasks | `Task.mark_complete()` (with `Task.frequency` and `Task.due_date`) | Completing a `"daily"`/`"weekly"` task returns the next occurrence with its `due_date` rolled forward. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
