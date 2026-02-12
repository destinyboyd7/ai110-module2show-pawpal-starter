"""
PawPal+ Streamlit app"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

"""
)

#Initialize Owner in session state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner
scheduler = Scheduler(owner=owner)


#owner info
st.subheader("Owner Information")
col1, col2 = st.columns(2)
with col1:
    st.metric("Owner Name", owner.name)
with col2:
    st.metric("Number of Pets", len(owner.pets))
st.divider()

#Add a pet
st.subheader("Add a Pet")
col1,  col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "other"], key="new_pet_species")
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3, key="new_pet_age")

if st.button("Add Pet"):
    # Create Pet object and add to Owner
    new_pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name} ({species}, age {age}) to {owner.name}'s pets!")
    st.rerun()

if owner.pets:
    st.write("### Current Pets:")
    for pet in owner.get_all_pets():
        pending_count = len(pet.get_all_tasks())
        completed_count = len([t for t in pet.get_all_tasks() if t.completion_status])
        st.write(
            (
                f"- {pet.name} ({pet.species}, {pet.age} years old) - "
                f" {pending_count} pending, {completed_count} completed"
            )
        )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# Add tasks for a pet
st.subheader("📝 Add Tasks for a Pet")

if owner.pets:
    pet_names = [pet.name for pet in owner.get_all_pets()]
    selected_pet_name = st.selectbox("Select Pet", pet_names, key="task_pet_select")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input(
            "Task description",
            value="Morning walk",
            key="new_task_desc")
    with col2:
        task_time = st.time_input("Time", key="new_task_time")
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"],
                                 index=0, key="new_task_freq")

    if st.button("Add Task", type="primary"):
        SELECTED_PET = None
        for pet in owner.get_all_pets():
            if pet.name == selected_pet_name:
                SELECTED_PET = pet
                break

        if SELECTED_PET:
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

# view all tasks
st.subheader("📋 All Tasks")

if owner.pets:
    # Filtering options
    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox(
            "Filter by Pet",
            ["All Pets"] + [pet.name for pet in owner.get_all_pets()],
            key="filter_pet"
        )
    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Completed"],
            key="filter_status"
        )

    # Apply filters
    if filter_pet == "All Pets":
        filtered_tasks = owner.get_all_tasks()
        DISPLAY_BY_PET = True
    else:
        filtered_tasks = scheduler.filter_tasks(pet_name=filter_pet)
        DISPLAY_BY_PET = False

    if filter_status == "Pending":
        filtered_tasks = [t for t in filtered_tasks if not t.completion_status]
    elif filter_status == "Completed":
        filtered_tasks = [t for t in filtered_tasks if t.completion_status]

    # Sort tasks by time
    sorted_tasks = scheduler.sort_by_time(filtered_tasks)

    if sorted_tasks:
        if DISPLAY_BY_PET:
            # Group by pet
            for pet in owner.get_all_pets():
                pet_tasks = [t for t in sorted_tasks if t.parent_pet == pet]
                if pet_tasks:
                    st.write(f"**{pet.name}'s Tasks:**")
                    for task in pet_tasks:
                        STATUS_ICON = "✅" if task.completion_status else "⏳"
                        col1, col2, col3 = st.columns([1, 3, 1])
                        with col1:
                            st.write(f"{STATUS_ICON} **{task.time}**")
                        with col2:
                            st.write(f"{task.description} ({task.frequency})")
                        with col3:
                            if not task.completion_status:
                                if st.button("✓ Complete", key=f"complete_{id(task)}"):
                                    task.mark_complete()
                                    st.success(
                                        (
                                            f"Task '{task.description}' "
                                            f" completed! Next occurrence created."
                                        )
                                    )
                                    st.rerun()
                    st.write("")
        else:
            # Single pet view
            st.write(f"**{filter_pet}'s Tasks:**")
            for task in sorted_tasks:
                STATUS_ICON = "✅" if task.completion_status else "⏳"
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.write(f"{STATUS_ICON} **{task.time}**")
                with col2:
                    st.write(f"{task.description} ({task.frequency})")
                with col3:
                    if not task.completion_status:
                        if st.button("✓ Complete", key=f"complete_{id(task)}"):
                            task.mark_complete()
                            st.success(
                                (f"Task '{task.description}' completed! Next occurrence created.")
                            )
                            st.rerun()
    else:
        st.info("No tasks match your filters.")
else:
    st.info("Add pets and tasks to see them here.")

st.divider()

# conflict warnings
st.subheader("⚠️ Conflict Detection")

if owner.pets and owner.get_all_tasks():
    warnings = scheduler.conflict_warnings()
    if warnings:
        st.warning("**Scheduling Conflicts Detected:**")
        for warning in warnings:
            st.write(f"• {warning}")
    else:
        st.success("✅ No scheduling conflicts detected!")
else:
    st.info("Add tasks to check for conflicts.")

st.divider()

# generate daily schedule
st.subheader("📅 Daily Schedule")

col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Daily Schedule", type="primary"):
        if not owner.pets:
            st.warning("⚠️ Please add at least one pet first.")
        else:
            daily_schedule = scheduler.generate_daily_schedule()

            if any(daily_schedule.values()):
                st.success("📅 Daily Schedule Generated!")

                # Create a professional table view
                for pet_name, tasks in daily_schedule.items():
                    if tasks:
                        st.write(f"### {pet_name}'s Daily Tasks:")

                        # Create data for table
                        table_data = []
                        for task in tasks:
                            table_data.append({
                                "Time": task.time,
                                "Task": task.description,
                                "Frequency": task.frequency,
                                "Status": "✅ Complete" if task.completion_status else "⏳ Pending"
                            })

                        st.table(table_data)
                    else:
                        st.write(f"### {pet_name}: No pending daily tasks")
            else:
                st.info("No daily tasks found. Add some tasks with 'daily' frequency!")

with col2:
    if st.button("Show Overdue Tasks"):
        overdue_tasks = scheduler.get_overdue_tasks()
        if overdue_tasks:
            st.warning(f"⚠️ {len(overdue_tasks)} Overdue Tasks Found!")
            sorted_overdue = scheduler.sort_by_time(overdue_tasks)
            for task in sorted_overdue:
                st.write(
                    ( f"• **{task.time}** - {task.description} "
                     f"({task.parent_pet.name if task.parent_pet else 'Unknown'})"
                    )
                )
        else:
            st.success("✅ No overdue tasks!")

st.divider()

# task statistics
st.subheader("📊 Task Statistics")

if owner.get_all_tasks():
    col1, col2, col3 = st.columns(3)

    all_tasks = owner.get_all_tasks()
    pending_tasks = [t for t in all_tasks if not t.completion_status]
    completed_tasks = [t for t in all_tasks if t.completion_status]

    with col1:
        st.metric("Total Tasks", len(all_tasks))
    with col2:
        st.metric("Pending", len(pending_tasks))
    with col3:
        st.metric("Completed", len(completed_tasks))

    # Frequency breakdown
    st.write("**Tasks by Frequency:**")
    freq_col1, freq_col2, freq_col3 = st.columns(3)
    with freq_col1:
        daily_count = len(scheduler.get_tasks_by_frequency("daily"))
        st.metric("Daily", daily_count)
    with freq_col2:
        weekly_count = len(scheduler.get_tasks_by_frequency("weekly"))
        st.metric("Weekly", weekly_count)
    with freq_col3:
        monthly_count = len(scheduler.get_tasks_by_frequency("monthly"))
        st.metric("Monthly", monthly_count)
else:
    st.info("No task statistics available yet.")

