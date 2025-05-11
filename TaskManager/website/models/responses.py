"""This file is meant to contain various responses available throughout the project.
One may be responses from API, other internal server messages - we will see"""
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class SimpleResponse:
    """ Simple dataclass that will allow to pass results from database functions - status and error explanation"""
    success: bool
    message: str = ''
    exception: Exception = None

@dataclass(frozen=True)
class ManyTasksResponse(SimpleResponse):
    """
    Inherits from SimpleResponse and extends it by one additional field - tasks. It's a list of dicts for easy JSON
    serializaiton
    """
    tasks: list[dict] = None

class TerminalAPIResponse(BaseModel):
    status: str
    result: str