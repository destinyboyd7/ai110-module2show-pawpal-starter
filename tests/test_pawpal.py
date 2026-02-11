"""
Docstring for tests.test_pawpal
"""

import unittest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestPawPal(unittest.TestCase):
    """
    Docstring for TestPawPal
    """
    def test_task_completion(self):
        """
        Docstring for test_task_completion

        """
        task = Task(description="Feed", time="08:00", frequency="daily")
        self.assertFalse(task.completion_status)
        task.mark_complete()
        self.assertTrue(task.completion_status)

    def test_task_addition(self):
        """
        Docstring for test_task_addition
        
        """
        pet = Pet(name="Buddy", species="Dog", age=3)
        initial_count = len(pet.get_all_tasks())
        task = Task(description="Walk", time="09:00", frequency="daily")
        pet.add_task(task)
        self.assertEqual(len(pet.get_all_tasks()), initial_count + 1)

    def test_sorting_correctness(self):
        """Verify tasks are returned in chronological order."""
        pet = Pet(name="Milo", species="Cat", age=2)
        times = ["15:00", "08:00", "12:30"]
        for t in times:
            pet.add_task(Task(description=f"Task at {t}", time=t, frequency="daily"))
        owner = Owner(name="Alex")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_time(pet.get_all_tasks())
        sorted_times = [task.time for task in sorted_tasks]
        self.assertEqual(sorted_times, sorted(times))

    def test_recurrence_logic_daily(self):
        """Confirm marking a daily task complete creates a new task for the following day."""
        pet = Pet(name="Luna", species="Dog", age=4)
        task = Task(description="Feed", time="07:00", frequency="daily")
        pet.add_task(task)
        initial_task_count = len(pet.get_all_tasks())
        task.mark_complete()
        self.assertTrue(task.completion_status)
        self.assertEqual(len(pet.get_all_tasks()), initial_task_count + 1)
        # Check that the new task is for the next day (time remains the same)
        new_task = pet.get_all_tasks()[-1]
        self.assertEqual(new_task.description, "Feed")
        self.assertEqual(new_task.time, "07:00")
        self.assertFalse(new_task.completion_status)

    def test_conflict_detection_same_pet(self):
        """Verify Scheduler flags duplicate times for the same pet."""
        pet = Pet(name="Max", species="Dog", age=5)
        task1 = Task(description="Walk", time="10:00", frequency="daily")
        task2 = Task(description="Feed", time="10:00", frequency="daily")
        pet.add_task(task1)
        pet.add_task(task2)
        owner = Owner(name="Sam")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        warnings = scheduler.conflict_warnings()
        self.assertTrue(any("Max" in w and "10:00" in w for w in warnings))

    def test_conflict_detection_cross_pet(self):
        """Verify Scheduler flags duplicate times for different pets."""
        pet1 = Pet(name="Bella", species="Cat", age=3)
        pet2 = Pet(name="Charlie", species="Dog", age=2)
        task1 = Task(description="Feed", time="08:30", frequency="daily")
        task2 = Task(description="Walk", time="08:30", frequency="daily")
        pet1.add_task(task1)
        pet2.add_task(task2)
        owner = Owner(name="Taylor")
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        scheduler = Scheduler(owner)
        warnings = scheduler.conflict_warnings()
        self.assertTrue(any("Bella" in w and "Charlie" in w and "08:30" in w for w in warnings))

    def test_edge_time_values(self):
        """Test tasks at edge times and invalid time format."""
        pet = Pet(name="Edge", species="Dog", age=1)
        task1 = Task(description="Midnight", time="00:00", frequency="daily")
        task2 = Task(description="Last Minute", time="23:59", frequency="daily")
        pet.add_task(task1)
        pet.add_task(task2)
        owner = Owner(name="Morgan")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_by_time(pet.get_all_tasks())
        self.assertEqual(sorted_tasks[0].time, "00:00")
        self.assertEqual(sorted_tasks[-1].time, "23:59")
        # Invalid time should not raise error on creation, but may affect sorting
        task_invalid = Task(description="Invalid", time="notatime", frequency="daily")
        pet.add_task(task_invalid)
        try:
            scheduler.sort_by_time(pet.get_all_tasks())
        except Exception as e:
            self.fail(f"Sorting failed with invalid time: {e}")

    def test_no_pets_no_tasks(self):
        """Scheduler handles no pets and no tasks gracefully."""
        owner = Owner(name="Jamie")
        scheduler = Scheduler(owner)
        #self.assertEqual(scheduler.get_all_tasks(), [])
        self.assertEqual(scheduler.generate_daily_schedule(), {})

    def test_all_tasks_completed(self):
        """Scheduler returns empty for all completed tasks."""
        pet = Pet(name="Done", species="Cat", age=2)
        task = Task(description="Nap", time="14:00", frequency="daily")
        pet.add_task(task)
        task.mark_complete()
        owner = Owner(name="Alexis")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        # There should be one new incomplete recurring task
        incomplete_tasks = scheduler.filter_tasks(completion_status=False)
        self.assertEqual(len(incomplete_tasks), 1)
        self.assertEqual(incomplete_tasks[0].description, "Nap")
        self.assertEqual(incomplete_tasks[0].time, "14:00")
        self.assertFalse(incomplete_tasks[0].completion_status)

    def test_overdue_tasks(self):
        """Correctly identifies overdue tasks."""
        pet = Pet(name="Late", species="Dog", age=3)
        # Set a time that is guaranteed to be before now (e.g., "00:01")
        task = Task(description="Early Walk", time="00:01", frequency="daily")
        pet.add_task(task)
        owner = Owner(name="Pat")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        overdue = scheduler.get_overdue_tasks()
        self.assertTrue(any(t.description == "Early Walk" for t in overdue))

    def test_invalid_frequency(self):
        """System handles tasks with unsupported frequency."""
        pet = Pet(name="Odd", species="Cat", age=1)
        task = Task(description="Mystery", time="10:00", frequency="yearly")
        pet.add_task(task)
        owner = Owner(name="Chris")
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        # Should not crash, and task should be present
        self.assertIn(task, scheduler.get_tasks_by_frequency("yearly"))

if __name__ == "__main__":
    unittest.main()