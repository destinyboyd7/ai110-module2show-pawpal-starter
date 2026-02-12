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

My scheduler considers time and frequency of task such as daily, weekly, monthly. Time was prioritized the most beucase the schduler depends on it the most when tasks needs to occur and the avoid conflcit time overlaps of tasks. Frequency is another constraint I priotized because recurring routines are common with pets especially for feeding and walks so it would be important to owners as well. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

For readability and performance my scheduler largerly relies on time as its main constraint rather then priority or owner preference when generating the schedule. This tradeoff is reasonable becuase the main gola of the schduler is to ensure that all task are listed and do not overlap especilly is an owner has multiple pets. By focusing on the time, the schedule prioritizes simplicity of being easy to understand and maintain. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools to help largely with the implementation of the classes in pawpal_system.py. The prompts and questions that were most helpful was having the copilot explain why it chose to implement certain methods or debugging method. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I rejected AI suggestion when it came to building my UML becuase the file being in .js was effecting the outpout and preview in the Mermaid Live website. I also didn't accept certain suggestions for pawpal_system methods when it would use irrelevant variables. I evaluated by just using my own knowledge of my code and the objective of the project. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I the behaviors I tested for included 
task completion, task addition, sorting correctness, reoccurence of daily taks, conflict detection for the same and different pets, and Edge time values. Moving into specific for the scheduler it was tested what it would do when it has no pet or tasks entered and make sure it returns empty when all task are completed. Last things it test for when if overude tasks were handled propely and how the ystem handles taks with unsupported frequency. 

These were important to test for becuase they ensure readability and proper performance for the owner. By sorting and and dealing with tasks addidtions espceially with reccuring or empty tasks list. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am 80% confident in my schedulers ability to work correctly. If I had more time I would change time value from military to standard time and test edge cases for edge time value and sorting by time again becuase it would be dependet on am/pm selection. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satified with the frontend app.py portion. Just knowing that the backend fuctions were actually able to be connected to the fronted and work propelly to an extent. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add options for multiple owners especially for couples or families with pets in a household so that tasks can be split. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that while AI suggestions never truly hurt you. It is still important as a developer to know yurgoal and task. i already learned thatwith designing systems manyu things rely on one another to work so it's important to do your do diligence.