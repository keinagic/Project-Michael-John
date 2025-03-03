import os
from data import database, database_checker


class FoolProofing:
    @staticmethod
    def create_tables():
    # Create tables if they don't exist; make sure that there is a table to work with
        conn = database.create_connection()
        if not os.path.exists(database.DB_PATH):
            try:
                database.create_tables(conn)
                print("Tables created successfully")
            except Exception as e:
                print(f"Error creating tables: {e}")
            finally:
                conn.close()
        else:
            print("Database already exists")

    def check_db_integrity():
        conn = database.create_connection()
        try:
            database_checker.check_db_integrity(conn)
        except Exception as e:
            print(f"Error checking database integrity: {e}")
        finally:
            conn.close()



if __name__ == "__main__":
    FoolProofing.create_tables()
    FoolProofing.check_db_integrity()
