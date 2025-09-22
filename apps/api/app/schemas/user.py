from pydantic import BaseModel, Field, field_validator
from datetime import date, date as ddate, datetime
import re
from uuid import UUID

MIN_DOB = date(1915,1,1)
NAME_RE = re.compile(r"^[A-Za-z]{2,20}$")

def calc_age(dob: date) -> int:
    today = ddate.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return years

class UserBase(BaseModel):
    firstname: str = Field(min_length=2, max_length=20)
    lastname: str = Field(min_length=2, max_length=20)
    date_of_birth: date

    @field_validator("firstname")
    @classmethod
    def v_first(cls, v: str):
        if not NAME_RE.fullmatch(v):
            raise ValueError("firstname_alpha_2_20")
        return v

    @field_validator("lastname")
    @classmethod
    def v_last(cls, v: str):
        if not NAME_RE.fullmatch(v):
            raise ValueError("lastname_alpha_2_20")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def v_dob(cls, v: date):
        if v < MIN_DOB:
            raise ValueError("dob_min_1915_01_01")
        if v > ddate.today():
            raise ValueError("dob_not_in_future")
        return v

class UserCreate(UserBase): pass

class UserUpdate(BaseModel):
    firstname: str | None = Field(default=None, min_length=2, max_length=20)
    lastname: str | None = Field(default=None, min_length=2, max_length=20)
    date_of_birth: date | None = None

    @field_validator("firstname")
    @classmethod
    def v_first(cls, v: str | None):
        if v is None: return v
        import re
        if not re.fullmatch(r"^[A-Za-z]{2,20}$", v):
            raise ValueError("firstname_alpha_2_20")
        return v

    @field_validator("lastname")
    @classmethod
    def v_last(cls, v: str | None):
        if v is None: return v
        import re
        if not re.fullmatch(r"^[A-Za-z]{2,20}$", v):
            raise ValueError("lastname_alpha_2_20")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def v_dob(cls, v: date | None):
        if v is None: return v
        from datetime import date as ddate
        if v < MIN_DOB:
            raise ValueError("dob_min_1915_01_01")
        if v > ddate.today():
            raise ValueError("dob_not_in_future")
        return v

class UserOut(BaseModel):
    id: int
    guid: UUID
    firstname: str
    lastname: str
    date_of_birth: date
    created_at: datetime
    updated_at: datetime
    age: int
