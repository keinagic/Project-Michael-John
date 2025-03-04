# from pathlib import Path
# from modules.database_modules import core_database_modules
# from modules.user_interface_backend import user_inputs
from modules.database_modules import core_database as db
from modules.database_modules import core_database_checker
from cfg import CORE_ORGANIZATION_DATABASE as CORE_DB_PATH


class CoreFoolProofing:
    @staticmethod
    def check_database():
        if not CORE_DB_PATH.exists():
            print("Making your database for you...")
            conn = db.create_connection(CORE_DB_PATH)
            if conn:
                conn.close()
                CoreFoolProofing.check_tables()
            else:
                print("Failed to create the database connection.")
        else:
            CoreFoolProofing.check_tables()

    @staticmethod
    def check_tables():
        conn = db.create_connection(CORE_DB_PATH)
        try:
            required_table = "trainees"
            if not core_database_checker.table_exists(conn, required_table):
                print("Tables not found! Creating tables...")
                try:
                    db.CreateMainTables.create_trainees(conn)
                    db.CreateMainTables.create_teams(conn)
                    db.CreateMainTables.create_team_members(conn)
                    db.CreateMainTables.create_scores(conn)
                    print("Tables created successfully.")
                    print("Verifying table creation...")
                    CoreFoolProofing.check_database_integrity()
                except Exception as e:
                    print(f"Error creating tables: {e}")
            else:
                print("Tables exist. Proceeding to integrity check.")
                CoreFoolProofing.check_database_integrity()
        finally:
            conn.close()

    @staticmethod
    def check_database_integrity():
        """Verify database schema integrity and apply fixes if necessary."""
        conn = db.create_connection(CORE_DB_PATH)
        try:
            print("Checking database integrity...")
            core_database_checker.check_db_integrity(conn)
        except Exception as e:
            print(f"Error checking database integrity: {e}")
        finally:
            conn.close()
