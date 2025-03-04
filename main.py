from data import database_checker
from data import database as db


class FoolProofing:
    @staticmethod
    def check_tables():
        """Ensure that tables exist in the database."""
        conn = db.create_connection()

        # Check if at least one table exists
        required_table = "trainees"  # Change this to a table that must exist
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
            finally:
                conn.close()
        else:
            print("Tables exist. Proceeding to integrity check.")
            FoolProofing.check_database_integrity()

    @staticmethod
    def check_database_integrity():
        """Verify database schema integrity and apply fixes if necessary."""
        conn = db.create_connection()
        try:
            print("Checking database integrity...")
            database_checker.check_db_integrity(conn)
        except Exception as e:
            print(f"Error checking database integrity: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    FoolProofing.check_tables()
