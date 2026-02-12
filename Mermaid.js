classDiagram
    class Owner {
        constructor(name) {
            this.name = name;
            this.pets = [];
        }
        add_pet(pet) {
            if (!(pet instanceof Pet)) throw new TypeError("Can only add Pet objects.");
            this.pets.push(pet);
        }
        remove_pet(pet) {
            this.pets = this.pets.filter(p => p !== pet);
        }
        get_all_pets() {
            return [...this.pets];
        }
        get_all_tasks() {
            let tasks = [];
            for (const pet of this.pets) {
                tasks = tasks.concat(pet.get_all_tasks());
            }
            return tasks;
        }
        toString() {
            return `Owner(name='${this.name}', pets=${this.pets.length})`;
        }
    }

    class Pet {
        constructor(name, species, age) {
            this.name = name;
            this.species = species;
            this.age = age;
            this.tasks = [];
        }
        add_task(task) {
            if (!(task instanceof Task)) throw new TypeError("Can only add Task objects.");
            task.parent_pet = this;
            this.tasks.push(task);
        }
        remove_task(task) {
            this.tasks = this.tasks.filter(t => t !== task);
        }
        get_all_tasks() {
            return [...this.tasks];
        }
        get_pending_tasks() {
            return this.tasks.filter(task => !task.completion_status);
        }
        toString() {
            return `Pet(name='${this.name}', species='${this.species}', age=${this.age}, tasks=${this.tasks.length})`;
        }
    }

    class Task {
        constructor(description, time, frequency, completion_status = false, parent_pet = null) {
            this.description = description;
            this.time = time;
            this.frequency = frequency;
            this.completion_status = completion_status;
            this.parent_pet = parent_pet;
        }
        mark_complete() {
            this.completion_status = true;
            if (["daily", "weekly", "monthly"].includes(this.frequency) && this.parent_pet) {
                this._create_next_occurrence();
            }
        }
        _create_next_occurrence() {
            // Implementation: create a new Task for the next occurrence and add to parent_pet
        }
        reset_status() {
            this.completion_status = false;
        }
        toString() {
            const status = this.completion_status ? "Complete" : "Pending";
            return `Task(description='${this.description}', time='${this.time}', frequency='${this.frequency}', status='${status}')`;
        }
    }

    class Scheduler {
        constructor(owner) {
            this.owner = owner;
        }
        conflict_warnings() {}
        detect_conflicts() {}
        get_tasks_by_frequency(frequency) {}
        get_overdue_tasks() {}
        get_tasks_for_pet(pet_name) {}
        generate_daily_schedule() {}
        sort_by_time(tasks) {}
        mark_tasks_complete(tasks) {}
        filter_tasks(completion_status = null, pet_name = null) {}
        toString() {
            return `Scheduler(owner='${this.owner.name}')`;
        }
    }

    // Standalone TimeSlot dataclass (not used in main relationships)
    class TimeSlot {
        constructor(start, end) {
            this.start = start;
            this.end = end;
        }
    }

/*
classDiagram
    class Owner {
        -string name
        -List~Pet~ pets
        +__init__(name: string)
        +add_pet(pet: Pet) void
        +remove_pet(pet: Pet) void
        +get_all_pets() List~Pet~
        +get_all_tasks() List~Task~
        +__str__() string
    }

    class Pet {
        -string name
        -string species
        -int age
        -List~Task~ tasks
        +__init__(name: string, species: string, age: int)
        +add_task(task: Task) void
        +remove_task(task: Task) void
        +get_all_tasks() List~Task~
        +get_pending_tasks() List~Task~
        +__str__() string
    }

    class Task {
        -string description
        -string time
        -string frequency
        -bool completion_status
        -Pet parent_pet
        +__init__(description: string, time: string, frequency: string, completion_status: bool, parent_pet: Pet)
        +mark_complete() void
        -_create_next_occurrence() void
        +reset_status() void
        +__str__() string
    }

    class Scheduler {
        -Owner owner
        +__init__(owner: Owner)
        +conflict_warnings() List~string~
        +detect_conflicts() Dict~string, List~List~Task~~~
        +get_tasks_by_frequency(frequency: string) List~Task~
        +get_overdue_tasks() List~Task~
        +get_tasks_for_pet(pet_name: string) List~Task~
        +generate_daily_schedule() Dict~string, List~Task~~
        +sort_by_time(tasks: List~Task~) List~Task~
        +mark_tasks_complete(tasks: List~Task~) void
        +filter_tasks(completion_status: bool, pet_name: string) List~Task~
        +__str__() string
    }

    class TimeSlot {
        +datetime start
        +datetime end
    }

    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Task "*" --> "0..1" Pet : parent_pet
    Scheduler "1" --> "1" Owner : manages
*/