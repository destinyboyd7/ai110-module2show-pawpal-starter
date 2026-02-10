"""
Docstring for tests.test_pawpal
"""

import unittest
from pawpal_system import Task, Pet


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

if __name__ == "__main__":
    unittest.main()