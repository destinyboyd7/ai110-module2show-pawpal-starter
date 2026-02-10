"""
Docstring for main

"""
# Demo script for PawPal+
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    """
    Demo main function for PawPal+ system.
    """
    # Create an owner
    owner = Owner(name="Alex")

    # Create two pets
    pet1 = Pet(name="Buddy", species="Dog", age=5)
    pet2 = Pet(name="Mittens", species="Cat", age=3)

    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Add tasks to pets
    task1 = Task(description="Morning walk", time="07:30", frequency="daily")
    task2 = Task(description="Feed breakfast", time="08:00", frequency="daily")
    task3 = Task(description="Litter box cleaning", time="18:00", frequency="daily")

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Generate and print today's schedule
    print("Today's Schedule:")
    daily_schedule = scheduler.generate_daily_schedule()
    for pet_name, tasks in daily_schedule.items():
        print(f"\n{pet_name}:")
        if not tasks:
            print("  No tasks scheduled.")
        for task in tasks:
            print(f"  - {task.description} at {task.time}")

if __name__ == "__main__":
    main()
