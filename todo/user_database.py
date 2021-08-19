from .models import User
import motor.motor_asyncio
from fastapi import HTTPException, status
from .hashing import Hash

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')

database = client.TodoList
user_collections = database.users


async def check_user_email(user_email: str):
    data = await user_collections.find_one({'email': user_email})
    if data:
        return True
    return False


async def create_user(user: User):
    is_email_exists = await check_user_email(user.email)
    if not is_email_exists:
        document = User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
        result = await user_collections.insert_one(document.dict())
        data = await user_collections.find_one({'email': user.email})
        return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with email id {user.email} already exists'
    )


async def fetch_single_user(user_email: str, password: str):
    document = await user_collections.find_one({"email": user_email.strip()})
    if document:
        if not Hash.password_verify(document["password"], password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Password is incorrect'
            )
        return document
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Email is incorrect'
    )
