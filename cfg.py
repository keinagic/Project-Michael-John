from pathlib import Path
from modules import set_organization_name
from modules import common_modules
    
# Core Directories
ORGANIZATION_NAME = set_organization_name()

CORE_PROJECT_ROOT = Path(__file__).resolve().parent
CORE_ORGANIZATION_DIRECTORY = CORE_PROJECT_ROOT / "user_data" / f"{ORGANIZATION_NAME}"
CORE_ORGANIZATION_DATABASE = (
    CORE_PROJECT_ROOT
    / "user_data"
    / f"{ORGANIZATION_NAME}"
    / f"core_{ORGANIZATION_NAME}.db"
)

# Tournament Directories
TOURNAMENT_NAME = common_modules.CommonModules.set_tournament_name()
TOURNAMENT_DIRECTORY = CORE_ORGANIZATION_DIRECTORY / f"{TOURNAMENT_NAME}"
TOURNAMENT_DATABASE = TOURNAMENT_DIRECTORY / f"{TOURNAMENT_NAME}.db"