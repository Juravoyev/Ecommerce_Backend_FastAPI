from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models import Category

from schemas import CategoryCreate
from schemas import CategoryResponse

from dependencies import role_check


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(
        role_check(["admin"])
    )
):

    existing_category = await db.scalar(
        select(Category).where(
            Category.name == data.name
        )
    )

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    category = Category(
        name=data.name
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
async def get_categories(
    db: AsyncSession = Depends(get_db)
):

    result = await db.scalars(
        select(Category)
    )

    return result.all()
