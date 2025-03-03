import kots_interface.main_window as main_window
import os
from data import database


class FoolProofing:
    @staticmethod
    def create_tables():
        conn = database.DBConnection.create_connection()
        if not os.path.exists(database.DB_PATH):
            try:
                database.DBConnection.create_tables(conn)
                print("Tables created successfully")
            except Exception as e:
                print(f"Error creating tables: {e}")
            finally:
                conn.close()
        else:
            print("Database already exists")


if __name__ == "__main__":
    FoolProofing.create_tables()
    main_window.main()
