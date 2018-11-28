from api.auth.utility import generate_tokens
import jwt

def test_generate():
    user = "username"
    roles = ["admin", "superuser"]

    access_token, refresh_token = generate_tokens(user, roles, True)
    assert isinstance(access_token, str) and isinstance(refresh_token, str)   
    assert access_token != "" and refresh_token != ""

def test_decode():
    user = "username"
    roles = ["admin", "superuser"]

    #first login true
    access_token, _ = generate_tokens(user, roles, True)
    assert jwt.decode(access_token, verify=False)["username"] == user
    assert jwt.decode(access_token, verify=False)["role"] == roles
    assert jwt.decode(access_token, verify=False)["first_login"] == True
    
    #first login false
    access_token, _ = generate_tokens(user, roles, False)
    assert jwt.decode(access_token, verify=False)["username"] == user
    assert jwt.decode(access_token, verify=False)["role"] == roles
    assert jwt.decode(access_token, verify=False)["first_login"] == False
    
