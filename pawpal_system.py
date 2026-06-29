"""PawPal+ system skeletons.

Single-file class skeletons generated from the finalized UML.
Ownership (composition): PetOwner -> Pet -> Task.
Scheduler consumes tasks and produces a Plan; it owns no data.

Business logic is implemented here: models hold data and answer simple
questions about themselves, while the Scheduler turns tasks into a Plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


DAY_START = "08:00"


def _to_minutes(hhmm: str) -> int:
    """Convert an 'HH:MM' string to minutes since midnight."""
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


def _to_hhmm(minutes: int) -> str:
    """Convert minutes since midnight to an 'HH:MM' string."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


@dataclass
class Task:
    """A single pet-care activity that can be scheduled.

    Attributes:
        name: Short label, e.g. "Morning walk".
        duration: How long the task takes, in minutes.
        priority: Importance as an integer (3 = High, 2 = Medium, 1 = Low).
        category: Optional grouping label (walk, feeding, meds, ...). Display only.
        fixed_time: Optional required start time (e.g. "08:00"); None means flexible.
        completed: Whether the task has been done. Starts False.
        frequency: Recurrence cadence: "daily", "weekly", or None for one-off.
        due_date: Optional calendar date the task is due; used to roll forward.
    """

    name: str
    duration: int
    priority: int
    category: Optional[str] = None
    fixed_time: Optional[str] = None
    completed: bool = False
    frequency: Optional[str] = None
    due_date: Optional[date] = None

    def is_fixed(self) -> bool:
        """Return True if this task must occur at a specific time."""
        return self.fixed_time is not None

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed; spawn the next occurrence if recurring.

        Returns the new Task for the next occurrence when this task is
        recurring ("daily" or "weekly"), otherwise None. The next due date is
        the current due_date rolled forward by the recurrence interval (falling
        back to today's date when due_date is unset). The completed task is
        left in place for history.
        """
        self.completed = True

        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None  # not recurring -> no next occurrence

        base = self.due_date if self.due_date is not None else date.today()
        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            fixed_time=self.fixed_time,
            frequency=self.frequency,
            due_date=base + delta,
        )

    def summary(self) -> str:
        """Return a one-line, human-readable description of the task."""
        parts = [f"{self.name} ({self.duration} min)", f"[priority: {self.priority}]"]
        if self.category:
            parts.append(f"({self.category})")
        if self.fixed_time:
            parts.append(f"@ {self.fixed_time}")
        return " ".join(parts)


@dataclass
class Pet:
    """A pet that owns a list of care tasks.

    Attributes:
        name: The pet's name.
        species: e.g. "dog", "cat".
        breed: Optional breed label.
        age: Optional age in years.
        notes: Optional free-text notes (allergies, mobility, etc.).
        tasks: The pet's care tasks (managed via add_task / remove_task).
    """

    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    notes: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)

    def describe(self) -> str:
        """Return a readable summary of the pet (no task scheduling)."""
        details = self.species
        if self.breed:
            details += f", {self.breed}"
        if self.age is not None:
            details += f", {self.age}y"
        summary = f"{self.name} ({details})"
        if self.notes:
            summary += f" — {self.notes}"
        return summary


@dataclass
class Owner:
    """The app user: identity, time budget, preferences, and owned pets.

    Attributes:
        name: The owner's name.
        available_minutes: Total time budget for pet care today, in minutes.
        preferences: Optional scheduling preferences (placeholder until used).
        pets: The owner's pets (managed via add_pet / remove_pet).
    """

    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        self.pets.remove(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets (flattened)."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


@dataclass
class Plan:
    """A generated daily plan and the reasoning behind it.

    Attributes:
        scheduled_items: Ordered (start_time, Task) entries that made the plan.
        skipped_tasks: Tasks that did not fit the time budget.
        total_time_used: Total scheduled minutes.
        reasoning: Human-readable explanation of what was kept or dropped.
    """

    scheduled_items: list[tuple[str, Task]] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    total_time_used: int = 0
    reasoning: str = ""

    def explain(self) -> str:
        """Return the stored reasoning for this plan."""
        return self.reasoning

    def to_text(self) -> str:
        """Format the plan for display in the UI or CLI."""
        if not self.scheduled_items:
            lines = ["No tasks scheduled."]
        else:
            lines = ["Daily plan:"]
            for start, task in self.scheduled_items:
                lines.append(f"  {start} — {task.summary()}")

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped:")
            for task in self.skipped_tasks:
                lines.append(f"  - {task.name}")

        lines.append("")
        lines.append(f"Total time used: {self.total_time_used} min")
        return "\n".join(lines)


class Scheduler:
    """Turns a list of tasks and a time budget into a daily Plan.

    Stateless: the Scheduler owns no task data; everything is passed in.
    """

    def generate_plan(
        self, tasks: list[Task], available_minutes: int, day_start: str = DAY_START
    ) -> Plan:
        """Produce a Plan from the given tasks and time budget.

        day_start is the clock time the day begins (e.g. "08:00"); flexible
        tasks are assigned start times sequentially from this point.

        Runs sorting, conflict resolution, and budget filtering, then assigns
        times and returns a Plan describing the result.
        """
        # 1. Drop fixed-time tasks that conflict with a higher-priority one.
        resolved = self._resolve_conflicts(tasks)
        conflict_dropped = [t for t in tasks if t not in resolved]

        # 2. Order by priority, then 3. keep only what fits the time budget.
        ordered = self._sort_tasks(resolved)
        kept = self._filter_to_budget(ordered, available_minutes)
        budget_dropped = [t for t in ordered if t not in kept]

        # 4. Assign start times and build the chronological schedule.
        scheduled_items = self._assign_times(kept, day_start)
        total_time_used = sum(task.duration for _, task in scheduled_items)
        skipped_tasks = conflict_dropped + budget_dropped

        reasoning = self._build_reasoning(
            scheduled_items, conflict_dropped, budget_dropped, available_minutes
        )

        return Plan(
            scheduled_items=scheduled_items,
            skipped_tasks=skipped_tasks,
            total_time_used=total_time_used,
            reasoning=reasoning,
        )

    def plan_for(self, owner: Owner, day_start: str = DAY_START) -> Plan:
        """Retrieve every task across the owner's pets and plan them.

        Convenience wrapper that pulls tasks from the owner and uses the
        owner's time budget, so callers can schedule straight from an Owner.
        """
        return self.generate_plan(owner.all_tasks(), owner.available_minutes, day_start)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a new list of tasks ordered chronologically by start time.

        Fixed-time tasks come first, ascending by their 'HH:MM' time; flexible
        tasks (no fixed_time) follow, keeping their original relative order.
        The input list is not mutated, and the sort is stable so tasks sharing
        the same fixed_time preserve their original order.
        """
        return sorted(
            tasks,
            key=lambda task: (
                task.fixed_time is None,
                _to_minutes(task.fixed_time) if task.fixed_time is not None else 0,
            ),
        )

    def filter_by_completion(
        self, tasks: list[Task], completed: bool = False
    ) -> list[Task]:
        """Return a new list of tasks matching the given completion status.

        Defaults to completed=False, i.e. the still-to-do tasks. The input
        list is not mutated.
        """
        return [task for task in tasks if task.completed == completed]

    def filter_by_pet_name(self, owner: Owner, pet_name: str) -> list[Task]:
        """Return the tasks belonging to the owner's pet with this name.

        Tasks carry no pet reference, so ownership is resolved through the
        Owner -> Pet -> tasks structure. Matching is case-insensitive. Returns
        an empty list if no pet with that name exists.
        """
        wanted = pet_name.casefold()
        tasks: list[Task] = []
        for pet in owner.pets:
            if pet.name.casefold() == wanted:
                tasks.extend(pet.get_tasks())
        return tasks

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return warnings for tasks sharing the same scheduled (fixed) time.

        Lightweight, read-only check: tasks are grouped by their fixed_time and
        any slot holding two or more tasks produces one warning string naming
        the clashing tasks and their pets. Flexible tasks (no fixed_time) are
        ignored. Never raises and never alters the schedule.
        """
        by_time: dict[str, list[tuple[str, str]]] = {}
        for pet in owner.pets:
            for task in pet.get_tasks():
                if task.fixed_time is None:
                    continue
                by_time.setdefault(task.fixed_time, []).append((pet.name, task.name))

        warnings: list[str] = []
        for time in sorted(by_time):
            entries = by_time[time]
            if len(entries) > 1:
                names = ", ".join(f"{pet}'s '{task}'" for pet, task in entries)
                warnings.append(f"Conflict at {time}: {names}")
        return warnings

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (desc), tie-breaking by duration."""
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def _resolve_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Resolve overlaps among fixed-time tasks only.

        Flexible tasks have no time until generate_plan places them, so they
        cannot conflict at this stage; placing them into open gaps happens in
        generate_plan, not here.
        """
        flexible = [t for t in tasks if not t.is_fixed()]
        fixed = [t for t in tasks if t.is_fixed()]

        kept_fixed: list[Task] = []
        occupied: list[tuple[int, int]] = []
        # Higher priority wins a slot; tie-break by earlier start time.
        for task in sorted(fixed, key=lambda t: (-t.priority, _to_minutes(t.fixed_time))):
            start = _to_minutes(task.fixed_time)
            end = start + task.duration
            if any(start < o_end and o_start < end for o_start, o_end in occupied):
                continue  # overlaps an already-kept fixed task -> conflict
            occupied.append((start, end))
            kept_fixed.append(task)

        return kept_fixed + flexible

    def _filter_to_budget(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Keep the highest-priority tasks that fit within the time budget."""
        kept: list[Task] = []
        used = 0
        for task in tasks:
            if used + task.duration <= available_minutes:
                kept.append(task)
                used += task.duration
        return kept

    def _assign_times(
        self, tasks: list[Task], day_start: str = DAY_START
    ) -> list[tuple[str, Task]]:
        """Assign each kept task a start time and return them chronologically.

        Fixed tasks anchor at their required time; flexible tasks flow from
        day_start on a running clock that fixed tasks also advance.
        """
        clock = _to_minutes(day_start)
        items: list[tuple[int, Task]] = []
        for task in tasks:
            start = _to_minutes(task.fixed_time) if task.is_fixed() else clock
            clock = max(clock, start + task.duration)
            items.append((start, task))

        items.sort(key=lambda pair: pair[0])
        return [(_to_hhmm(start), task) for start, task in items]

    def _build_reasoning(
        self,
        scheduled_items: list[tuple[str, Task]],
        conflict_dropped: list[Task],
        budget_dropped: list[Task],
        available_minutes: int,
    ) -> str:
        """Build a human-readable explanation of the scheduling choices."""
        used = sum(task.duration for _, task in scheduled_items)
        lines = [
            f"Scheduled {len(scheduled_items)} task(s) using {used} of "
            f"{available_minutes} available minutes."
        ]
        for task in conflict_dropped:
            lines.append(f"Skipped '{task.name}': time conflict with a higher-priority task.")
        for task in budget_dropped:
            lines.append(f"Skipped '{task.name}': not enough time left in the budget.")
        return "\n".join(lines)
