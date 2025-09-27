from app.auth.auth_handler import create_access_token, verify_token
from datetime import timedelta


def test_token_creation_and_verification():
    data = {"sub": "usuario_test"}
    token = create_access_token(data, expires_delta=timedelta(minutes=1))
    user = verify_token(token)
    assert user == "usuario_test"


def test_invalid_token():
    invalid_token = "abc.def.ghi"
    user = verify_token(invalid_token)
    assert user is None
