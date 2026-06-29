"""PawPal+ CLI demo.

Builds a small set of pets and tasks for one owner, then uses the
Scheduler to generate and print today's daily plan.
"""

from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def build_owner() -> Owner:
    """Create one owner with two pets and a few care tasks.

    Tasks are intentionally added out of chronological order (and one is
    marked complete) so the sorting and filtering demos have something to do.
    """
    owner = Owner(name="Sam", available_minutes=90)

    # Pet 1: a dog. Tasks added evening-first to show off sort_by_time.
    rex = Pet(name="Rex", species="dog", breed="Labrador", age=4)
    rex.add_task(Task("Evening walk", duration=25, priority=2, category="walk", fixed_time="18:00"))
    rex.add_task(Task("Morning walk", duration=30, priority=3, category="walk", fixed_time="08:00"))
    morning_meds = Task("Morning meds", duration=5, priority=3, category="meds", fixed_time="08:30")
    morning_meds.mark_complete()  # already done today
    rex.add_task(morning_meds)
    rex.add_task(Task("Breakfast", duration=10, priority=3, category="feeding", fixed_time="08:30"))
    owner.add_pet(rex)

    # Pet 2: a cat with lighter, flexible needs (no fixed times).
    mia = Pet(name="Mia", species="cat", notes="indoor only")
    mia.add_task(Task("Brush coat", duration=15, priority=1, category="grooming"))
    mia.add_task(Task("Feed", duration=10, priority=2, category="feeding"))
    owner.add_pet(mia)

    return owner


def print_task_list(title: str, tasks) -> None:
    """Print a titled list of tasks, one per line, readable in the terminal."""
    width = 52
    print("=" * width)
    print(f"  {title}".ljust(width))
    print("-" * width)
    if not tasks:
        print("  (no tasks)")
    else:
        for task in tasks:
            time = task.fixed_time if task.fixed_time else "  --"
            status = "done" if task.completed else "todo"
            category = task.category if task.category else "-"
            print(f"  {time}   [{status}]  {task.name:<18} {task.duration:>3} min   ({category})")
    print("=" * width)
    print()


def demo_sorting_and_filtering(owner: Owner, scheduler: Scheduler) -> None:
    """Show the new sort_by_time and filtering helpers on the owner's tasks."""
    tasks = owner.all_tasks()

    # As entered: deliberately out of chronological order.
    print_task_list("ALL TASKS (as entered, unsorted)", tasks)

    # Sorted chronologically; flexible (no fixed time) tasks fall to the end.
    print_task_list("ALL TASKS (sorted by time)", scheduler.sort_by_time(tasks))

    # Only what still needs doing today.
    incomplete = scheduler.filter_by_completion(tasks, completed=False)
    print_task_list("INCOMPLETE TASKS ONLY", scheduler.sort_by_time(incomplete))

    # Tasks for a single selected pet, in time order.
    pet_name = "Rex"
    rex_tasks = scheduler.filter_by_pet_name(owner, pet_name)
    print_task_list(f"TASKS FOR {pet_name.upper()}", scheduler.sort_by_time(rex_tasks))


def demo_recurring(owner: Owner) -> None:
    """Show that completing a recurring task auto-creates the next occurrence."""
    rex = owner.pets[0]

    # A daily recurring task with an explicit due date.
    teeth = Task(
        "Brush teeth",
        duration=5,
        priority=2,
        category="grooming",
        frequency="daily",
        due_date=date(2026, 6, 28),
    )
    rex.add_task(teeth)

    print_task_list(f"{rex.name.upper()} — BEFORE completing recurring task", rex.get_tasks())

    # Completing a recurring task returns its next occurrence; add it back.
    next_task = teeth.mark_complete()
    if next_task is not None:
        rex.add_task(next_task)
        print(f"  Auto-created next '{next_task.name}' due {next_task.due_date} "
              f"(was {teeth.due_date}, now completed={teeth.completed})")
        print()

    print_task_list(f"{rex.name.upper()} — AFTER completing recurring task", rex.get_tasks())


def demo_conflicts(owner: Owner, scheduler: Scheduler) -> None:
    """Show conflict detection: warn when tasks share a scheduled time."""
    rex, mia = owner.pets[0], owner.pets[1]

    # Add a cross-pet clash: both pets need attention at 08:00.
    rex.add_task(Task("Vet check", duration=20, priority=3, category="meds", fixed_time="08:00"))
    mia.add_task(Task("Morning pill", duration=5, priority=3, category="meds", fixed_time="08:00"))

    width = 52
    print("=" * width)
    print("  CONFLICT WARNINGS".ljust(width))
    print("-" * width)
    warnings = scheduler.detect_conflicts(owner)
    if not warnings:
        print("  No conflicts found.")
    else:
        for warning in warnings:
            print(f"  - {warning}")
    print("=" * width)
    print()


def print_plan(owner: Owner, plan) -> None:
    """Print the generated plan as a clean, aligned terminal report."""
    width = 52
    print("=" * width)
    print("  TODAY'S SCHEDULE".ljust(width))
    print(f"  Owner: {owner.name}   |   Budget: {owner.available_minutes} min".ljust(width))
    print("=" * width)

    if not plan.scheduled_items:
        print("  (nothing scheduled)")
    else:
        for start, task in plan.scheduled_items:
            category = f"{task.category}" if task.category else "-"
            print(f"  {start}   {task.name:<18} {task.duration:>3} min   ({category})")

    print("-" * width)
    print(f"  Time used: {plan.total_time_used} / {owner.available_minutes} min")

    if plan.skipped_tasks:
        print()
        print("  Skipped:")
        for task in plan.skipped_tasks:
            print(f"    - {task.name}")

    print()
    print("  Why this plan:")
    for line in plan.explain().splitlines():
        print(f"    {line}")
    print("=" * width)


def main() -> None:
    """Build the demo data, show sorting/filtering, then print the plan."""
    owner = build_owner()
    scheduler = Scheduler()

    demo_sorting_and_filtering(owner, scheduler)
    demo_recurring(owner)
    demo_conflicts(owner, scheduler)

    plan = scheduler.plan_for(owner)
    print_plan(owner, plan)


if __name__ == "__main__":
    main()
