"""

 docstring for pawpal_system

"""

# PawPal+ Pet Care Scheduling Application Skeleton
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict

class Task:
    """
    Represents a single pet-related activity.
    """
    def __init__(
            self,
            description: str,
            time: str,
            frequency: str,
            completion_status: bool = False,
            parent_pet=None,
        ):
        """Initialize a Task object."""
        self.description = description
        self.time = time
        self.frequency = frequency
        self.completion_status = completion_status
        self.parent_pet = parent_pet


    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completion_status = True

        if self.frequency in ["daily", "weekly", "monthly"] and self.parent_pet is not None:
            self._create_next_occurrence()

    def _create_next_occurrence(self) -> None:
        """Create a new task instance for the next occurrence with updated date/time."""
        # Parse the current time (assume format 'HH:MM')
        try:
            now = datetime.now()
            task_time = datetime.strptime(self.time, '%H:%M')
            # Replace date with today for calculation
            task_time = task_time.replace(year=now.year, month=now.month, day=now.day)
        except ValueError:
            # If time format is not as expected, fallback to just copying
            task_time = now

        if self.frequency == "daily":
            next_time = task_time + timedelta(days=1)
        elif self.frequency == "weekly":
            next_time = task_time + timedelta(weeks=1)
        elif self.frequency == "monthly":
            # Add 1 month (approximate as 30 days)
            next_time = task_time + timedelta(days=30)
        else:
            next_time = task_time

        # Format back to 'HH:MM' for time field
        new_time_str = next_time.strftime('%H:%M')
        new_task = Task(
            description=self.description,
            time=new_time_str,
            frequency=self.frequency,
            parent_pet=self.parent_pet
        )
        self.parent_pet.add_task(new_task)

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
        #set parent_pet reference for task
        task.parent_pet = self
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
    Manages scheduling for an owner's pets.
    """

    def __init__(self, owner: Owner):
        """Initialize a Scheduler object."""
        self.owner = owner

    def conflict_warnings(self) -> List[str]:
        """
        Lightweight conflict detection.
        Returns warnings for scheduling conflicts.
        """
        warnings = []
        conflicts = self.detect_conflicts()
        for time, conflict_groups in conflicts.items():
            for group in conflict_groups:
                pet_names = {getattr(t.parent_pet, 'name', None) for t in group}
                task_descriptions = ', '.join(t.description for t in group)
                if len(pet_names) == 1:
                    pet_name = next(iter(pet_names))
                    warnings.append(
                        (
                            f"Warning: {len(group)} tasks for pet '{pet_name}'"
                            f" are scheduled at {time}: {task_descriptions}"
                        )

                    )
                else:
                    warnings.append(
                        (
                             f"Warning: Tasks for multiple pets ({', '.join(pet_names)})"
                             f"are scheduled at {time}: {task_descriptions}"
                        )

                    )
        return warnings

    def detect_conflicts(self) -> Dict[str, List[List[Task]]]:
        """
        Detects and returns scheduling conflicts for all pets.
        Returns a dict mapping time strings to lists of conflicting Task objects.
        Example: { '08:00': [ [Task1, Task2], [Task3, Task4] ] }
        """
        all_tasks = self.owner.get_all_tasks()
        time_pet_map = defaultdict(list)
        time_map = defaultdict(list)
        for task in all_tasks:
            if not task.completion_status:
                time_pet_map[(task.time, getattr(task.parent_pet, 'name', None))].append(task)
                time_map[task.time].append(task)

        conflicts = defaultdict(list)
        # Same-pet conflicts
        for (time), tasks in time_pet_map.items():
            if len(tasks) > 1:
                conflicts[time].append(tasks)
        # Cross-pet conflicts
        for time, tasks in time_map.items():
            pet_names = {getattr(t.parent_pet, 'name', None) for t in tasks}
            if len(tasks) > 1 and len(pet_names) > 1:
                conflicts[time].append(tasks)
        return dict(conflicts)

    def get_tasks_by_frequency(self, frequency: str) -> List[Task]:
        """Return all tasks with the specified frequency."""
        return [task for task in self.owner.get_all_tasks() if task.frequency == frequency]

    def get_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks that are pending."""
        now = datetime.now().strftime('%H:%M')
        return [
            task for task in self.owner.get_all_tasks()
            if not task.completion_status and task.time < now
        ]

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks for a specific pet by name."""
        for pet in self.owner.get_all_pets():
            if pet.name == pet_name:
                return pet.get_all_tasks()
        raise ValueError(f"Pet named '{pet_name}' not found.")

    def generate_daily_schedule(self) -> Dict[str, List[Task]]:
        """Generate a daily schedule mapping pet names to daily tasks."""
        return {
            pet.name: self.sort_by_time([
                task for task in pet.get_all_tasks()
                if task.frequency == "daily" and not task.completion_status
            ])
            for pet in self.owner.get_all_pets()
        }

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return a list of Task objects sorted by their time attribute (HH:MM)."""
        return sorted(tasks, key=lambda task: task.time)

    def mark_tasks_complete(self, tasks: List[Task]) -> None:
        """Mark a list of tasks as complete."""
        for task in tasks:
            task.mark_complete()

    def filter_tasks(
        self,
        completion_status: bool = None,
        pet_name: str = None
    ) -> List[Task]:
        """
        Filter tasks by completion status and/or pet name.
        If a filter is None, it is ignored.
        """
        if pet_name is not None:
            tasks = [
                task for pet in self.owner.get_all_pets() if pet.name == pet_name
                for task in pet.get_all_tasks()
            ]
        else:
            tasks = self.owner.get_all_tasks()
        if completion_status is not None:
            tasks = [task for task in tasks if task.completion_status == completion_status]
        return tasks

    def __str__(self) -> str:
        """Return string representation of the scheduler."""
        return f"Scheduler(owner='{self.owner.name}')"

@dataclass
class TimeSlot:
    """Represents a block of time with a start and end datetime."""
    start: datetime
    end: datetime