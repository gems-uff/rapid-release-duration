import os
import datetime
from enum import Enum
from pathlib import Path

def project_root() -> Path:
    return Path(__file__).parent.parent

DATA_PATH: Path = project_root() / 'data'
REPO_PATH: Path = project_root() / 'repos'
TMP_PATH: Path = project_root() / 'tmp'
CPU: int = int(os.getenv('CPU', 10))

RAPID_RELEASE_LIM = 7*6
TRAD_RELEASE_LIM = 7*12

class CycleType(Enum):
    FIRST = 'f'
    RAPID = 'r'
    TRAD = 't'
    OTHER = 'o'
    PROBLEM = 'p'

def delta2days(td):
    return td.total_seconds() / datetime.timedelta(days=1).total_seconds()

# def is_rapid_release(release):    
#     if not release.commits:
#         return False
#     if not release.prev_main_release:
#         return False
#     days = delta2days(release.cycle)
#     if days == 0:
#         return False
#     if days > RAPID_RELEASE_LIM:
#         return False
#     return True

# def is_trad_release(release):
#     if not release.commits:
#         return False
#     if not release.prev_main_release:
#         return False
#     days = delta2days(release.cycle)
#     if days == 0:
#         return False
#     if days < TRAD_RELEASE_LIM:
#         return False
#     return True