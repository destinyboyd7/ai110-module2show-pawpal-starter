"""
PawPal+ Streamlit app"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

#Initialize Owner in session state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.subheader("Owner Information")
st.write(f"**Owner:** {owner.name}")
st.write(f"**Total Pets:** {len(owner.pets)}")

st.divider()

st.subheader("Add a Pet")
col1,  col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3, key="new_pet_age")

if st.button("Add Pet"):
    # Create Pet object and add to Owner
    new_pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(new_pet)
    st.success(f"✅ Added {pet_name} ({species}, age {age}) to {owner.name}'s pets!")
    st.rerun()

#Display current pets
if owner.pets:
    st.write("### Current Pets:")
    for pet in owner.get_all_pets():
        st.write(f"- {pet.name} ({pet.species}, {pet.age} years old) - {len(pet.tasks)} tasks")
else:
    st.info("No pets yet. Add one above.")

st.divider()


st.subheader("Add Tasks for a Pet")
st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if owner.pets:
    # Select which pet to add task to
    pet_names = [pet.name for pet in owner.get_all_pets()]
    selected_pet_name = st.selectbox("Select Pet", pet_names, key="task_pet_select")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task description", value="Morning walk",
                                         key="new_task_desc"
                                        )
    with col2:
        task_time = st.time_input("Time", key="new_task_time")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"],
                                 index=0, key="new_task_freq")

    if st.button("Add Task"):
        # Find the selected pet
        SELECTED_PET = None
        for pet in owner.get_all_pets():
            if pet.name == selected_pet_name:
                SELECTED_PET = pet
                break

        if SELECTED_PET:
            # Create Task object and add to Pet
            new_task = Task(
                description=task_description,
                time=task_time.strftime('%H:%M'),
                frequency=frequency
            )
            SELECTED_PET.add_task(new_task)
            st.success(f"✅ Added task '{task_description}' to {selected_pet_name}!")
            st.rerun()
else:
    st.warning("⚠️ Add a pet first before creating tasks.")

st.divider()

st.subheader("All Tasks")
if owner.pets:
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        for pet in owner.get_all_pets():
            st.write(f"**{pet.name}'s Tasks:**")
            pet_tasks = pet.get_all_tasks()
            if pet_tasks:
                for task in pet_tasks:
                    STATUS_ICON = "✅" if task.completion_status else "⏳"
                    st.write(f"{STATUS_ICON} {task.description} - {task.time} ({task.frequency})")
            else:
                st.write("  No tasks yet")
    else:
        st.info("No tasks created yet.")
else:
    st.info("Add pets and tasks to see them here.")

st.divider()

# ============ GENERATE SCHEDULE ============
st.subheader("Build Schedule")
st.caption("Generate a daily schedule for all your pets.")

if st.button("Generate Daily Schedule"):
    if not owner.pets:
        st.warning("⚠️ Please add at least one pet first.")
    else:
        # Create Scheduler and generate schedule
        scheduler = Scheduler(owner=owner)
        daily_schedule = scheduler.generate_daily_schedule()

        if any(daily_schedule.values()):
            st.success("📅 Daily Schedule Generated!")
            for pet_name, tasks in daily_schedule.items():
                if tasks:
                    st.write(f"### {pet_name}'s Daily Tasks:")
                    # Sort tasks by time
                    sorted_tasks = sorted(tasks, key=lambda t: t.time)
                    for task in sorted_tasks:
                        st.write(f"- **{task.time}**: {task.description}")
                else:
                    st.write(f"### {pet_name}: No pending daily tasks")
        else:
            st.info("No daily tasks found. Add some tasks with 'daily' frequency!")



"""

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your " \
        "scheduling logic (classes/functions) and call it here."
    )
    st.markdown(

Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.

    )

"""