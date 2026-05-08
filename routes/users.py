from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models import User

from schemas import UserResponse

from dependencies import get_current_user
from dependencies import role_check


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
async def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user


@router.get(
    "/",
    response_model=list[UserResponse]
)
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(
        role_check(["admin"])
    )
):

    result = await db.scalars(
        select(User)
    )

    return result.all()
