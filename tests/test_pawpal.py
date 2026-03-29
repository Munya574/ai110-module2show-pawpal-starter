from pawpal_system import Pet, Task


def test_task_completion_marks_task_completed():
    task = Task(description="Test task", duration_minutes=10, frequency="once", priority=1)
    assert not task.completed

    task.mark_complete()

    assert task.completed


def test_adding_task_to_pet_increases_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Feed", duration_minutes=10, frequency="daily", priority=1))

    assert len(pet.tasks) == 1
