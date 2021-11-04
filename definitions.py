from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

NHK_DATA_PATH = ROOT_DIR / "data/nhk_data.csv"
NHK_DATA_REV_PATH = ROOT_DIR / "data/nhk_data.rev.csv"
NHK_DATA_SQLITE_PATH = ROOT_DIR / "data/nhk_data.sqlite3"

NHK_DATA_LOOKUP_SIZE = 10
