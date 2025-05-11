from . import db
from .models import AddTaskRequestModel
from .models.responses import SimpleResponse, ManyTasksResponse, OneTaskResponse
from .db_models import Task
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError, NoResultFound


def try_add_new_task(task_data: AddTaskRequestModel, user_id:int, parent_task_id: Optional[int] = None) ->SimpleResponse:
    if not isinstance(task_data, AddTaskRequestModel):
        err = TypeError("Provided task_data is not instance of AddTaskRequestModel")
        return SimpleResponse(False, str(err), err)

    new_task = Task(
        title=task_data.title,
        importance=task_data.importance,
        deadline=task_data.deadline,
        est_time_days=task_data.est_time_days,
        description=task_data.description,
        user_id=user_id,
        parent_task_id=parent_task_id
    )
    try:
        db.session.add(new_task)
        db.session.commit()
        assigned_id = new_task.id
        return SimpleResponse(True, str(assigned_id))
    except SQLAlchemyError as e:
        db.session.rollback()
        return SimpleResponse(False, str(e), e)

def try_getting_user_tasks(user_id: int) -> ManyTasksResponse:
    if not isinstance(user_id, int):
        err = TypeError("Provided user_id is not an instance of int")
        return ManyTasksResponse(False, str(err), err)

    try:
        tasks = Task.query.filter_by(user_id=user_id).all()
        tasks_formatted = []
        for task in tasks:
            tasks_formatted.append(task.to_dict())
        return ManyTasksResponse(True, tasks=tasks_formatted)
    except NoResultFound as nrf:
        db.session.rollback()
        return ManyTasksResponse(False, f'No tasks found for user {user_id}', nrf)
    except SQLAlchemyError as e:
        db.session.rollback()
        return ManyTasksResponse(False, str(e), e)

def try_getting_specific_task(user_id: int, task_id: int) -> OneTaskResponse:
    if not isinstance(task_id, int) or not isinstance(user_id, int):
        err = TypeError("At least one of provided id's is not an instance of int")
        return OneTaskResponse(False, str(err), err)

    try:
        task = Task.query.filter_by(user_id=user_id, id=task_id).one()
        task_dict = task.to_dict()
        return OneTaskResponse(True, task=task_dict)
    except NoResultFound as nrf:
        return OneTaskResponse(False, f'No task with id {task_id} found in your account', nrf)
    except SQLAlchemyError as e:
        return OneTaskResponse(False, str(e), e)