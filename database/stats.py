import sqlite3
import os

class UserStatsManager:
    @staticmethod
    def get_db_connection(db_path: str) -> sqlite3.Connection:
        """Establishes connection and enforces row-factory dict mappings."""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def get_global_metrics(db_path: str) -> dict:
        """Calculates cohort-wide statistical aggregate data summaries."""
        db_real_path = os.path.abspath(db_path)
        with UserStatsManager.get_db_connection(db_real_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    COUNT(id) AS total_candidates,
                    ROUND(COALESCE(AVG(score), 0), 2) AS avg_score,
                    COALESCE(MAX(score), 0) AS max_score,
                    COALESCE(MIN(score), 0) AS min_score
                FROM users
            """)
            return dict(cur.fetchone())

    @staticmethod
    def get_top_performers(db_path: str, limit: int = 5) -> list:
        """Retrieves top scoring students using subquery logic thresholds."""
        db_real_path = os.path.abspath(db_path)
        with UserStatsManager.get_db_connection(db_real_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, roll_no, email, score 
                FROM users 
                WHERE score >= (SELECT AVG(score) FROM users)
                ORDER BY score DESC, name ASC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_all_student_records(db_path: str) -> list:
        """Returns complete administrative student roster array metrics."""
        db_real_path = os.path.abspath(db_path)
        with UserStatsManager.get_db_connection(db_real_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, roll_no, email, phone, cnic, score 
                FROM users
                ORDER BY roll_no ASC
            """)
            return [dict(row) for row in cur.fetchall()]