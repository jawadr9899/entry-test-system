import sqlite3
import json
import os
from .database_manager import DatabaseManager


def load_data(db: str):
    DatabaseManager.init_db(db)
    print("Database initialization successful!")    
    
    existing_questions = DatabaseManager.get_questions()
    if existing_questions:
        print(f"Database already contains {len(existing_questions)} questions. Skipping JSON import entirely.")
        return 

    json_path = "json/questions.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            q_data = json.load(f)
            loaded_count = 0
            for q in q_data:
                try:
                    DatabaseManager.add_question(q["question"], q["options"], q["correct_index"])  
                    loaded_count += 1
                except sqlite3.IntegrityError:
                    continue 
        print(f"Loaded {loaded_count} new questions from JSON file.")
    else:
        print(f"Warning: {json_path} not found. Skipping default question population injection.")