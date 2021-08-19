from fastapi import APIRouter, HTTPException, status, Depends
from ..user_database import fetch_single_user
from .. import token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication'],
    prefix='/login'
)


@router.post('/')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = await fetch_single_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Email or password is incorrect'
        )

    access_token = token.create_access_token(data={"sub": user['email']})
    return {"access_token": access_token, "token_type": "bearer"}
