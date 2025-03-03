import sqlite3
from pathlib import Path
import datetime

DB_PATH = Path("trainees.db")


@staticmethod
def create_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    c = conn.cursor()
    # trainees table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS trainees (
            id INTEGER PRIMARY KEY,
            unique_trainee_id TEXT UNIQUE,
            name TEXT NOT NULL,
            novice_status INTEGER DEFAULT 1 --1 for Novice, 0 for Advanced
        )
        """
    )
    # scores table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY,
            trainee_id INTEGER,
            score REAL,
            role TEXT CHECK(role IN ('Debater', 'Adjudicator')),
            type TEXT CHECK(type IN ('Training', 'Tournament')),
            FOREIGN KEY(trainee_id) REFERENCES trainees(unique_trainee_id)
        )
        """
    )
    # teams table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS teams(
            id INTEGER PRIMARY KEY,
            format TEXT CHECK(format IN ('AsParl', 'BritParl')),
            team_name TEXT
        )
        """
    )
    # team_members table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS team_members(
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            trainee_id INTEGER,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            FOREIGN KEY(trainee_id) REFERENCES trainees(unique_trainee_id)
        )
        """
    )
    conn.commit()


class DatabaseFunctions:
    # Get the sequence number for the current month
    def get_sequence_number(conn, current_month, current_year):
        c = conn.cursor()
        # Get the maximum sequence number for the current month
        try:
            c.execute(
                """
                SELECT MAX(unique_trainee_id) FROM trainees
                WHERE unique_trainee_id LIKE ?
                """,
                (f"{current_year}{current_month}%",),
            )
            # Extract the sequence number from the result
            sequence_number = c.fetchone()[0]
            if sequence_number is None:
                sequence_number = 0
            else:
                sequence_number = int(sequence_number[4:])
            return sequence_number

        # Handle exceptions
        except sqlite3.Error as e:
            print(f"Error retrieving sequence number: {e}")
            return None
    # Generate a unique trainee ID
    def generate_unique_trainee_id(conn):
        # Get the current date
        current_date = datetime.datetime.now().date()
        current_month = current_date.strftime("%m")
        current_year = current_date.strftime("%y")
        # Get the sequence number
        sequence_number = DatabaseFunctions.get_sequence_number(
            conn, current_month, current_year
        )
        # Increment the sequence number and format it
        sequence_number_int = int(sequence_number) + 1
        sequence_number_str = str(sequence_number_int).zfill(3)
        # Generate the unique trainee ID
        unique_trainee_id = f"{current_year}{current_month}{sequence_number_str}"
        return unique_trainee_id

    # Register a trainee
    def register_trainee(conn, unique_trainee_id, name, role="Debater"):
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO trainees (unique_trainee_id, name, role)
                VALUES (?, ?)
                """,
                (unique_trainee_id, name, role),
            )
            conn.commit()
            trainee_id = c.lastrowid
            print(f"Registered trainee: {trainee_id}")
            return trainee_id
        except sqlite3.Error as e:
            print(f"Error registering trainee: {e}")
            conn.rollback()
            return None

    # Update the novice status of a trainee
    def update_novice_status(conn, trainee_id, novice_status):
        c = conn.cursor()
        try:
            c.execute(
                """
                UPDATE trainees
                SET novice_status = ?
                WHERE id = ?
                """,
                (novice_status, trainee_id),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating novice status: {e}")
            conn.rollback()

    # Update the role of a trainee
    def update_role(conn, trainee_id, role):
        c = conn.cursor()
        try:
            c.execute(
                """
                UPDATE trainees
                SET role = ?
                WHERE id = ?
                """,
                (role, trainee_id),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating role: {e}")
            conn.rollback()

    # Add a score for a trainee
    def add_score(conn, trainee_id, score, role, type):
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO scores (trainee_id, score, role, type)
                VALUES (?, ?, ?, ?)
                """,
                (trainee_id, score, role, type),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding score: {e}")
            conn.rollback()

    # Create a team
    def create_team(conn, format, team_name):
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO teams (format, team_name)
                VALUES (?, ?)
                """,
                (format, team_name),
            )
            conn.commit()
            team_id = c.lastrowid
            print(f"Created team: {team_id}")  # debug
            return team_id
        except sqlite3.Error as e:
            print(f"Error creating team: {e}, SQL: {c.last_executed}")  # debug
            conn.rollback()
            return None

    # Add a trainee to a team
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

    # Get all trainees
    def get_trainee(conn, trainee_id):
        c = conn.cursor()
        try:
            c.execute(
                """
                SELECT * FROM trainees
                WHERE id = ?
                """,
                (trainee_id,),
            )
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving trainee: {e}")
            return None
