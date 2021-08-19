from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from todo.routers import todo, user, authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(todo.router)
app.include_router(user.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get('/')
def index():
    return {
        'msg': 'working'
    }
