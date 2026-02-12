# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Smart Scheduling 
Updated the schduler used on the pet care app to prioritize time. This allowed for sorting to occur so that no matter the order the task are inpputted it will be sorted by time correctly. Also, added conflict detetion method to avoid time conflicts for different tasks. 

## Testing PawPal+
command to run tests: python3 -m unittest tests/test_pawpal.py

I have about 11 different test the cover the most importnat edge cases for the per schduler. This includes task completion, task addition, sorting correctness, reoccurence of daily taks, conflict detection for the same and different pets, Edge time values. Moving into specific for the scheduler it was tested what it would do when it has no pet or tasks entered and make sure it returns empty when all task are completed. Last things it test for when if overude tasks were handled propely and how the ystem handles taks with unsupported frequency. My confinced in the system's reliability based on my test results are a 4 stars because all test passed very quickly but their could always be faults I am missing. 




## Features

- Recurring Task Scheduling: Automatically generates the next occurrence of daily, weekly, or monthly tasks when a task is marked complete.

- Task Completion Tracking: Allows marking tasks as complete or resetting their status to pending.

- Conflict Detection: Identifies scheduling conflicts for tasks that overlap in time, both within the same pet and across different pets.

- Overdue Task Identification: Detects and lists all tasks that are overdue and still pending.

- Task Filtering: Filters tasks by completion status and/or by pet name for easy management.

- Daily Schedule Generation: Produces a daily schedule for each pet, sorted by time, showing all pending daily tasks.

- Task Sorting: Sorts tasks by their scheduled time for organized viewing and scheduling.

- Multi-Pet Management: Supports managing multiple pets and their associated tasks under a single owner.

- Batch Task Completion: Allows marking multiple tasks as complete in a single operation.

## 📸 Demo

<a href= "/Users/destiny/IntroAI/ai110-module2show-pawpal-starter/PawPal_SS.png" target="_blank"><img src='/Users/destiny/IntroAI/ai110-module2show-pawpal-starter/PawPal_SS.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.


