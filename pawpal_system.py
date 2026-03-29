from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Owner:
    name: str
    available_minutes: int = 0


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: int
    category: str
    preferred_time: Optional[str] = None


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: Optional[List[Task]] = None):
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = tasks or []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass

    def generate_plan(self):
        """Generate a daily care plan from the current tasks."""
        pass

    def explain_plan(self):
        """Explain the generated plan and the reasoning behind it."""
        pass
