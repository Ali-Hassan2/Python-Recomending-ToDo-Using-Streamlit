import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import time
from Db_ToDo import create_table, add_data, view_data, view_all_unique_data, get_task, edit_task_data, delete_task

from datetime import datetime


def calculate_priority(task_due_date, task_importance, time_remaining):

    if isinstance(task_due_date, str):
        task_due_date = datetime.strptime(task_due_date, "%Y-%m-%d").date()


    current_date = datetime.today().date()

    if time_remaining == "1D":
        remaining_days = 1
    elif time_remaining == "2D":
        remaining_days = 2
    elif time_remaining == "3D":
        remaining_days = 3
    elif time_remaining == "4D":
        remaining_days = 4
    elif time_remaining == "5D":
        remaining_days = 5
    elif time_remaining == "6D":
        remaining_days = 6
    elif time_remaining == "7D":
        remaining_days = 7
    else:

        remaining_days = (task_due_date - current_date).days


    if remaining_days <= 0:
        remaining_days = 1


    priority_score = 1 / remaining_days


    priority_score += (task_importance * 0.2)

    return priority_score

def predict_tasks(tasks):
    task_data = []
    for task in tasks:
        task_name = task[0]
        task_status = task[1]
        task_due_date = task[2]
        task_description = task[3]
        time_remaining = task[4]
        task_importance = task[5]


        priority_score = calculate_priority(task_due_date, task_importance, time_remaining)

        task_data.append({
            "task": task_name,
            "status": task_status,
            "due_date": task_due_date,
            "description": task_description,
            "time_remaining": time_remaining,
            "importance": task_importance,
            "priority_score": priority_score
        })


    task_data_sorted = sorted(task_data, key=lambda x: x['priority_score'], reverse=True)
    return task_data_sorted



