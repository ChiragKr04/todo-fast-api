from fastapi import APIRouter, HTTPException, status
from ..user_database import create_user, fetch_single_user
from ..models import User

router = APIRouter(
    tags=['User'],
    prefix='/api/user'
)


@router.post('/')
async def post_user(user: User):
    response = await create_user(user)
    if response:
        return {
            "id": str(response["_id"]),
            'name': str(response['name']),
            'email': str(response['email']),
            'password': str(response['password'])
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with email id {user.email} already exists'
    )


@router.get('/{user_email}/{password}')
async def get_user(user_email: str, password: str):
    response = await fetch_single_user(user_email, password)
    if response:
        return {
            "id": str(response["_id"]),
            'name': str(response['name']),
            'email': str(response['email']),
            'password': str(response['password'])
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Email or password is incorrect'
    )
