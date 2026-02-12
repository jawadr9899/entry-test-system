import os
import sqlite3
import hashlib

DB_NAME = ""

class DatabaseManager:
    @staticmethod
    def set_db_name(database_name:str="entry_test.db"):
        global DB_NAME
        DB_NAME = "database/sqlite/" + database_name 
        
    @staticmethod
    def init_db(path:str=""):
        global DB_NAME
        if len(DB_NAME) == 0:
            DB_NAME = path

        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    roll_no TEXT UNIQUE,
                    email TEXT UNIQUE,
                    cnic TEXT UNIQUE,
                    password TEXT,
                    pic_path TEXT,
                    score INTEGER DEFAULT 0
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    opt1 TEXT, opt2 TEXT, opt3 TEXT, opt4 TEXT,
                    correct INTEGER
                )
            """)
            conn.commit()

    @staticmethod
    def clear_data():
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("DELETE FROM users")
            conn.execute("DELETE FROM questions")
            conn.commit()

    @staticmethod
    def add_student(name, roll_no, email, cnic,password,pic_path):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        with sqlite3.connect(DB_NAME) as conn:
            try:
                conn.execute(
                    "INSERT INTO users (name, roll_no, email, cnic, password, pic_path) VALUES (?, ?, ?,?,?,?)",
                    (name, roll_no, email,cnic, hashed, pic_path),
                )
            except sqlite3.IntegrityError:
                print(f"Skipping duplicate: {roll_no}")

    @staticmethod
    def login_student(roll_no, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            
            cur.execute("SELECT password FROM users WHERE roll_no=?", (roll_no,))
            result = cur.fetchone()
            
            if result is None:
                return None, "Roll No not found in Database"
            
            stored_password = result[0]
            
            if stored_password != hashed:
                return None, "Incorrect Password"
                
            cur.execute("SELECT id, name, roll_no,cnic,pic_path FROM users WHERE roll_no=?", (roll_no,))
            user = cur.fetchone()
            return user, None

    @staticmethod
    def add_question(q, opts, correct):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                "INSERT INTO questions (question, opt1, opt2, opt3, opt4, correct) VALUES (?,?,?,?,?,?)",
                (q, opts[0], opts[1], opts[2], opts[3], correct),
            )
            conn.commit()

    @staticmethod
    def get_questions():
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM questions")
            return cur.fetchall()

    @staticmethod
    def save_score(user_id, score):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("UPDATE users SET score=? WHERE id=?", (score, user_id))
            conn.commit()
