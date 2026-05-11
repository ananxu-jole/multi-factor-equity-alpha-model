from __future__ import annotations

from datetime import datetime
from pathlib import Path


PHASE2_NB01_FOLDER_NAME = "nb01_data_foundation"


def get_project_root() -> Path:
    """Return the project root based on the src/ package location."""
    return Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    return get_project_root() / "data"


def get_processed_dir() -> Path:
    return get_data_dir() / "processed"


def get_phase2_processed_dir() -> Path:
    return get_processed_dir() / "phase2"


def get_phase2_nb01_output_dir() -> Path:
    return get_phase2_processed_dir() / PHASE2_NB01_FOLDER_NAME


def get_sql_dir() -> Path:
    return get_project_root() / "sql"


def get_sqlite_db_path() -> Path:
    return get_sql_dir() / "project_underdog.db"


def make_run_id(prefix: str = "phase2_nb01") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}"


def make_run_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_phase2_nb01_directories() -> dict[str, Path]:
    project_root = get_project_root()
    data_dir = ensure_directory(get_data_dir())
    processed_dir = ensure_directory(get_processed_dir())
    phase2_dir = ensure_directory(get_phase2_processed_dir())
    output_dir = ensure_directory(get_phase2_nb01_output_dir())
    sql_dir = ensure_directory(get_sql_dir())

    return {
        "project_root": project_root,
        "data_dir": data_dir,
        "processed_dir": processed_dir,
        "phase2_dir": phase2_dir,
        "output_dir": output_dir,
        "sql_dir": sql_dir,
        "sqlite_db_path": get_sqlite_db_path(),
    }
