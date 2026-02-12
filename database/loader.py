import sqlite3
import json
import os
from .database_manager import DatabaseManager

def load_data(database_name:str):
    DatabaseManager.set_db_name(database_name)
    DatabaseManager.init_db()
    print("Database initialization successful!")    
    # load questions
    if os.path.exists("json/questions.json"):
        with open("json/questions.json", "r") as f:
            q_data = json.load(f)
            for q in q_data:
                try:
                  DatabaseManager.add_question(q["question"], q["options"], q["correct_index"])  
                except sqlite3.IntegrityError:
                    continue 
        print(f"Loaded {len(q_data)} questions.")
    else:
        print("Warning: questions.json not found.")

 
