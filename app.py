import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.title("📚 AI Study Planner")

# User inputs
st.sidebar.header("Add Subjects")

subject_list = []
num_subjects = st.sidebar.number_input("Number of Subjects", 1, 10, 3)

for i in range(num_subjects):
    name = st.sidebar.text_input(f"Subject {i+1} Name", f"Subject {i+1}")
    deadline = st.sidebar.date_input(f"Deadline {i+1}", datetime.now())
    difficulty = st.sidebar.slider(f"Difficulty {i+1}", 1, 5, 3)

    subject_list.append({
        "name": name,
        "deadline": str(deadline),
        "difficulty": difficulty
    })

daily_hours = st.sidebar.slider("Daily Study Hours", 1, 12, 4)

# AI logic
def calculate_priority(subject):
    deadline = datetime.strptime(subject["deadline"], "%Y-%m-%d")
    days_left = (deadline - datetime.now()).days
    if days_left <= 0:
        days_left = 1
    return subject["difficulty"] / days_left

def generate_schedule(subjects, daily_hours):
    subjects_sorted = sorted(subjects, key=calculate_priority, reverse=True)
    schedule = []
    current_date = datetime.now()

    last_subject = None

    for subject in subjects_sorted:
        hours_needed = subject["difficulty"] * 2

        while hours_needed > 0:
            study_hours = min(daily_hours, hours_needed)

            # Avoid same subject repeatedly (basic AI improvement)
            if last_subject == subject["name"]:
                current_date += timedelta(days=1)

            schedule.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Subject": subject["name"],
                "Hours": study_hours
            })

            last_subject = subject["name"]
            hours_needed -= study_hours
            current_date += timedelta(days=1)

    return pd.DataFrame(schedule)

# Generate button
if st.button("Generate Study Plan"):
    df = generate_schedule(subject_list, daily_hours)
    st.success("✅ Plan Generated!")

    st.dataframe(df)

    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Plan", csv, "study_plan.csv", "text/csv")