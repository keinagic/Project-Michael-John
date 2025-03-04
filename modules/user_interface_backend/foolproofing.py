from pathlib import Path
from modules.database_modules import database as db  # Make sure your module is imported correctly.
from modules.user_interface_backend import user_inputs  # Adjust according to your actual module name.
from modules.database_modules import database_checker  # Assuming this module is available.

class FoolProofing:
    # Placeholder will be replaced with user input from a UI.
    DB_NAME = user_inputs.CoachInput.make_database_name("placeholder")
    DATA_PATH = Path(__file__).resolve().parent.parent.parent
    DB_PATH = DATA_PATH / "user_data" / f"{DB_NAME}.db"

    @staticmethod
    def check_database():
        if not FoolProofing.DB_PATH.exists():
            print("Making your database for you...")
            conn = db.create_connection(FoolProofing.DB_PATH)
            if conn:
                conn.close()
                FoolProofing.check_tables()
            else:
                print("Failed to create the database connection.")
        else:
            FoolProofing.check_tables()

    @staticmethod
    def check_tables():
        """Ensure that tables exist in the database."""
        conn = db.create_connection(FoolProofing.DB_PATH)
        try:
            required_table = "trainees"
            if not database_checker.table_exists(conn, required_table):
                print("Tables not found! Creating tables...")
                try:
                    db.CreateTables.create_trainees(conn)
                    db.CreateTables.create_teams(conn)
                    db.CreateTables.create_team_members(conn)
                    db.CreateTables.create_scores(conn)
                    print("Tables created successfully.")
                    print("Verifying table creation...")
                    FoolProofing.check_database_integrity()
                except Exception as e:
                    print(f"Error creating tables: {e}")
            else:
                print("Tables exist. Proceeding to integrity check.")
                FoolProofing.check_database_integrity()
        finally:
            conn.close()

    @staticmethod
    def check_database_integrity():
        """Verify database schema integrity and apply fixes if necessary."""
        conn = db.create_connection(FoolProofing.DB_PATH)
        try:
            print("Checking database integrity...")
            database_checker.check_db_integrity(conn)
        except Exception as e:
            print(f"Error checking database integrity: {e}")
        finally:
            conn.close()
