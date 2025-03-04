import sqlite3
from pathlib import Path

def create_tourney_db_connection(tourney_db_path: Path):
    try:
        conn = sqlite3.connect(str(tourney_db_path))
        return conn
    except sqlite3.Error as e:
        print(f"Error making a database: {e}")
        return None

class TournamentDatabaseTables:
    @staticmethod
    def index_table_of_trainees(conn):
        c = conn.cursor()
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS trainees(
                    unique_trainee_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Trainees table not created: {e}\nPlease retry.")

    @staticmethod
    def create_debaters(conn):
        # Create the debaters table
        c = conn.cursor()
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS debaters(
                    unique_trainee_id TEXT,
                    inrounds_score_total INT,
                    team_id TEXT,
                    FOREIGN KEY(unique_trainee_id) REFERENCES trainees(unique_trainee_id),
                    FOREIGN KEY(team_id) REFERENCES teams(team_name)
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Debaters table not created: {e}\nPlease retry.")

    @staticmethod
    def create_adjes(conn):
        # Create the adjudicators table
        c = conn.cursor()
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS adjudicators(
                    unique_trainee_id TEXT,
                    inrounds_score_total INT,
                    FOREIGN KEY(unique_trainee_id) REFERENCES trainees(unique_trainee_id)
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Adjudicators table not created: {e}\nPlease retry.")
            
    @staticmethod
    def create_teams(conn):
        # Create the teams table
        c = conn.cursor()
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS teams(
                    team_name TEXT PRIMARY KEY,
                    break_eligibility INT -- 1 is novice, 0 is open
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Teams table not created: {e}\nPlease retry.")

    @staticmethod
    def create_round(conn, round_number: int):
        # Create a round table; adjust the schema as needed for your tournament
        c = conn.cursor()
        try:
            c.execute(
                f"""
                CREATE TABLE IF NOT EXISTS round{round_number}(
                    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id TEXT,
                    score INT,
                    FOREIGN KEY(team_id) REFERENCES teams(team_name)
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating round table round{round_number}: {e}")
            return None
