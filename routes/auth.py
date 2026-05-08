from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models import User

from schemas import UserCreate
from schemas import UserResponse
from schemas import Token

import security


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    existing_user = await db.scalar(
        select(User).where(
            User.username == data.username
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User(
        username=data.username,
        email=data.email,
        password=security.get_password_hash(
            data.password
        )
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    user = await db.scalar(
        select(User).where(
            User.username == form_data.username
        )
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Username yoki password xato"
        )

    if not security.verify_password(
        form_data.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Username yoki password xato"
        )

    access_token = security.create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
