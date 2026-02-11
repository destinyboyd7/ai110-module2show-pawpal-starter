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
    task1= Task(description="Evening walk", time="18:00", frequency="daily")
    task2 = Task(description="Feed breakfast", time="08:00", frequency="daily")
    task3 = Task(description="Morning walk", time="07:30", frequency="daily")
    task4 = Task(description="Playtime", time="15:00", frequency="weekly")
    task5 = Task(description="Vet appointment", time="14:00", frequency="monthly")


    task6 = Task(description="Litter box cleaning", time="18:00", frequency="weekly")
    task7 = Task(description="Feed breakfast", time="08:00", frequency="daily")
    task8 = Task(description="Grooming", time="14:00", frequency="monthly")

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task4)
    pet1.add_task(task5)
    pet1.add_task(task3)

    # Add two tasks at the same time for different pets
    # task1 (Buddy, 18:00) and task6 (Mittens, 18:00)
    # task5 (Buddy, 14:00) and task8 (Mittens, 14:00)

    pet2.add_task(task6)
    pet2.add_task(task7)
    pet2.add_task(task8)



    # Create scheduler
    scheduler = Scheduler(owner)

    # Print conflict warnings
    print("\n" + "=" * 50)
    print("Conflict Warnings:")
    print("=" * 50)
    warnings = scheduler.conflict_warnings()
    if not warnings:
        print("No conflicts detected.")
    else:
        for w in warnings:
            print(w)

    # Generate and print today's schedule
    print("=" * 50)
    print("Today's Schedule:")
    print("=" * 50)
    daily_schedule = scheduler.generate_daily_schedule()
    for pet_name, tasks in daily_schedule.items():
        print(f"\n{pet_name}:")
        if not tasks:
            print("  No tasks scheduled.")
        for task in tasks:
            print(f"  - {task.description} at {task.time}")

    # Test filtering by frequency
    print("\n" + "=" * 50)
    print("Daily Tasks:")
    print("=" * 50)
    for pet_name, tasks in daily_schedule.items():
        daily_tasks = [t for t in tasks if t.frequency == "daily"]
        if daily_tasks:
            print(f"\n{pet_name}:")
            for task in daily_tasks:
                print(f"  - {task.time} at {task.description}")

    print("\n" + "=" * 50)
    print("Weekly Tasks:")
    print("=" * 50)
    for pet_name, tasks in daily_schedule.items():
        weekly_tasks = [t for t in tasks if t.frequency == "weekly"]
        if weekly_tasks:
            print(f"\n{pet_name}:")
            for task in weekly_tasks:
                print(f"  - {task.time} at {task.description}")

    # Test sorting by demonstration
    print("\n" + "=" * 50)
    print("Buddy's Tasks Sorted by Time:")
    print("=" * 50)
    print("\nBefore explicit sorting:")
    buddy_tasks = daily_schedule["Buddy"]
    for task in buddy_tasks:
        print(f"  - {task.time} at {task.description}")

    print("\nMorning tasks only:")
    morning_tasks = [t for t in buddy_tasks if t.time < "12:00"]
    for task in morning_tasks:
        print(f"  - {task.time} at {task.description}")

if __name__ == "__main__":
    main()
