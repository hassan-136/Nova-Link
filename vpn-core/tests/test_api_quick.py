import requests
import json

BASE_URL = 'http://localhost:5000/api'

print("🧪 Testing Nova-Link VPN Core API...\n")

# Test 1: Health Check
print("1️⃣ Health Check:")
response = requests.get(f'{BASE_URL}/health')
print(json.dumps(response.json(), indent=2))

# Test 2: Server Info
print("\n2️⃣ Server Info:")
response = requests.get(f'{BASE_URL}/server/info')
print(json.dumps(response.json(), indent=2))

# Test 3: Tunnel Status
print("\n3️⃣ Tunnel Status:")
response = requests.get(f'{BASE_URL}/tunnel/status')
print(json.dumps(response.json(), indent=2))

# Test 4: Register a Client
print("\n4️⃣ Registering Test Client:")
response = requests.post(f'{BASE_URL}/client/register', json={
    'client_id': 'test_client_001',
    'client_name': 'Test Client Windows'
})
print(json.dumps(response.json(), indent=2))

# Test 5: List Allocations
print("\n5️⃣ IP Allocations:")
response = requests.get(f'{BASE_URL}/ip/list')
print(json.dumps(response.json(), indent=2))

print("\n✅ All tests completed!")