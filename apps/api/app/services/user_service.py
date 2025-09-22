from ..repositories.user_repository import UserRepository
from ..domain.user import UserEntity
from ..core.errors import ServiceError
from ..schemas.user import calc_age

class UserService:
    def __init__(self, repo: UserRepository): self.repo = repo

    async def list_users(self) -> list[dict]:
        entities = await self.repo.list_users()
        return [self._to_out(e) for e in entities]

    async def create_user(self, data: dict) -> dict:
        entity = UserEntity(id=None, guid=data.get("guid"), firstname=data["firstname"], lastname=data["lastname"],
                            date_of_birth=data["date_of_birth"], created_at=data.get("created_at"), updated_at=data.get("updated_at"))
        created = await self.repo.create_user(entity)
        return self._to_out(created)

    async def update_user(self, id: int, patch: dict) -> dict:
        updated = await self.repo.update_user(id, patch)
        if not updated: raise ServiceError("user_not_found", 404)
        return self._to_out(updated)

    async def delete_user(self, id: int) -> None:
        ok = await self.repo.delete_user(id)
        if not ok: raise ServiceError("user_not_found", 404)

    def _to_out(self, e: UserEntity) -> dict:
        return {
            "id": e.id,
            "guid": e.guid,
            "firstname": e.firstname,
            "lastname": e.lastname,
            "date_of_birth": e.date_of_birth,
            "created_at": e.created_at,
            "updated_at": e.updated_at,
            "age": calc_age(e.date_of_birth),
        }
