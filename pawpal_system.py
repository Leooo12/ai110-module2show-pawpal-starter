"""PawPal+ system skeletons.

Single-file class skeletons generated from the finalized UML.
Ownership (composition): PetOwner -> Pet -> Task.
Scheduler consumes tasks and produces a Plan; it owns no data.

No business logic is implemented here yet — method bodies are stubs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """A single pet-care activity that can be scheduled.

    Attributes:
        name: Short label, e.g. "Morning walk".
        duration: How long the task takes, in minutes.
        priority: Importance as an integer (3 = High, 2 = Medium, 1 = Low).
        category: Optional grouping label (walk, feeding, meds, ...). Display only.
        fixed_time: Optional required start time (e.g. "08:00"); None means flexible.
    """

    name: str
    duration: int
    priority: int
    category: Optional[str] = None
    fixed_time: Optional[str] = None

    def is_fixed(self) -> bool:
        """Return True if this task must occur at a specific time."""
        raise NotImplementedError

    def summary(self) -> str:
        """Return a one-line, human-readable description of the task."""
        raise NotImplementedError


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
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        raise NotImplementedError

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        raise NotImplementedError

    def describe(self) -> str:
        """Return a readable summary of the pet (no task scheduling)."""
        raise NotImplementedError


@dataclass
class PetOwner:
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
        raise NotImplementedError

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        raise NotImplementedError


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
        raise NotImplementedError

    def to_text(self) -> str:
        """Format the plan for display in the UI or CLI."""
        raise NotImplementedError


class Scheduler:
    """Turns a list of tasks and a time budget into a daily Plan.

    Stateless: the Scheduler owns no task data; everything is passed in.
    """

    def generate_plan(self, tasks: list[Task], available_minutes: int) -> Plan:
        """Produce a Plan from the given tasks and time budget."""
        raise NotImplementedError

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (desc), tie-breaking by duration."""
        raise NotImplementedError

    def _resolve_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Resolve overlapping fixed-time tasks."""
        raise NotImplementedError

    def _filter_to_budget(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Keep the highest-priority tasks that fit within the time budget."""
        raise NotImplementedError
