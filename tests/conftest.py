from app.main import server
import pytest
import tempfile

@pytest.fixture
def client():
    #db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    server.config['TESTING'] = True
    client = server.test_client()

    yield client

    #os.close(db_fd)
    #os.unlink(app.config['DATABASE'])

