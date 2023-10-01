from enum import Enum


class HealthGrade(Enum):
    HG_GOOD = 0
    HG_ALARM = 1
    HG_CRITICAL = 2


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1
