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

One tradeoff is in conflict detection: it warns only when two tasks share the *exact* same scheduled time, rather than detecting when one task's duration overlaps another's. This keeps the algorithm simple and readable — it just groups tasks by their fixed start time and flags any slot with more than one task — and it works well for basic schedule warnings like two tasks both set for 08:30. The cost is that it can miss conflicts caused by duration, such as a 30-minute task at 08:00 running into a task at 08:15. A future improvement would compare each task's start *and* end time to catch overlapping ranges, not just identical start times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
