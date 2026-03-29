from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def format_schedule(tasks):
    if not tasks:
        return "No tasks scheduled for today."

    lines = ["Today's Schedule:"]
    for index, task in enumerate(tasks, start=1):
        date_part = task.due_date.isoformat() if task.due_date else "No date"
        time_part = task.due_time or "No time"
        lines.append(
            f"{index}. {task.description} — {task.duration_minutes} min | "
            f"{date_part} {time_part} | {task.frequency} | priority {task.priority} | pet {task.pet_name}"
        )
    return "\n".join(lines)


def main():
    owner = Owner(name="Jordan", available_minutes=90)

    dog = Pet(name="Mochi", species="dog", age=4)
    cat = Pet(name="Piper", species="cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            description="Brush coat",
            duration_minutes=25,
            frequency="once",
            priority=3,
            category="grooming",
            due_time="15:00",
            due_date=date.today(),
        )
    )
    dog.add_task(
        Task(
            description="Morning walk",
            duration_minutes=20,
            frequency="daily",
            priority=1,
            category="walk",
            due_time="09:00",
            due_date=date.today(),
        )
    )
    cat.add_task(
        Task(
            description="Feed breakfast",
            duration_minutes=10,
            frequency="daily",
            priority=1,
            category="feed",
            due_time="09:00",
            due_date=date.today(),
        )
    )
    cat.add_task(
        Task(
            description="Play with feather toy",
            duration_minutes=15,
            frequency="evening",
            priority=2,
            category="play",
            due_time="18:00",
            due_date=date.today(),
        )
    )

    scheduler = Scheduler(owner=owner)
    print("Unsorted pending tasks:")
    print(format_schedule(scheduler.get_all_pending_tasks()))

    print("\nSorted tasks by due date/time:")
    sorted_tasks = scheduler.sort_by_time(scheduler.get_all_pending_tasks())
    print(format_schedule(sorted_tasks))

    print("\nFiltered tasks for Mochi:")
    filtered_tasks = scheduler.filter_tasks(completed=False, pet_name="Mochi")
    print(format_schedule(filtered_tasks))

    print("\nConflict warnings:")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")

    print("\nGenerate today's plan:")
    plan = scheduler.generate_plan()
    print(format_schedule(plan))

    if plan:
        recurring = scheduler.mark_task_complete(plan[0])
        if recurring:
            print("\nRecurring task created:")
            print(format_schedule([recurring]))


if __name__ == "__main__":
    main()
