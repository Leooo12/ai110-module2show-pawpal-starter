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


def test_sort_by_priority_orders_high_before_medium_before_low():
    scheduler = Scheduler()
    tasks = [
        Task("Brush coat", duration=15, priority=1),   # Low
        Task("Morning walk", duration=30, priority=3),  # High
        Task("Feed", duration=10, priority=2),          # Medium
    ]

    ordered = scheduler.sort_by_priority(tasks)

    assert [task.priority for task in ordered] == [3, 2, 1]


def test_sort_by_priority_breaks_ties_by_time():
    scheduler = Scheduler()
    tasks = [
        Task("Evening meds", duration=5, priority=3, fixed_time="18:00"),
        Task("Morning meds", duration=5, priority=3, fixed_time="08:00"),
        Task("Flexible meds", duration=5, priority=3),  # no fixed time -> last
    ]

    ordered = scheduler.sort_by_priority(tasks)

    assert [task.name for task in ordered] == [
        "Morning meds",
        "Evening meds",
        "Flexible meds",
    ]


def test_generate_plan_schedules_high_priority_first_under_budget():
    scheduler = Scheduler()
    tasks = [
        Task("Low task", duration=30, priority=1),
        Task("High task", duration=30, priority=3),
    ]

    plan = scheduler.generate_plan(tasks, available_minutes=30)

    scheduled = [task.name for _, task in plan.scheduled_items]
    assert scheduled == ["High task"]
    assert [task.name for task in plan.skipped_tasks] == ["Low task"]


def test_task_to_dict_from_dict_round_trip():
    task = Task(
        "Brush teeth",
        duration=5,
        priority=2,
        category="grooming",
        fixed_time="08:00",
        completed=True,
        frequency="daily",
        due_date=date(2026, 6, 28),
    )

    restored = Task.from_dict(task.to_dict())

    assert restored == task
    assert restored.due_date == date(2026, 6, 28)


def test_owner_save_and_load_round_trip(tmp_path):
    pet = Pet(name="Rex", species="dog", breed="Labrador", age=4)
    pet.add_task(Task("Morning walk", duration=30, priority=3, fixed_time="08:00"))
    pet.add_task(Task("Brush teeth", duration=5, priority=2,
                      frequency="daily", due_date=date(2026, 6, 28)))
    owner = Owner(name="Sam", available_minutes=90)
    owner.add_pet(pet)

    path = tmp_path / "data.json"
    owner.save_to_json(str(path))
    loaded = Owner.load_from_json(str(path))

    assert isinstance(loaded, Owner)
    assert loaded.name == "Sam"
    assert len(loaded.pets) == 1
    assert isinstance(loaded.pets[0], Pet)
    assert len(loaded.pets[0].tasks) == 2
    assert all(isinstance(t, Task) for t in loaded.pets[0].tasks)
    assert loaded.pets[0].tasks[1].due_date == date(2026, 6, 28)


def test_load_from_json_returns_none_when_missing(tmp_path):
    missing = tmp_path / "does_not_exist.json"

    assert Owner.load_from_json(str(missing)) is None


def test_detect_conflicts_warns_about_same_time():
    pet = Pet(name="Rex", species="dog")
    pet.add_task(Task("Breakfast", duration=10, priority=3, fixed_time="08:30"))
    pet.add_task(Task("Morning meds", duration=5, priority=3, fixed_time="08:30"))

    owner = Owner(name="Sam", available_minutes=90)
    owner.add_pet(pet)

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "08:30" in warnings[0]
