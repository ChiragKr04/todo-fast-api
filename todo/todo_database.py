from .models import Todo
# MongoDb Driver
import motor.motor_asyncio
from fastapi import HTTPException, status

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')

# Getting database(TodoList) in mongodb
database = client.TodoList

# Getting Table (collections() in mongodb) Like in database in mongodb
todo_collections = database.todo


async def fetch_single(todo_id: str):
    document = await todo_collections.find_one({'todo_id': todo_id})
    if document:
        return document
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Todo with id {todo_id} not found'
    )


async def get_all():
    print("get req")
    todos = []
    cursor = todo_collections.find({}).sort("_id", -1)
    async for document in cursor:
        todos.append(Todo(**document))
    return todos


async def create(todo):
    print("post req")
    document = todo
    result = await todo_collections.insert_one(document)
    return document


async def update(todo_id: str, response: Todo):
    await todo_collections.update_one(
        {"todo_id": todo_id},
        {"$set": {"title": response.title, "description": response.description}, },
    )
    document = await todo_collections.find_one({"todo_id": todo_id})
    return document


async def delete(todo_id: str):
    document = await todo_collections.find_one({'todo_id': todo_id})
    if document:
        res = await todo_collections.delete_one({'todo_id': todo_id})
        return True
    return False
