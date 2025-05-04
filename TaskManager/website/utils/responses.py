"""This file is meant to contain various responses available throughout the project.
One may be responses from API, other internal server messages - we will see"""
from typing import NamedTuple

class SimpleResponse(NamedTuple):
    """ Simple NamedTuple that will allow to pass results from database functions - status and error explanation"""
    success: bool
    message: str = ''
    exception: Exception = None