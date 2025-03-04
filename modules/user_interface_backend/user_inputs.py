from pathlib import Path
from cfg import CORE_ORGANIZATION_DIRECTORY as CORE_DIR


class CoachInput:

    @staticmethod
    def make_database_name(organization_name: str) -> str:
        # Hopefully going to be used for UI hehehehehe
        return organization_name

    @staticmethod
    def get_database_list() -> list:
        # Hopefully useful enough to be used for UI eheheheh
        database_paths = CORE_DIR
        db_files = [file.name for file in CORE_DIR.glob("*.db") if file.is_file()]
        return db_files

    def set_organization_name(user_organization: str) -> str:
        return user_organization
