from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID
@dataclass(slots=True)
class UserEntity:
    id: int | None
    guid: UUID
    firstname: str
    lastname: str
    date_of_birth: date
    created_at: datetime
    updated_at: datetime
