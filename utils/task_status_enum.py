from enum import Enum

class TaskStatus(Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'