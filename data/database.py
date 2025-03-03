import sqlite3
from pathlib import Path

DB_PATH = Path("trainees.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS trainees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            novice_status INTEGER DEFAULT 1, --1 for Novice, 0 for Advanced
            role TEXT CHECK(role IN ('Debater', 'Adjudicator')) DEFAULT 'Debater'
        )
    """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY,
            trainee_id INTEGER,
            score REAL,
            role TEXT CHECK(role IN ('Debater', 'Adjudicator')),
            type TEXT CHECK(type IN ('Training', 'Tournament')),
            FOREIGN KEY(trainee_id) REFERENCES trainees(id)
        )
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS teams(
            id INTEGER PRIMARY KEY,
            format TEXT CHECK(format IN ('AsParl', 'BritParl')),
            team_name TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS team_members(
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            trainee_id INTEGER,
            FOREIGN KEY(team_id) REFERENCES teams(id),
            FOREIGN KEY(trainee_id) REFERENCES trainees(id)
        )
        """
    )
    conn.commit()


def register_trainee(conn, name, role="Debater"):
    c = conn.cursor()
    try:
        c.execute(
            """
            INSERT INTO trainees (name, role)
            VALUES (?, ?)
            """,
            (name, role),
        )
        conn.commit()
        trainee_id = c.lastrowid
        print(f"Registered trainee: {trainee_id}")
        return trainee_id
    except sqlite3.Error as e:
        print(f"Error registering trainee: {e}")
        conn.rollback()
        return None


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
    except sqlite3.Error as e:
        print(f"Error creating team: {e}")
        conn.rollback()


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
