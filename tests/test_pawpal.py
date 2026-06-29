"""Tests for PawPal+ Task behavior."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task("Morning walk", duration=30, priority=3)

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet(name="Rex", species="dog")
    task = Task("Morning walk", duration=30, priority=3)

    before = len(pet.get_tasks())
    pet.add_task(task)
    after = len(pet.get_tasks())

    assert after == before + 1


def test_daily_recurring_task_creates_next_occurrence():
    due = date(2026, 6, 28)
    task = Task("Brush teeth", duration=5, priority=2, frequency="daily", due_date=due)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == due + timedelta(days=1)


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    tasks = [
        Task("Evening walk", duration=25, priority=2, fixed_time="18:00"),
        Task("Morning walk", duration=30, priority=3, fixed_time="08:00"),
        Task("Lunch", duration=10, priority=2, fixed_time="12:00"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.fixed_time for task in ordered] == ["08:00", "12:00", "18:00"]


def test_detect_conflicts_warns_about_same_time():
    pet = Pet(name="Rex", species="dog")
    pet.add_task(Task("Breakfast", duration=10, priority=3, fixed_time="08:30"))
    pet.add_task(Task("Morning meds", duration=5, priority=3, fixed_time="08:30"))

    owner = Owner(name="Sam", available_minutes=90)
    owner.add_pet(pet)

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "08:30" in warnings[0]
