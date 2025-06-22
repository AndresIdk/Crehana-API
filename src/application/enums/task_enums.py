from enum import Enum


class TaskStatus(str, Enum):
    pending = "Pending"
    in_progress = "In Progress"
    completed = "Completed"


class TaskPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class TaskCompleteness(str, Enum):
    not_started = "0%"
    in_progress = "50%"
    completed = "100%"
