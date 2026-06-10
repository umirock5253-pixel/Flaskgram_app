import pytest
from app import create_app, db
from app.models import User, Post
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        user1 = User(
            username='testuser',
            email='test@test.com',
            password=generate_password_hash('password123')
        )
        user2 = User(
            username='testuser2',
            email='test2@test.com',
            password=generate_password_hash('password123')
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        post = Post(content='Test post content', user_id=1)
        db.session.add(post)
        db.session.commit()
    yield

# ========================
# AUTH TESTS
# ========================

def test_register(client):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_register_duplicate_email(client, init_db):
    response = client.post('/auth/register', data={
        'username': 'anotheruser',
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already registered' in response.data

def test_login(client, init_db):
    response = client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_login_wrong_password(client, init_db):
    response = client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

# ========================
# POST TESTS
# ========================

def test_create_post(client, init_db):
    client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    response = client.post('/posts/create', data={
        'content': 'This is a test post'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Post created successfully' in response.data

def test_delete_post(client, init_db):
    client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    response = client.post('/posts/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Post deleted successfully' in response.data

def test_delete_post_unauthorized(client, init_db):
    client.post('/auth/login', data={
        'email': 'test2@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    response = client.post('/posts/delete/1', follow_redirects=True)
    assert response.status_code == 403

# ========================
# API TESTS
# ========================

def test_api_get_users(client, init_db):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_api_get_posts(client, init_db):
    response = client.get('/api/posts')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['content'] == 'Test post content'