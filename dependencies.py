import jwt
import security

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati tugagan"
    )

    try:

        payload = security.decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await db.scalar(
        select(User).where(
            User.id == int(user_id)
        )
    )

    if user is None:
        raise credentials_exception

    return user


def role_check(required_roles: list):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role not in required_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ruxsat etilmagan"
            )

        return current_user

    return role_checker
