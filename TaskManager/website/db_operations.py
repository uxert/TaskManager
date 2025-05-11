from . import db
from .models import AddTaskRequestModel, TargetSpecificTaskModel
from .models.responses import SimpleResponse
from .db_models import Task
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError



def try_add_new_task(task_data: AddTaskRequestModel, user_id:int, parent_task_id: Optional[int] = None) ->SimpleResponse:
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

