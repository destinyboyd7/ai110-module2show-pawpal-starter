# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform: 
    Add Pet Profile 
    Owner Availabiltiy 
    Hourly/Daily Planner 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My intial UML design includes an Owner owns multiple Pet profiles; each Pet has many Task entries; a Scheduler takes an Owner and the Pets' Tasks and produces a daily plan, handling priorities, time constraints and conflicts. My include classes were the Owner, Pet, Task, and Scheduler. The assigned responsibilities are as listed below:

    Owner:
        - manage pet list, report total available time, update owner preferences
    Pet:
        - hold pet data, add/remove tasks, compute total care time
    Task:
        - represent a schedulable unit, expose duration/priority, check schedulability, comparison for ordering
    Scheduler:
        - generate and optimize schedules, sort/prioritize tasks, detect/resolve conflicts, reschedule, export and explain the resulting plan


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes my design changed during implemetation. there were missing relationships related to task ownership and the direct connection between scheduler and task. The logic bottlenecks were task aggregation, conflict resoultion, updating relationships, and scalability. One change I made was adding a flat list of all the task to the scheduler. I made this schnage so that the owner could have easier acess to the task. Each task also was change to refernce its specifc pet and each pet references its owner. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
