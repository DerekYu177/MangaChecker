"""
A collection of os specific tasks
"""
import os
from functools import wraps
import errno
import signal

PROJECT_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir))

def file_exists(file_location):
    """
    Checks whether the file exists
    """
    return os.path.isfile(file_location)

def get_project_folder():
    """
    Allows other modules to import the project folder
    """
    return PROJECT_FOLDER

def is_file_empty(file_location):
    """
    Checks whether the file is empty
    (Holds no data)
    """
    if not file_exists(file_location):
        return True

    return os.stat(file_location).st_size == 0

def clear_file(file_location):
    """
    Delete
    """
    if not file_exists(file_location):
        return

    os.remove(file_location)

def find(project_location):
    """
    Computes the full path of a file
    based on it's relative position to the
    PROJECT_FOLDER
    """
    return os.path.join(
        PROJECT_FOLDER,
        project_location
    )

class TimeoutError(Exception):
    """
    Just an error that we raise when we timeout
    """
    pass

def timeout(seconds=2, error_message=os.strerror(errno.ETIMEDOUT)):
    def decorator(func):
        def _handle_timeout(_signum, _frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)

            return result
        return wraps(func)(wrapper)
    return decorator
