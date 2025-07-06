import sqlite3
conn = sqlite3.connect("data.db")
c = conn.cursor()

# Create table with additional columns and new name tasktablee
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS tasktablee(
                    task TEXT, 
                    task_status TEXT, 
                    task_due_date DATE,
                    task_description TEXT,
                    time_remaining TEXT,
                    task_importance INTEGER)''')
    conn.commit()


# Add data with additional fields: task_description, time_remaining, and task_importance
def add_data(task, task_status, task_due_date, task_description, time_remaining, task_importance):
    try:
        c.execute('''INSERT INTO tasktablee(task, task_status, task_due_date, task_description, time_remaining, task_importance)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (task, task_status, task_due_date, task_description, time_remaining, task_importance))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error during insertion: {e}")
    conn.commit()


# Reading Data from tasktablee
def view_data():
    try:
        c.execute('SELECT * FROM tasktablee')
        data = c.fetchall()
        return data
    except Exception as e:
        print(f"Error during reading: {e}")


def view_all_unique_data():
    c.execute('SELECT DISTINCT task FROM tasktablee')
    data = c.fetchall()
    return data


def get_task(task):
    c.execute('SELECT * FROM tasktablee WHERE task = ?', (task,))
    data = c.fetchall()
    return data


def edit_task_data(newTask, newTaskStatus, newTaskDueDate, newTaskDescription, newTimeRemaining, newTaskImportance):
    try:
        print(f"Updating task: {newTask}")
        query = '''UPDATE tasktablee SET task = ?, task_status = ?, task_due_date = ?, 
                   task_description = ?, time_remaining = ?, task_importance = ? WHERE task = ?'''
        c.execute(query, (newTask, newTaskStatus, newTaskDueDate, newTaskDescription, newTimeRemaining, newTaskImportance, newTask))
        conn.commit()

        # Check if task exists after update
        c.execute("SELECT * FROM tasktablee WHERE task = ?", (newTask,))
        data = c.fetchall()
        if data:
            print("Task updated successfully")
        else:
            print("No task found with this name")

        return data
    except Exception as e:
        print(f"Error during update: {e}")
def delete_task(task):
    try:
        c.execute('DELETE FROM tasktablee WHERE task = ?', (task,))
        conn.commit()
        print(f"Task '{task}' deleted successfully.")
    except Exception as e:
        print(f"Error during deletion: {e}")