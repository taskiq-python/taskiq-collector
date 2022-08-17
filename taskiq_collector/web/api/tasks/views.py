from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import NonNegativeInt
from starlette import status

from taskiq_collector.db.models.task import TaskModel
from taskiq_collector.web.api.tasks.schema import SearchResult, UpdateModel

router = APIRouter()


@router.get("", response_model=SearchResult)
async def search(  # noqa: C901, WPS211
    task_name: Optional[str] = None,
    task_id: Optional[str] = None,
    completed: Optional[bool] = None,
    is_err: Optional[bool] = None,
    before_id: Optional[NonNegativeInt] = None,
    after_id: Optional[NonNegativeInt] = None,
    limit: int = Query(gt=0, le=100, default=20),  # noqa: WPS432
) -> SearchResult:
    """
    Search for tasks.

    :param task_name: name of the task
    :param task_id: task_id
    :param is_err: is_err task field
    :param completed: filter completed
        or not completed tasks.
    :param before_id: cursor location.
    :param after_id: cursor location.
    :param limit: maximum number of tasks.
    :return: Found tasks
    """
    queryset = TaskModel.objects
    if task_name is not None:
        queryset = queryset.filter(TaskModel.task_name.startswith(task_name))
    if task_id is not None:
        queryset = queryset.filter(TaskModel.task_id.startswith(task_id))
    if is_err is not None:
        queryset = queryset.filter(TaskModel.is_err == is_err)
    if completed is not None:
        queryset = queryset.filter(TaskModel.completed == completed)
    if before_id is not None:
        queryset = queryset.filter(TaskModel.id < before_id).order_by("-id")
    elif after_id is not None:
        queryset = queryset.filter(after_id < TaskModel.id).order_by("id")
    else:
        queryset = queryset.order_by("-id")
    has_next = False
    if await queryset.count() > limit:
        has_next = True
    return SearchResult(
        has_next=has_next,
        results=await queryset.limit(limit).all(),
    )


@router.put("")
async def save_task(task: TaskModel) -> None:
    """
    Create new task in the database.

    :param task: task json.
    :raises HTTPException: if values are incorrect.
    """
    try:
        # We remove supplied value to create new insted of updating old.
        task.id = None  # type: ignore
        await task.save()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.patch("/{task_id}")
async def modify_task(task_id: str, task_data: UpdateModel) -> None:
    """
    Update a task.

    :param task_id: id of a task.
    :param task_data: new data for the task.
    :raises HTTPException: if task not found,
        or if the task cannot be updated.
    """
    task = await TaskModel.objects.filter().get_or_none(TaskModel.task_id == task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task '{task_id}' not found.",
        )
    try:
        await task.update(**task_data.dict())
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{task_id}", response_model=TaskModel)
async def get_task(task_id: str) -> Optional[TaskModel]:
    """
    Retrieve task from the DB.

    :param task_id: id of a task.
    :return: task json or null.
    """
    return await TaskModel.objects.filter(TaskModel.task_id == task_id).get_or_none()


@router.delete("/{task_id}")
async def delete_task(task_id: str) -> None:
    """
    Delete task from the database.

    :param task_id: id of a task.
    """
    await TaskModel.objects.filter(TaskModel.task_id == task_id).delete()