def main():
    st.title("Predictive ToDo List App")

    menu = ["Create", "Read", "Update", "Delete", "About", "Prediction"]
    option = st.sidebar.selectbox("Menu", menu)

    create_table()

    if option == "Create":
        st.subheader("Create New")
        area1, area2 = st.columns(2)

        with area1:
            task = st.text_area("Task To Do: ")

        with area2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_rem = st.selectbox("Time Remaining", ["1D", "2D", "3D", "4D", "5D", "6D", "7D", "more..."])
            task_due_date = st.date_input("Due Date")
            task_description = st.text_area("Description:")


            task_importance = st.slider("Task Importance", 1, 5, 3)

            if st.button("Add Task"):
                add_data(task, task_status, task_due_date, task_description, task_rem, task_importance)
                st.success("Data Save Successfully {}".format(task))

    elif option == "Read":
        st.subheader("Task List")

        result = view_data()

        st.write(result)

        dataFrame = pd.DataFrame(result, columns=['Task', 'Task Status', 'Due Date', 'Description', 'Time Remaining',
                                                  'Importance'])

        with st.expander("View All Data"):
            st.dataframe(dataFrame)

        with st.expander("Task Status"):
            taskpd = dataFrame['Task Status'].value_counts().to_frame().reset_index()
            taskpd.columns = ['Task Status', 'count']
            st.dataframe(taskpd)

            p1 = px.pie(taskpd, names='Task Status', values='count')
            st.plotly_chart(p1)

    elif option == "Update":
        st.subheader("Update Any Task")

        result = view_data()

        dataFrame = pd.DataFrame(result,
                                 columns=["Task", "Status", "Due Date", "Description", "Time Remaining", "Importance"])

        with st.expander("Current Data"):
            st.dataframe(dataFrame)

        listTasks = [i[0] for i in view_all_unique_data()]

        selectedTask = st.selectbox("Task to Edit", listTasks)

        selectedResult = get_task(selectedTask)

        if selectedResult:
            task = selectedResult[0][0]
            task_status = selectedResult[0][1]
            task_due_date = selectedResult[0][2]
            task_description = selectedResult[0][3]
            time_remaining = selectedResult[0][4]
            task_importance = selectedResult[0][5]

            if isinstance(task_due_date, str):
                try:
                    task_due_date = datetime.strptime(task_due_date, "%Y-%m-%d").date()
                except ValueError:
                    task_due_date = datetime.today().date()

            area1, area2 = st.columns(2)

            with area1:
                new_task = st.text_area("Task To Do: ", task)

            with area2:
                new_task_status = st.selectbox("Task Status", ["ToDo", "Doing", "Done"],
                                               index=["ToDo", "Doing", "Done"].index(task_status))

                new_task_due_date = st.date_input("Due Date", task_due_date)
                new_task_description = st.text_area("Description:", task_description)

                new_time_remaining = st.selectbox("Time Remaining",
                                                  ["1D", "2D", "3D", "4D", "5D", "6D", "7D", "more..."],
                                                  index=["1D", "2D", "3D", "4D", "5D", "6D", "7D", "more..."].index(
                                                      time_remaining))

                new_task_importance = st.slider("Importance (1 to 5)", 1, 5, task_importance)

                if st.button("Update Task"):
                    edit_task_data(new_task, new_task_status, new_task_due_date, new_task_description,
                                   new_time_remaining, new_task_importance)

                    st.success(f"Data Updated Successfully: {task} To {new_task}")
    elif option == "Delete":
        st.subheader("Delete Task")

        result = view_data()
        dataFrame = pd.DataFrame(result,
                                 columns=["Task", "Status", "Due Date", "Description", "Time Remaining", "Importance"])

        with st.expander("Current Tasks"):
            st.dataframe(dataFrame)


        listTasks = [i[0] for i in view_all_unique_data()]
        selectedTask = st.selectbox("Select Task to Delete", listTasks)

        if selectedTask:
            if st.button("Delete Task"):
                try:
                    # Call the delete_task function from Db_ToDo.py
                    delete_task(selectedTask)
                    st.success(f"Task '{selectedTask}' deleted successfully.")
                except Exception as e:
                    st.error(f"Error deleting task: {e}")





    elif option == "Prediction":

        st.subheader("Prediction of Tasks.")


        result = view_data()



        task_df = pd.DataFrame(result)



        st.write("Here are your current tasks:")

        st.dataframe(task_df)



        if st.button('What AI Suggests'):



            with st.spinner('AI is calculating your most urgent task...'):

                time.sleep(2)



                predicted_tasks = predict_tasks(result)



                st.write("Here are your tasks sorted by priority (time remaining and importance):")

                predicted_task_df = pd.DataFrame(predicted_tasks)



                st.dataframe(predicted_task_df[['task', 'priority_score', 'due_date', 'importance']])



                if predicted_tasks:
                    most_urgent_task = predicted_tasks[0]

                    suggestion_text = f"**AI Suggests:** First, you should complete: **{most_urgent_task['task']}** due on {most_urgent_task['due_date']} with importance level {most_urgent_task['importance']} and a priority score of {most_urgent_task['priority_score']}"

                    st.write(suggestion_text)
    else:
        st.markdown("""
            <style>
                .about-container {
                    background-color: #f7f9fc;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    margin-top: 20px;
                    animation: fadeIn 1.5s ease-out;
                }

                .about-title {
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #4CAF50;
                    margin-bottom: 20px;
                    animation: slideIn 1.5s ease-out;
                }

                .about-text {
                    font-size: 1.2rem;
                    color: white;
                    line-height: 1.8;
                    animation: fadeIn 2s ease-out;
                }

                .highlight {
                    color: #007bff;
                    font-weight: 600;
                }

                .tech-stack {
                    display: flex;
                    justify-content: center;
                    gap: 15px;
                    margin-top: 20px;
                }

                .tech-stack img {
                    height: 50px;
                }

                /* Keyframe animations */
                @keyframes fadeIn {
                    0% { opacity: 0; }
                    100% { opacity: 1; }
                }

                @keyframes slideIn {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(0); }
                }
            </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="about-container">', unsafe_allow_html=True)

        st.markdown('<h2 class="about-title">Welcome to the Predictive ToDo List App!</h2>', unsafe_allow_html=True)

        st.markdown("""
                        <p class="about-text">This application helps you stay organized by providing an easy-to-use platform to manage your tasks. You can create, update, view, and delete tasks while keeping track of their status, due dates, and importance.</p>

                        <p class="about-text">Whether you're managing your daily to-do list or planning long-term tasks, this app ensures you never miss out on what’s important. It predicts and prioritizes tasks based on the urgency and importance you set for each task.</p>

                        <h3 class="about-title">Key Features:</h3>
                        <ul class="about-text">
                            <li><strong>Create Tasks:</strong> Add new tasks with detailed information.</li>
                            <li><strong>Update Tasks:</strong> Edit existing tasks, such as their status, due date, description, and importance.</li>
                            <li><strong>View Tasks:</strong> See all your tasks listed, filtered by status or priority.</li>
                            <li><strong>Delete Tasks:</strong> Remove completed or irrelevant tasks.</li>
                        </ul>

                        <h3 class="about-title">How It Works:</h3>
                        <ol class="about-text">
                            <li>Add a new task with details like status, due date, and importance.</li>
                            <li>You can update tasks as you progress, setting the correct status (ToDo, Doing, Done).</li>
                            <li>Tasks can be deleted once completed or no longer needed.</li>
                        </ol>

                        <h3 class="about-title">Why Predictive?</h3>
                        <p class="about-text">The app doesn't just let you manage tasks—it predicts and prioritizes based on the due dates and task importance, helping you focus on what matters most.</p>

                        <h3 class="about-title">Technologies Used:</h3>
                        <ul class="about-text">
                            <li><strong>Python</strong> (for backend)</li>
                            <li><strong>Streamlit</strong> (for the frontend)</li>
                            <li><strong>SQLite</strong> (for storing task data)</li>
                            <li><strong>Plotly</strong> (for interactive data visualization)</li>
                        </ul>

                        <h3 class="about-title">Developed By:</h3>
                        <p class="about-text">**Ali Hassan** – A passionate developer with a focus on creating useful productivity tools.</p>

                        <p class="about-text">If you have any feedback or suggestions, feel free to reach out via GitHub or other social media channels.</p>
                    """, unsafe_allow_html=True)

        st.markdown('<div class="tech-stack">', unsafe_allow_html=True)
        st.markdown("""
                        <a href="https://github.com/Ali-Hassan2">
                            <img src="https://img.shields.io/badge/GitHub-Ali%20Hassan-%2312101C?logo=github" alt="GitHub Badge">
                        </a>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
