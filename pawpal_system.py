"""

 docstring for pawpal_system

"""

# PawPal+ Pet Care Scheduling Application Skeleton
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

class Task:
    """
    Represents a single pet-related activity.
    """
    def __init__(
            self,
            description: str,
            time: str,
            frequency: str,
            completion_status: bool = False
        ):
        """Initialize a Task object."""
        self.description = description
        self.time = time
        self.frequency = frequency
        self.completion_status = completion_status

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completion_status = True

    def reset_status(self) -> None:
        """Reset this task's completion status to incomplete."""
        self.completion_status = False

    def __str__(self) -> str:
        """Return string representation of the task."""
        status = "Complete" if self.completion_status else "Pending"
        return (
            f"Task(description='{self.description}', time='{self.time}', "
            f"frequency='{self.frequency}', status='{status}')"
        )


class Pet:
    """
    Represents a pet with associated tasks.
    """
    def __init__(
            self,
            name: str,
            species: str,
            age: int
        ):
        """Initialize a Pet object."""
        self.name = name
        self.species = species
        self.age = age
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        if not isinstance(task, Task):
            raise TypeError("Can only add Task objects.")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        try:
            self.tasks.remove(task)
        except ValueError as exc:
            raise ValueError("Task not found in pet's task list.") from exc

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks.copy()

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending tasks for this pet."""
        return [task for task in self.tasks if not task.completion_status]

    def __str__(self) -> str:
        """Return string representation of the pet."""
        return (
            f"Pet(name='{self.name}', species='{self.species}', "
            f"age={self.age}, tasks={len(self.tasks)})"
        )


class Owner:
    """
    Manages multiple pets.
    """
    def __init__(self, name: str):
        """Initialize an Owner object."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        if not isinstance(pet, Pet):
            raise TypeError("Can only add Pet objects.")
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list."""
        try:
            self.pets.remove(pet)
        except ValueError as exc:
            raise ValueError("Pet not found in owner's list.") from exc

    def get_all_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets.copy()

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_all_tasks())
        return tasks

    def __str__(self) -> str:
        """Return string representation of the owner."""
        return (
            f"Owner(name='{self.name}', pets={len(self.pets)})"
        )

class Scheduler:
    """
    The central system that organizes and manages tasks.
    """
    def __init__(self, owner: Owner):
        """Initialize a Scheduler object."""
        self.owner = owner

    def get_tasks_by_frequency(self, frequency: str) -> List[Task]:
        """Return all tasks with the specified frequency."""
        return [task for task in self.owner.get_all_tasks() if task.frequency == frequency]

    def get_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks that are pending."""
        overdue = []
        now = datetime.now().strftime('%H:%M')
        for task in self.owner.get_all_tasks():
            if not task.completion_status and task.time < now:
                overdue.append(task)
        return overdue

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks for a specific pet by name."""
        for pet in self.owner.get_all_pets():
            if pet.name == pet_name:
                return pet.get_all_tasks()
        raise ValueError(f"Pet named '{pet_name}' not found.")

    def generate_daily_schedule(self) -> Dict[str, List[Task]]:
        """Generate a daily schedule mapping pet names to daily tasks."""
        schedule = {}
        for pet in self.owner.get_all_pets():
            daily_tasks = [
                task
                for task in pet.get_all_tasks()
                if (
                    task.frequency == "daily"
                    and not task.completion_status
                )
            ]
            schedule[pet.name] = daily_tasks
        return schedule

    def mark_tasks_complete(self, tasks: List[Task]) -> None:
        """Mark a list of tasks as complete."""
        for task in tasks:
            task.mark_complete()

    def __str__(self) -> str:
        """Return string representation of the scheduler."""
        return f"Scheduler(owner='{self.owner.name}')"
@dataclass
class TimeSlot:
    """Represents a block of time with a start and end datetime."""
    start: datetime
    end: datetime