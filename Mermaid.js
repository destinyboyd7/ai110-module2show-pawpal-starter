classDiagram
    class Owner {
        +name: string
        +available_time: int
        +preferences: dict
        +pets: list~Pet~
        +__init__(name, available_time, preferences=None)
        +add_pet(pet)
        +remove_pet(pet)
        +get_total_available_time()
        +update_preferences(preferences)
        +__str__()
    }

    class Pet {
        +name: string
        +species: string
        +age: int
        +special_needs: list~string~
        +tasks: list~Task~
        +__init__(name, species, age, special_needs=None)
        +add_task(task)
        +remove_task(task)
        +get_all_tasks()
        +get_total_care_time()
        +__str__()
    }

    class Task {
        +name: string
        +duration: int
        +priority: int
        +category: string
        +frequency: string
        +preferred_time: string
        +is_flexible: bool
        +notes: string
        +__init__(name, duration, priority, category, frequency="daily", preferred_time=None, is_flexible=True, notes="")
        +get_priority()
        +get_duration()
        +is_high_priority()
        +can_be_scheduled_at(time_slot)
        +update_details(duration, priority, category, ...)
        +__str__()
        +__lt__(other)
    }

    class Scheduler {
        +owner: Owner
        +daily_plan: list~dict~
        +unscheduled_tasks: list~Task~
        +scheduling_strategy: string
        +__init__(owner, strategy="priority_first")
        +generate_schedule()
        +_sort_tasks_by_priority()
        +_calculate_total_task_time()
        +_can_fit_all_tasks()
        +_schedule_high_priority_first()
        +_optimize_by_time_blocks()
        +_handle_conflicts()
        +get_schedule()
        +get_unscheduled_tasks()
        +explain_schedule()
        +reschedule()
        +export_schedule(format)
        +__str__()
    }

    Owner "1" *-- "0..*" Pet : owns
    Pet "1" *-- "0..*" Task : has
    Scheduler "1" --> "1" Owner : schedules for
    Scheduler "1" ..> "0..*" Task : manages