
class Owner {
    constructor(name, available_time, preferences = {}) {
        this.name = name;
        this.available_time = available_time;
        this.preferences = preferences;
        this.pets = [];
    }
    addPet(pet) {
        this.pets.push(pet);
    }
    removePet(pet) {
        this.pets = this.pets.filter(p => p !== pet);
    }
    getTotalAvailableTime() {
        return this.available_time;
    }
    updatePreferences(preferences) {
        this.preferences = preferences;
    }
    toString() {
        return `${this.name} (Available time: ${this.available_time})`;
    }
}

class Pet {
    constructor(name, species, age, special_needs = []) {
        this.name = name;
        this.species = species;
        this.age = age;
        this.special_needs = special_needs;
        this.tasks = [];
    }
    addTask(task) {
        this.tasks.push(task);
    }
    removeTask(task) {
        this.tasks = this.tasks.filter(t => t !== task);
    }
    getAllTasks() {
        return this.tasks;
    }
    getTotalCareTime() {
        return this.tasks.reduce((sum, task) => sum + task.duration, 0);
    }
    toString() {
        return `${this.name} (${this.species}, Age: ${this.age})`;
    }
}

class Task {
    constructor(name, duration, priority, category, frequency = "daily", preferred_time = null, is_flexible = true, notes = "") {
        this.name = name;
        this.duration = duration;
        this.priority = priority;
        this.category = category;
        this.frequency = frequency;
        this.preferred_time = preferred_time;
        this.is_flexible = is_flexible;
        this.notes = notes;
    }
    getPriority() {
        return this.priority;
    }
    getDuration() {
        return this.duration;
    }
    isHighPriority() {
        return this.priority >= 8;
    }
    canBeScheduledAt(time_slot) {
        return this.is_flexible || this.preferred_time === time_slot;
    }
    updateDetails({duration, priority, category, frequency, preferred_time, is_flexible, notes}) {
        if (duration !== undefined) this.duration = duration;
        if (priority !== undefined) this.priority = priority;
        if (category !== undefined) this.category = category;
        if (frequency !== undefined) this.frequency = frequency;
        if (preferred_time !== undefined) this.preferred_time = preferred_time;
        if (is_flexible !== undefined) this.is_flexible = is_flexible;
        if (notes !== undefined) this.notes = notes;
    }
    toString() {
        return `${this.name} (${this.category}, Priority: ${this.priority})`;
    }
}

class Scheduler {
    constructor(owner, strategy = "priority_first") {
        this.owner = owner;
        this.daily_plan = [];
        this.unscheduled_tasks = [];
        this.scheduling_strategy = strategy;
    }
    generateSchedule() {
        // Implementation goes here
    }
    _sortTasksByPriority() {
        // Implementation goes here
    }
    _calculateTotalTaskTime() {
        // Implementation goes here
    }
    _canFitAllTasks() {
        // Implementation goes here
    }
    _scheduleHighPriorityFirst() {
        // Implementation goes here
    }
    _optimizeByTimeBlocks() {
        // Implementation goes here
    }
    _handleConflicts() {
        // Implementation goes here
    }
    getSchedule() {
        return this.daily_plan;
    }
    getUnscheduledTasks() {
        return this.unscheduled_tasks;
    }
    explainSchedule() {
        // Implementation goes here
    }
    reschedule() {
        // Implementation goes here
    }
    exportSchedule(format) {
        // Implementation goes here
    }
    toString() {
        return `Scheduler for ${this.owner.name}`;
    }
}