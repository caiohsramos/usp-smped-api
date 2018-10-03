from api.auth.utility import generate_tokens
import jwt

def test_generate():
    user = "username"
    roles = ["admin", "superuser"]

    access_token, refresh_token = generate_tokens(user, roles)
    assert isinstance(access_token, str) and isinstance(refresh_token, str)   
    assert access_token != "" and refresh_token != ""

def test_decode():
    user = "username"
    roles = ["admin", "superuser"]

    access_token, _ = generate_tokens(user, roles)
    assert jwt.decode(access_token, verify=False)["username"] == user
    assert jwt.decode(access_token, verify=False)["role"] == roles
    
