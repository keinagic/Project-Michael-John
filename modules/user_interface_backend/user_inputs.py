from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
USER_DATA_DIR = PROJECT_ROOT / "user_data"

class CoachInput:

    @staticmethod
    def make_database_name(organization_name: str) -> str:
        # Hopefully going to be used for UI hehehehehe
        return organization_name
    @staticmethod
    def get_database_list() -> list:
        # Hopefully useful enough to be used for UI eheheheh
        database_paths = USER_DATA_DIR
        db_files = list(database_paths.glob("*.db"))
        return db_files
