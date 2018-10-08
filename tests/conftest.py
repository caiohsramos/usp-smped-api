from main import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = server.test_client()

    yield client


