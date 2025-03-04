import sqlite3
import datetime
import csv
from pathlib import Path
from cfg import CORE_ORGANIZATION_DATABASE as CORE_DB_PATH

class CoreDatabaseFunctions:
    # Get the sequence number for the current month
    @staticmethod
    def get_sequence_number(conn, current_month, current_year):
        c = conn.cursor()
        try:
            c.execute(
                """
                SELECT MAX(unique_trainee_id) FROM trainees
                WHERE unique_trainee_id LIKE ?
                """,
                (f"{current_year}{current_month}%",),
            )
            sequence_number = c.fetchone()[0]
            if sequence_number is None:
                sequence_number = 0
            else:
                sequence_number = int(sequence_number[-3:])
            return sequence_number
        except sqlite3.Error as e:
            print(f"Error retrieving sequence number: {e}")
            return None

    # Generate a unique trainee ID
    @staticmethod
    def generate_unique_trainee_id(conn):
        current_date = datetime.datetime.now().date()
        current_month = current_date.strftime("%m")
        current_year = current_date.strftime("%y")

        while True:

            sequence_number = CoreDatabaseFunctions.get_sequence_number(
                conn, current_month, current_year
            )
            sequence_number_int = int(sequence_number) + 1
            sequence_number_str = str(sequence_number_int).zfill(3)
            unique_trainee_id = f"{current_year}{current_month}{sequence_number_str}"

            c = conn.cursor()
            c.execute(
                "SELECT 1 FROM trainees WHERE unique_trainee_id = ?",
                (unique_trainee_id,),
            )
            if c.fetchone() is None:
                return unique_trainee_id

    # Register a trainee
    @staticmethod
    def register_trainee(
        conn, unique_trainee_id, last_name, first_name, novice_status=1
    ):
        c = conn.cursor()
        try:
            c.execute(
                "SELECT 1 FROM trainees WHERE unique_trainee_id = ?",
                (unique_trainee_id,),
            )
            if c.fetchone():
                print(f"Trainee {unique_trainee_id} already exists")
                return None
            c.execute(
                """
                INSERT INTO trainees (unique_trainee_id, first_name, last_name, novice_status)
                VALUES (?, ?, ?, ?)
                """,
                (unique_trainee_id, first_name, last_name, novice_status),
            )
            conn.commit()
            print(f"Registered trainee: {unique_trainee_id}")
            return unique_trainee_id
        except sqlite3.Error as e:
            print(f"Error registering trainee: {e}")
            conn.rollback()
            return None

    # Update the novice status of a trainee
    @staticmethod
    def update_novice_status(conn, unique_trainee_id, novice_status):
        c = conn.cursor()
        try:
            c.execute(
                """
                UPDATE trainees
                SET novice_status = ?
                WHERE unique_trainee_id = ?
                """,
                (novice_status, unique_trainee_id),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating novice status: {e}")
            conn.rollback()

    # Add a score for a trainee
    @staticmethod
    def add_score(conn, trainee_id, score, role, score_type):
        valid_roles = {"Debater", "Adjudicator"}
        valid_types = {"Training", "Tournament"}

        if role not in valid_roles or score_type not in valid_types:
            print("Invalid role or score type")
            return
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO scores (trainee_id, score, role, score_type)
                VALUES (?, ?, ?, ?)
                """,
                (trainee_id, score, role, score_type),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding score: {e}")
            conn.rollback()

    # Create a team
    @staticmethod
    def create_team(conn, debate_format, team_name):
        if debate_format not in (0, 1):
            print("Invalid debate format.")
            return None

        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO teams (debate_format, team_name)
                VALUES (?, ?)
                """,
                (debate_format, team_name),
            )
            conn.commit()
            team_id = c.lastrowid
            print(f"Created team: {team_id}")
            return team_id
        except sqlite3.Error as e:
            print(f"Error creating team: {e}")
            conn.rollback()
            return None

    # Add a trainee to a team
    @staticmethod
    def add_team_member(conn, team_id, trainee_id):
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO team_members (team_id, trainee_id)
                VALUES (?, ?)
                """,
                (team_id, trainee_id),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding team member: {e}")
            conn.rollback()

    # Get a trainee by unique_trainee_id
    @staticmethod
    def get_trainee(conn, unique_trainee_id):
        c = conn.cursor()
        try:
            c.execute(
                """
                SELECT * FROM trainees
                WHERE unique_trainee_id = ?
                """,
                (unique_trainee_id,),
            )
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving trainee: {e}")
            return None
        
class ExportData:
    @staticmethod
    def export_trainees_for_tourney(db_path: Path, output_file: Path):
        db_path = CORE_DB_PATH
        c = sqlite3.connect(str(db_path))
        cursor = c.cursor()
        
        query = "SELECT unique_trainee_id, first_name, last_name FROM trainees"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        
        with output_file.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(["unique_trainee_id", "first_name", "last_name"])
            
            writer.writerow(rows)
            
            c.close()
            print("Trainee data exported, and ready for tournament import")