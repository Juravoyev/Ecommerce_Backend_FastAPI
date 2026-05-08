from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models import Tag

from schemas import TagCreate
from schemas import TagResponse

from dependencies import role_check


router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)


@router.post(
    "/",
    response_model=TagResponse
)
async def create_tag(
    data: TagCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(
        role_check(["admin"])
    )
):

    existing_tag = await db.scalar(
        select(Tag).where(
            Tag.name == data.name
        )
    )

    if existing_tag:
        raise HTTPException(
            status_code=400,
            detail="Tag already exists"
        )

    tag = Tag(
        name=data.name
    )

    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


@router.get(
    "/",
    response_model=list[TagResponse]
)
async def get_tags(
    db: AsyncSession = Depends(get_db)
):

    result = await db.scalars(
        select(Tag)
    )

    return result.all()
