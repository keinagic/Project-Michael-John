import sqlite3
from pathlib import Path
from cfg import TOURNAMENT_NAME, TOURNAMENT_DIRECTORY, TOURNAMENT_DATABASE
from tournament_database import TournamentDatabaseTables as tdbtables
import tournament_database as tdb
import csv


class TournamentDatabaseModules:
    def import_trainees(csv_file: Path, db_path: Path):
        db_path = TOURNAMENT_DATABASE
        c = tdb.create_tourney_db_connection(db_path)
        cursor = c.cursor()

        try:
            tdbtables.index_table_of_trainees()
        except sqlite3.Error as e:
            return None

        with csv_file.open("r", newline="", encoding="utf8") as csvfile:
            reader = csv.DictReader(csv_file)
            for row in reader:
                unique_trainee_id = row["unique_trainee_id"]
                first_name = row["first_name"]
                last_name = row["last_name"]

                try:
                    cursor.execute(
                        """
                        INSERT INTO trainees(
                            unique_trainee_id,
                            first_name,
                            last_name
                        )
                        VALUES (?,?,?)
                        """(
                            unique_trainee_id, first_name, last_name
                        )
                    )
                except sqlite3.Error as e:
                    print(f"Error inserting row {row}: {e}")
        c.commit()
        c.close()

        print("CSV import completed successfully.")
