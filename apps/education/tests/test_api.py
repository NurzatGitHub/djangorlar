import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.education.models import Course, Lesson

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
@pytest.mark.django_db
def test_course_list_success(api_client, test_user):
    # Good data test
    api_client.force_authenticate(user=test_user)
    response = api_client.get('/api/education/courses/')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    
@pytest.mark.django_db
def test_course_create_success(api_client, test_user):
    """Good data test - create course"""
    api_client.force_authenticate(user=test_user)
    data = {'title': 'Test Course', 'description': 'Test Description'}
    response = api_client.post('/api/education/courses/', data)
    print("Response status:", response.status_code) 
    print("Response data:", response.data)
    assert response.status_code == 201
    assert response.data['title'] == 'Test Course'

@pytest.mark.django_db  
def test_course_create_bad_data(api_client, test_user):
    """Bad data test - missing title"""
    api_client.force_authenticate(user=test_user)
    data = {'description': 'Test Description'}  # No title
    response = api_client.post('/api/education/courses/', data)
    assert response.status_code == 400  # Bad request

@pytest.mark.django_db
def test_course_list_unauthorized(api_client):
    """Bad data test - no authentication"""
    response = api_client.get('/api/education/courses/')
    assert response.status_code == 401  # Unauthorized
    
@pytest.fixture
def test_course(test_user):
    return Course.objects.create(
        title='Test Course',
        description='Test Description',
        owner=test_user
    )
    
@pytest.mark.django_db
def test_lesson_create_success(api_client, test_user, test_course):
    """Good data test - create lesson"""
    api_client.force_authenticate(user=test_user)
    data = {
        'title': 'Test Lesson',
        'content': 'Lesson Content',
        'course': test_course.id
    }
    response = api_client.post('/api/education/lessons/', data)
    assert response.status_code == 201
    assert response.data['title'] == 'Test Lesson'
    
@pytest.mark.django_db
def test_lesson_create_bad_data(api_client, test_user):
    """Bad data test - missing title"""
    api_client.force_authenticate(user=test_user)
    data = {
        'title': 'Test Lesson',
        'content': 'Test Content',
    }
    response = api_client.post('/api/education/lessons/', data)
    assert response.status_code == 400  # Bad request
    
@pytest.fixture
def test_lesson(test_user, test_course):
    return Lesson.objects.create(
        title='Test Lesson',
        content='Lesson Content',
        course=test_course,
    )
    
@pytest.mark.django_db
def test_lesson_publish_success(api_client, test_user, test_lesson):
    """Good data test - publish lesson"""
    api_client.force_authenticate(user=test_user)
    response = api_client.post(f'/api/education/lessons/{test_lesson.id}/publish/')
    assert response.status_code == 200
    assert response.data['is_published'] == True
    
@pytest.mark.django_db
def test_lesson_publish_unauthorized(api_client, test_lesson):
    """Bad data test - unauthorized publish attempt"""
    response = api_client.post(f'/api/education/lessons/{test_lesson.id}/publish/')
    assert response.status_code == 401  # Unauthorized
    
@pytest.mark.django_db
def test_lesson_unpublish_success(api_client, test_user, test_lesson):
    
    api_client.force_authenticate(user=test_user)
    response = api_client.post(f'/api/education/lessons/{test_lesson.id}/unpublish/')
    assert response.status_code == 200
    assert response.data['is_published'] == False
    
@pytest.mark.django_db
def test_lesson_delete_success(api_client, test_user, test_lesson):
    """Good data test - delete lesson"""
    api_client.force_authenticate(user=test_user)
    response = api_client.delete(f'/api/education/lessons/{test_lesson.id}/')
    assert response.status_code == 204  # No content
    
@pytest.mark.django_db
def test_lesson_delete_not_found(api_client, test_user):
    """Bad data test - delete non-existent lesson"""
    api_client.force_authenticate(user=test_user)
    response = api_client.delete('/api/education/lessons/9999/')
    assert response.status_code == 404  # Not found
    
@pytest.mark.django_db
def test_lesson_move_success(api_client, test_user, test_lesson):
    """Good data test - move lesson"""
    api_client.force_authenticate(user=test_user)
    data = {'before_lesson_id': None}
    response = api_client.put(
        f'/api/education/lessons/{test_lesson.id}/move/', 
        data, 
        format='json'  # Force JSON format
    )
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_jwt_token_success(api_client, test_user):
    """Good data test - obtain JWT token"""
    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    response = api_client.post('/api/token/', data)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_jwt_token_bad_credentials(api_client):
    """Bad data test - invalid credentials for JWT token"""
    data = {
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }
    response = api_client.post('/api/token/', data)
    assert response.status_code == 401

@pytest.mark.django_db
def test_jwt_token_refresh_success(api_client, test_user):
    """Good data test - refresh JWT token"""
    # First obtain token
    data = {
        'email': 'test@example.com', 'password': 'testpass123'}
    token_response = api_client.post('/api/token/', data)
    refresh_token = token_response.data['refresh']
    
    # then refresh it
    refresh_data = {'refresh': refresh_token}
    response = api_client.post('/api/token/refresh/', refresh_data)
    assert response.status_code == 200
    assert 'access' in response.data