import json
import os
from .database_manager import DatabaseManager

def load_data(database_name:str):
    DatabaseManager.set_db_name(database_name)
    if os.path.exists("database/sqlite/"+database_name): 
        return

    DatabaseManager.init_db()
    print("Database initialization successful!")    
    # load questions
    if os.path.exists("json/questions.json"):
        with open("json/questions.json", "r") as f:
            q_data = json.load(f)
            for q in q_data:
                DatabaseManager.add_question(q["question"], q["options"], q["correct_index"])
        print(f"Loaded {len(q_data)} questions.")
    else:
        print("Warning: questions.json not found.")

    # load students
    if os.path.exists("json/students.json"):
        with open("json/students.json", "r") as f:
            s_data = json.load(f)
            for s in s_data:
                DatabaseManager.add_student(s["name"], s["roll_no"], s["password"])
        print(f"Loaded {len(s_data)} students.")
    else:
        print("Warning: students.json not found.")

