import sqlite3
from pathlib import Path
from cfg import CORE_ORGANIZATION_DATABASE as CORE_DB_PATH


def create_connection(db_path: Path):
    db_path = CORE_DB_PATH
    try:
        CORE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        return conn
    except sqlite3.Error as e:
        print(f"Error making a database: {e}")
        return None


class CreateMainTables:
    @staticmethod
    def create_trainees(conn):
        c = conn.cursor()
        # trainees table
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS trainees (
                    unique_trainee_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    novice_status INTEGER CHECK (novice_status IN(0,1))
                )
                """
            )
        except sqlite3.Error as e:
            print(f"Error creating trainees table: {e}")
        conn.commit()

    @staticmethod
    def create_scores(conn):
        c = conn.cursor()
        # scores table
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS scores(
                    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trainee_id TEXT,
                    score REAL,
                    role TEXT CHECK(role IN ('Debater', 'Adjudicator')),
                    score_type TEXT CHECK(score_type IN ('Training', 'Tournament')),
                    FOREIGN KEY(trainee_id) REFERENCES trainees(unique_trainee_id)
                )
                """
            )
        except sqlite3.Error as e:
            print(f"Error creating scores table: {e}")
        conn.commit()

    @staticmethod
    def create_teams(conn):
        c = conn.cursor()
        # teams table
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS teams(
                    id INTEGER PRIMARY KEY, 
                    debate_format INTEGER CHECK (debate_format IN(0,1)),
                    team_name TEXT
                )
                """
            )
        except sqlite3.Error as e:
            print(f"Error creating teams table: {e}")
        conn.commit()

    @staticmethod
    def create_team_members(conn):
        c = conn.cursor()
        # team_members table
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS team_members(
                    team_id INTEGER,
                    trainee_id TEXT,
                    PRIMARY KEY(team_id, trainee_id),
                    FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE CASCADE,
                    FOREIGN KEY(trainee_id) REFERENCES trainees(unique_trainee_id)
                )
                """
            )
        except sqlite3.Error as e:
            print(f"Error creating team_members table: {e}")
        conn.commit()
