import json

def test_example(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert rv.status == '401 UNAUTHORIZED'

def test_get_token(client):
    rv = client.post('/auth/tokens', json={'username':'user','password':'password'})
    resp = json.loads(rv.data)
    assert resp['access_token'] and resp['refresh_token']

def test_get_refresh(client):
    rv = client.post('/auth/tokens', json={'username':'user','password':'password'})
    resp = json.loads(rv.data)
    refresh = resp['refresh_token']
    rv = client.post('/auth/refresh', json={'refresh_token': refresh})
    resp = json.loads(rv.data)
    assert resp['access_token']

def test_public_get(client):
    rv = client.get('/forms')
    resp = json.loads(rv.data)
    assert resp["_items"] 