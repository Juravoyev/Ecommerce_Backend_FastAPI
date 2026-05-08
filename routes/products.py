import os
import shutil
import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models import Product
from models import Tag

from schemas import ProductResponse

from dependencies import role_check

from config import UPLOAD_FOLDER


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse
)
async def create_product(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    tag_ids: str = Form(""),
    image: UploadFile = File(None),

    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        role_check(["seller", "admin"])
    )
):

    image_name = None
    if image:
        ext = image.filename.split(".")[-1]
        image_name = f"{uuid.uuid4()}.{ext}"
        image_path = os.path.join(
            UPLOAD_FOLDER,
            image_name
        )

        with open(image_path, "wb") as buffer:

            shutil.copyfileobj(
                image.file,
                buffer
            )

    product = Product(
        title=title,
        description=description,
        price=price,
        image=image_name,
        category_id=category_id,
        owner_id=current_user.id
    )

    if tag_ids:

        ids = [
            int(tag_id)
            for tag_id in tag_ids.split(",")
        ]

        result = await db.scalars(
            select(Tag).where(
                Tag.id.in_(ids)
            )
        )

        product.tags = result.all()

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@router.get(
    "/",
    response_model=list[ProductResponse]
)
async def get_products(
    db: AsyncSession = Depends(get_db)
):

    result = await db.scalars(
        select(Product)
    )

    return result.all()


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),

    current_user=Depends(
        role_check(["admin", "seller"])
    )
):

    product = await db.scalar(
        select(Product).where(
            Product.id == product_id
        )
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product topilmadi"
        )

    if (
        current_user.role == "seller" and product.owner_id != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="Bu mahsulot sizga tegishli emas"
        )

    await db.delete(product)
    await db.commit()
    return {
        "message": "Product o'chirildi"
    }
