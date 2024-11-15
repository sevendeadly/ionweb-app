# tests/conftest.py
import pytest
from backend.app import app, get_db_connection
import psycopg2
from unittest.mock import MagicMock, patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    return mock_conn, mock_cur


# tests/test_app.py
def test_hello_endpoint_success(client, mock_db_connection):
    mock_conn, mock_cur = mock_db_connection
    mock_cur.fetchone.return_value = ('Test User',)

    with patch('backend.app.get_db_connection', return_value=mock_conn):
        response = client.get('/')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['message'] == 'Hello world, Test User'
        assert json_data['status'] == 'success'


def test_hello_endpoint_no_data(client, mock_db_connection):
    mock_conn, mock_cur = mock_db_connection
    mock_cur.fetchone.return_value = None

    with patch('backend.app.get_db_connection', return_value=mock_conn):
        response = client.get('/')
        assert response.status_code == 404
        json_data = response.get_json()
        assert 'No name found' in json_data['message']


def test_hello_endpoint_db_connection_error(client):
    with patch('backend.app.get_db_connection', return_value=None):
        response = client.get('/')
        assert response.status_code == 500
        json_data = response.get_json()
        assert 'Database connection failed' in json_data['message']


def test_hello_endpoint_db_query_error(client, mock_db_connection):
    mock_conn, mock_cur = mock_db_connection
    mock_cur.execute.side_effect = psycopg2.Error("Database error")

    with patch('backend.app.get_db_connection', return_value=mock_conn):
        response = client.get('/')
        assert response.status_code == 500
        json_data = response.get_json()
        assert 'Internal server error' in json_data['message']


def test_get_db_connection_success():
    mock_connect = MagicMock()

    with patch('psycopg2.connect', mock_connect):
        connection = get_db_connection()
        assert connection is not None
        mock_connect.assert_called_once()


def test_get_db_connection_failure():
    with patch('psycopg2.connect', side_effect=psycopg2.Error("Connection error")):
        connection = get_db_connection()
        assert connection is None