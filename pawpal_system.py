from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str = "once"
    completed: bool = False
    priority: int = 1
    category: Optional[str] = None
    due_time: Optional[str] = None
    due_date: Optional[date] = None
    pet_name: Optional[str] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next recurring instance if needed."""
        self.completed = True
        frequency = self.frequency.lower()
        if frequency not in {"daily", "weekly"}:
            return None

        next_date = (self.due_date or date.today()) + (
            timedelta(days=1) if frequency == "daily" else timedelta(weeks=1)
        )

        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            completed=False,
            priority=self.priority,
            category=self.category,
            due_time=self.due_time,
            due_date=next_date,
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        if task.pet_name is None:
            task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        """Remove a task by description and return whether it was removed."""
        for task in self.tasks:
            if task.description == description:
                self.tasks.remove(task)
                return True
        return False

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """Return only incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name and return whether it was removed."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                return True
        return False

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return a pet matching the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for every pet owned by this owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across every pet."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_pending_tasks())
        return tasks


class Scheduler:
    FREQUENCY_ORDER = {
        "daily": 1,
        "morning": 2,
        "afternoon": 3,
        "evening": 4,
        "once": 5,
        "weekly": 6,
        "as needed": 7,
    }

    def __init__(self, owner: Owner):
        """Create a scheduler for the given owner."""
        self.owner = owner

    def add_task_to_pet(self, pet_name: str, task: Task) -> bool:
        """Add a new task to a specific pet by name."""
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return False
        pet.add_task(task)
        return True

    def get_all_tasks(self) -> List[Task]:
        """Retrieve every task for every pet owned by the owner."""
        return self.owner.get_all_tasks()

    def get_all_pending_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks from the owner and pets."""
        return self.owner.get_all_pending_tasks()

    def _parse_time_to_minutes(self, due_time: Optional[str]) -> int:
        """Convert an HH:MM due_time string into total minutes."""
        if not due_time:
            return 24 * 60
        try:
            hours, minutes = [int(part) for part in due_time.split(":")]
            return hours * 60 + minutes
        except ValueError:
            return 24 * 60

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by due date, due time, then frequency and priority."""
        tasks = tasks or self.get_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                task.due_date or date.max,
                self._parse_time_to_minutes(task.due_time),
                self.FREQUENCY_ORDER.get(task.frequency.lower(), 99),
                task.priority,
            ),
        )

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]
        return tasks

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and create the next recurring instance if applicable."""
        recurrence = task.mark_complete()
        if recurrence and task.pet_name:
            self.add_task_to_pet(task.pet_name, recurrence)
        return recurrence

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Detect tasks scheduled at the same date and time."""
        tasks = tasks or self.get_all_tasks()
        conflict_map = {}
        for task in tasks:
            if task.due_date is None or task.due_time is None:
                continue
            key = (task.due_date, task.due_time)
            conflict_map.setdefault(key, []).append(task)

        warnings: List[str] = []
        for (due_date, due_time), grouped in conflict_map.items():
            if len(grouped) > 1:
                items = ", ".join(
                    f"{task.pet_name or 'Unknown pet'}:{task.description}" for task in grouped
                )
                warnings.append(
                    f"Conflict on {due_date} at {due_time} between tasks: {items}"
                )
        return warnings

    def generate_plan(self) -> List[Task]:
        """Build a schedule from pending tasks within available minutes."""
        available = self.owner.available_minutes
        ordered_tasks = self.sort_by_time(self.get_all_pending_tasks())
        plan: List[Task] = []

        for task in ordered_tasks:
            if task.duration_minutes <= available:
                plan.append(task)
                available -= task.duration_minutes

        return plan

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        plan = self.generate_plan()
        warnings = self.detect_conflicts(plan)
        if not plan:
            return f"No pending tasks can fit into {self.owner.available_minutes} available minutes."

        lines = [f"Plan for {self.owner.name}: {len(plan)} tasks scheduled."]
        if warnings:
            lines.append("Warnings:")
            lines.extend(f"- {warning}" for warning in warnings)
        for task in plan:
            lines.append(
                f"- {task.description} ({task.duration_minutes}m, {task.frequency}, priority {task.priority})"
            )

        return "\n".join(lines)
