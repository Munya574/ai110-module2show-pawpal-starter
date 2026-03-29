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

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

owner = st.session_state.owner

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

st.subheader("Owner & Pets")
owner_name = st.text_input("Owner name", value=owner.name)
available_minutes = st.number_input(
    "Available minutes per day", min_value=0, max_value=1440, value=owner.available_minutes
)
owner.name = owner_name
owner.available_minutes = available_minutes

st.markdown("### Add a new pet")
new_pet_name = st.text_input("New pet name", value="Mochi")
new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=new_pet_name, species=new_pet_species))
    st.success(f"Added {new_pet_name} to {owner.name}'s pets.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age, "tasks": len(pet.tasks)}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add a task for a specific pet.")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet = st.selectbox("Pet", pet_names)
    task_description = st.text_input("Task description", value="Morning walk")
    task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    task_category = st.selectbox("Category", ["walk", "feed", "meds", "grooming", "play", "other"], index=0)

    if st.button("Add task"):
        priority_map = {"high": 1, "medium": 2, "low": 3}
        task = Task(
            description=task_description,
            duration_minutes=task_duration,
            frequency="daily",
            priority=priority_map[task_priority],
            category=task_category,
        )
        scheduler = Scheduler(owner)
        scheduler.add_task_to_pet(selected_pet, task)
        st.success(f"Added task to {selected_pet}.")

    st.write("Current tasks by pet:")
    for pet in owner.pets:
        st.markdown(f"**{pet.name} ({pet.species})**")
        if pet.tasks:
            st.table(
                [
                    {
                        "description": task.description,
                        "duration": task.duration_minutes,
                        "frequency": task.frequency,
                        "priority": task.priority,
                        "category": task.category,
                        "completed": task.completed,
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.write("No tasks yet for this pet.")
else:
    st.info("Add a pet before you add tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate today’s schedule using your owner and pet data.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    st.text(scheduler.explain_plan())
