from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.user import User
from ..domain.user import UserEntity

class UserRepository:
    def __init__(self, session: AsyncSession): self.session = session

    async def list_users(self) -> list[UserEntity]:
        res = await self.session.execute(select(User).order_by(User.id.desc()))
        rows = res.scalars().all()
        return [UserEntity(
            id=r.id, guid=r.guid, firstname=r.firstname, lastname=r.lastname,
            date_of_birth=r.date_of_birth, created_at=r.created_at, updated_at=r.updated_at
        ) for r in rows]

    async def create_user(self, u: UserEntity) -> UserEntity:
        row = User(firstname=u.firstname, lastname=u.lastname, date_of_birth=u.date_of_birth)
        self.session.add(row); await self.session.commit(); await self.session.refresh(row)
        return UserEntity(id=row.id, guid=row.guid, firstname=row.firstname, lastname=row.lastname,
                          date_of_birth=row.date_of_birth, created_at=row.created_at, updated_at=row.updated_at)

    async def update_user(self, id: int, data: dict) -> UserEntity | None:
        res = await self.session.execute(select(User).where(User.id == id))
        row = res.scalar_one_or_none()
        if not row: return None
        for k, v in data.items():
            setattr(row, k, v)
        await self.session.commit(); await self.session.refresh(row)
        return UserEntity(id=row.id, guid=row.guid, firstname=row.firstname, lastname=row.lastname,
                          date_of_birth=row.date_of_birth, created_at=row.created_at, updated_at=row.updated_at)

    async def delete_user(self, id: int) -> bool:
        res = await self.session.execute(delete(User).where(User.id == id))
        deleted = res.rowcount or 0; await self.session.commit(); return deleted > 0
