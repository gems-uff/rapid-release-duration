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

def get_release_time(srelease):
    ''' Calculate when the release was ready to delivery '''
    if srelease.commits:
        return srelease.release.tag.commit.committer_time
        # return srelease.commits.last(lambda c: c.committer_time).committer_time
    else:
        return srelease.time
    
def get_cycle(srelease):
    ''' Calculate the time elapsed from previous release '''
    if srelease.prev_main_release:
        prev_release_time = get_release_time(srelease.prev_main_release)
        release_time = get_release_time(srelease)
        return release_time - prev_release_time
    else:
        return datetime.timedelta(0)

def get_start(srelease):
    ''' Calculate the time the release development started ''' 
    if srelease.commits:
        return srelease.commits.first(lambda c: c.author_time).author_time
    else:
        return get_release_time(srelease)
        
def get_duration(srelease):
    ''' Calculate the development duration '''
    return get_release_time(srelease) - get_start(srelease)
        
def get_start_delay(srelease):
    ''' Calculate the time the development started in relation of the previous release '''
    if srelease.prev_main_release:
        prev_release = srelease.prev_main_release
        return get_start(srelease) - get_release_time(prev_release)
    else:
        return datetime.timedelta(0)

def get_commits_in_advance(srelease):
    if not srelease.commits or not srelease.prev_main_release:
        return 0
    
    prev_release = srelease.prev_main_release
    return [commit for commit in srelease.commits if commit.author_time < get_release_time(prev_release)]

def is_rapid_release(release):    
    if not release.commits:
        return False
    if not release.prev_main_release:
        return False
    days = delta2days(get_cycle(release))
    if days <= 0:
        return False
    if days > RAPID_RELEASE_LIM:
        return False
    return True

def is_trad_release(release):
    if not release.commits:
        return False
    if not release.prev_main_release:
        return False
    days = delta2days(get_cycle(release))
    if days <= 0:
        return False
    if days < TRAD_RELEASE_LIM:
        return False
    return True
