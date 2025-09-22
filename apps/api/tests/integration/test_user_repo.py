import pytest
from datetime import date
from app.models.user import User

@pytest.mark.integration
def test_create_and_list_users(db_session):
    u = User(firstname="Bob", lastname="Brown", date_of_birth=date(1980,5,5))
    db_session.add(u)
    db_session.flush()
    rows = db_session.query(User).all()
    assert any(r.firstname == "Bob" for r in rows)
