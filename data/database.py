import sqlite3
from pathlib import Path
import datetime

DB_PATH = Path("trainees.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    c = conn.cursor()
    # trainees table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS trainees (
            unique_trainee_id TEXT UNIQUE PRIMARY KEY,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            novice_status INTEGER DEFAULT 1 --1 for Novice, 0 for Advanced
        )
        """
    )
    # scores table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS scores(
            trainee_id TEXT,
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
            debate_format INTEGER, -- 1 for AsParl, 0 for BritParl
            team_name TEXT
        )
        """
    )
    # team_members table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS team_members(
            team_id INTEGER,
            trainee_id TEXT,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            FOREIGN KEY(trainee_id) REFERENCES trainees(unique_trainee_id)
        )
        """
    )
    conn.commit()


class DatabaseFunctions:
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
                sequence_number = int(sequence_number[4:])
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
        sequence_number = DatabaseFunctions.get_sequence_number(
            conn, current_month, current_year
        )
        sequence_number_int = int(sequence_number) + 1
        sequence_number_str = str(sequence_number_int).zfill(3)
        unique_trainee_id = f"{current_year}{current_month}{sequence_number_str}"
        return unique_trainee_id

    # Register a trainee
    @staticmethod
    def register_trainee(conn, unique_trainee_id, last_name, first_name, novice_status=1):
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO trainees (unique_trainee_id, last_name, first_name, novice_status)
                VALUES (?, ?, ?, ?)
                """,
                (unique_trainee_id, last_name, first_name, novice_status),
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
    @staticmethod
    def create_team(conn, debate_format, team_name):
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
