"""
API Integration Tests
"""
import pytest
import requests
import time

BASE_URL = 'http://localhost:5000/api'


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f'{BASE_URL}/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'


def test_server_info():
    """Test server info endpoint"""
    response = requests.get(f'{BASE_URL}/server/info')
    assert response.status_code == 200
    data = response.json()
    assert 'server_public_key' in data


def test_client_registration():
    """Test client registration flow"""
    # Register client
    payload = {
        'client_id': 'api_test_client',
        'client_name': 'API Test Client'
    }
    response = requests.post(f'{BASE_URL}/client/register', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert 'ip_address' in data

    # Unregister client
    response = requests.post(f'{BASE_URL}/client/unregister', json=payload)
    assert response.status_code == 200


def test_tunnel_control():
    """Test tunnel start/stop"""
    # Start tunnel
    response = requests.post(f'{BASE_URL}/tunnel/start')
    assert response.status_code == 200

    # Get status
    response = requests.get(f'{BASE_URL}/tunnel/status')
    assert response.status_code == 200
    data = response.json()
    assert data['tunnel']['status'] == 'active'

    # Stop tunnel
    response = requests.post(f'{BASE_URL}/tunnel/stop')
    assert response.status_code == 200


if __name__ == '__main__':
    print("⚠️ Make sure API server is running before testing!")
    print("Run: python vpn-core/api/app.py")
    time.sleep(2)
    pytest.main([__file__, '-v'])