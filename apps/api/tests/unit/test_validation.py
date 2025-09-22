import pytest
from datetime import date, timedelta
from app.schemas.user import UserCreate

@pytest.mark.unit
def test_user_validation_ok():
    u = UserCreate(firstname="Alice", lastname="Smith", date_of_birth=date(1990,1,1))
    assert u.firstname == "Alice"

@pytest.mark.unit
def test_user_validation_bad_name():
    with pytest.raises(Exception):
        UserCreate(firstname="A", lastname="Smith", date_of_birth=date(1990,1,1))

@pytest.mark.unit
def test_user_validation_future_dob():
    with pytest.raises(Exception):
        UserCreate(firstname="Alice", lastname="Smith", date_of_birth=date.today() + timedelta(days=1))
