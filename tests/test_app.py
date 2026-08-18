import os
import sys
import tempfile

import pytest

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app


@pytest.fixture
def client():
    """Тестовый клиент Flask"""
    app.config['TESTING'] = True
    
    # Создаем временную директорию для статики
    temp_static = tempfile.mkdtemp()
    app.config['STATIC_FOLDER'] = temp_static
    
    # Создаем директорию, если её нет
    os.makedirs(temp_static, exist_ok=True)
    
    with app.test_client() as client:
        yield client
    
    # Очистка после тестов
    qr_path = os.path.join(temp_static, 'qr_code.png')
    if os.path.exists(qr_path):
        os.remove(qr_path)


def test_home_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200


def test_generate_qr(client):
    """Тест генерации QR-кода"""
    response = client.post('/', data={'data': 'https://test.com'})
    assert response.status_code == 200
    assert response.content_type == 'image/png'
    
    # qr_path = os.path.join(app.config['STATIC_FOLDER'], 'qr_code.png')
    # assert os.path.exists(qr_path)
    # assert os.path.getsize(qr_path) > 0


def test_generate_qr_empty_data(client):
    """Тест с пустыми данными"""
    response = client.post('/', data={'data': ''})
    # В зависимости от логики app.py
    assert response.status_code == 200 or response.status_code == 400


def test_generate_qr_missing_data(client):
    """Тест без данных"""
    response = client.post('/', data={})
    assert response.status_code == 400


def test_invalid_method(client):
    """Тест на неподдерживаемый метод"""
    response = client.put('/')
    assert response.status_code == 405  # Method Not Allowed