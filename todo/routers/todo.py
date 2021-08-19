from fastapi import APIRouter, HTTPException, status, Depends
from ..todo_database import get_all, create, update, delete, fetch_single
from ..models import Todo
from .. import oauth2

router = APIRouter(
    tags=['Todo'],
    prefix='/api/todo'
)


@router.get('/')
async def get_all_todo(current_user: Todo = Depends(oauth2.get_current_user)):
    response = await get_all()
    return {
        "data": response
    }


@router.get('/{todo_id}', response_model=Todo)
async def get_single_todo(todo_id: str):
    response = await fetch_single(todo_id)
    if response:
        return response
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Todo with title {todo_id} not found'
    )


@router.post('/', response_model=Todo)
async def create_todo(todo: Todo):
    response = await create(todo.dict())
    if response:
        return response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Failed to create a Todo'
    )


@router.put('/{todo_id}', response_model=Todo)
async def update_todo(todo_id: str, response: Todo):
    response = await update(todo_id, response)
    if response:
        return response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Failed to update Todo'
    )


@router.delete('/{todo_id}')
async def delete_todo(todo_id: str):
    response = await delete(todo_id)
    if response:
        return {
            "detail": "Todo deleted",
            "success_code": 200
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "detail": "Todo failed to deleted",
            "success_code": 400
        }
    )
