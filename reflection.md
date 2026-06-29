# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

PawPal+ is built around three core actions a user can perform:

1. **Enter and manage owner and pet info.** The user provides the basic context the plan is built around — their own details and information about their pet (name, type/breed, and any care-relevant constraints).
2. **Add and edit care tasks.** The user builds and adjusts the list of tasks to be scheduled (walks, feeding, medications, enrichment, grooming, and so on), giving each task at minimum a duration and a priority.
3. **Generate and view a daily plan.** The user asks PawPal+ to turn those tasks and constraints (available time, priority, preferences) into a daily schedule, then sees the resulting plan displayed clearly — ideally with an explanation of why tasks were ordered, kept, or dropped.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML modeled PawPal+ as five classes arranged around a clear ownership chain and a separate scheduling step.

- **PetOwner** — the top of the data hierarchy. It holds the owner's `name`, their daily time budget (`available_minutes`), optional `preferences`, and the list of `pets` they own. Its responsibility is to manage owner-level info and the set of pets (`add_pet`, `remove_pet`).
- **Pet** — owns the care tasks for one animal. It holds basic info (`name`, `species`, `breed`, `age`, `notes`) and a list of `tasks`. Its responsibility is to manage its own tasks (`add_task`, `remove_task`, `get_tasks`) and describe itself (`describe`).
- **Task** — the schedulable unit. It holds `name`, `duration`, an integer `priority` (3 = High, 2 = Medium, 1 = Low), an optional `category`, and an optional `fixed_time`. Its responsibility is to know facts about itself — whether it must occur at a set time (`is_fixed`) and how to summarize itself (`summary`). It contains no scheduling logic.
- **Scheduler** — the "brain," and intentionally stateless: it owns no data. It receives a list of tasks and a time budget and produces a plan (`generate_plan`), using internal steps to sort by priority, resolve fixed-time conflicts, and filter tasks to the available budget.
- **Plan** — the result of scheduling plus its explanation. It holds the `scheduled_items` (time + task), `skipped_tasks`, `total_time_used`, and the `reasoning`. Its responsibility is to carry the outcome and present it (`explain`, `to_text`).

The relationships were composition down the ownership chain (PetOwner → Pet → Task) and dependency for the algorithm: the Scheduler *consumes* tasks and *produces* a Plan without owning either. I chose this split so that data, scheduling logic, and the result are each handled by a single class, following the Single Responsibility Principle.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff in the scheduler is its conflict detection strategy. It only warns when two tasks have the exact same scheduled start time, rather than detecting when one task's duration overlaps another. This approach keeps the algorithm simple, readable, and efficient by grouping tasks according to their start time and flagging any time slot containing multiple tasks. It works well for basic schedule warnings, such as two tasks both scheduled for 08:30. However, it may miss conflicts caused by overlapping durations, such as a 30-minute task beginning at 08:00 followed by another task at 08:15. A future improvement would compare each task's start and end times to detect overlapping time ranges instead of only identical start times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

**c. AI strategy**

The AI features I found most effective were the ones that let me stay in control of the design rather than hand it off. Having the assistant read my actual files before suggesting anything was the biggest one — it would inspect `pawpal_system.py` and `app.py` and tell me where tasks were displayed or which Scheduler methods existed, instead of guessing. Scoped, "do not edit yet" review prompts were also valuable: I could ask for an analysis (for example, comparing my code against the UML, or proposing a Features list) and decide what to act on before any code changed. Asking it to run `main.py` and use the real output, rather than describe what it imagined the output to be, kept the documentation honest.

There was at least one suggestion I modified to keep the design clean. When wiring the Scheduler into the UI, the assistant offered to also implement the "Generate schedule" button in `app.py`. I chose to keep that change out of scope so the task display work stayed focused, and I kept the README honest about the button still being a placeholder rather than letting the docs claim a feature the UI did not yet have. Keeping the data models free of scheduling logic — Tasks answer questions about themselves, the Scheduler does the planning — was a boundary I held to whenever a suggestion risked blurring it.

Using separate chat sessions for different phases helped me stay organized. Keeping design review, the UI changes, the UML update, and the README/reflection work in distinct conversations meant each session had a clear goal and a manageable amount of context, and it was easier to revisit a specific decision later without scrolling through unrelated work. It also made it natural to finish and verify one phase before opening the next.

The main thing I learned about being the lead architect while using AI is that the assistant is fast at producing options and surfacing details, but the responsibility for the design and for verifying the result stays with me. I had to read every suggested change, decide whether it fit the architecture I wanted, and confirm it actually worked — running the tests, running the CLI, and checking the output myself. The AI accelerated the work, but the judgment about what PawPal+ should be, and the accountability for what shipped, were mine.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
