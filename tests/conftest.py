from main import server
import pytest

@pytest.fixture
def client():
    server.config['TESTING'] = True
    client = server.test_client()

    yield client


