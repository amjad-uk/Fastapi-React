from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_session
from ..repositories.user_repository import UserRepository
from ..services.user_service import UserService
def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))
