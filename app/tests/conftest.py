import sys, os
sys.path.insert(0, os.path.abspath('..'))

from main import app
import pytest
import tempfile

@pytest.fixture
def client():
    #db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    #os.close(db_fd)
    #os.unlink(app.config['DATABASE'])

