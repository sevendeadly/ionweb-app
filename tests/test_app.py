import pytest
from unittest.mock import patch, MagicMock
from backend.app import app, get_db_connection


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_endpoint_success(client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = ('Test User',)
    mock_conn.cursor.return_value = mock_cur

    with patch('backend.app.get_db_connection', return_value=mock_conn):
        response = client.get('/')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['message'] == 'Hello world, Test User'
        assert json_data['status'] == 'success'


def test_hello_endpoint_db_error(client):
    with patch('backend.app.get_db_connection', return_value=None):
        response = client.get('/')
        assert response.status_code == 500
        json_data = response.get_json()
        assert 'Database connection failed' in json_data['message']
