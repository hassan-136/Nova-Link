"""
Complete Integration Test Suite for VPN Core
Run this to verify everything works before team integration
"""
import requests
import json
import time
from colorama import init, Fore, Style

init(autoreset=True)

BASE_URL = 'http://localhost:5000/api'


def print_test(test_name):
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}{test_name}")
    print(f"{Fore.CYAN}{'=' * 60}")


def print_success(message):
    print(f"{Fore.GREEN}✓ {message}")


def print_error(message):
    print(f"{Fore.RED}✗ {message}")


def test_health_check():
    print_test("TEST 1: Health Check")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is healthy: {data['service']}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Connection failed: {e}")
        return False


def test_server_info():
    print_test("TEST 2: Server Information")
    try:
        response = requests.get(f'{BASE_URL}/server/info')
        data = response.json()
        print_success("Server Info Retrieved:")
        print(f"  Server Public Key: {data['server_public_key'][:40]}...")
        print(f"  Server IP: {data['server_ip']}")
        print(f"  Server Port: {data['server_port']}")
        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def test_tunnel_status():
    print_test("TEST 3: Tunnel Status")
    try:
        response = requests.get(f'{BASE_URL}/tunnel/status')
        data = response.json()
        print_success(f"Tunnel Status: {data['tunnel']['status']}")
        print(f"  Active Peers: {data['tunnel']['active_peers']}")
        print(f"  IP Utilization: {data['ip_pool']['utilization']}")
        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def test_client_registration():
    print_test("TEST 4: Client Registration Flow")
    try:
        # Register client 1
        response = requests.post(f'{BASE_URL}/client/register', json={
            'client_id': 'integration_test_1',
            'client_name': 'Integration Test Client 1'
        })
        data = response.json()

        if data['success']:
            print_success(f"Client 1 registered: {data['ip_address']}")
        else:
            print_error("Client 1 registration failed")
            return False

        # Register client 2
        response = requests.post(f'{BASE_URL}/client/register', json={
            'client_id': 'integration_test_2',
            'client_name': 'Integration Test Client 2'
        })
        data = response.json()

        if data['success']:
            print_success(f"Client 2 registered: {data['ip_address']}")
        else:
            print_error("Client 2 registration failed")
            return False

        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def test_ip_management():
    print_test("TEST 5: IP Address Management")
    try:
        # Get IP stats
        response = requests.get(f'{BASE_URL}/ip/stats')
        stats = response.json()
        print_success("IP Pool Statistics:")
        print(f"  Total IPs: {stats['total_ips']}")
        print(f"  Allocated: {stats['allocated']}")
        print(f"  Available: {stats['available']}")
        print(f"  Utilization: {stats['utilization']}")

        # List allocations
        response = requests.get(f'{BASE_URL}/ip/list')
        data = response.json()
        print_success(f"Total Allocations: {data['count']}")

        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def test_peer_management():
    print_test("TEST 6: Peer Management")
    try:
        response = requests.get(f'{BASE_URL}/peer/list')
        data = response.json()
        print_success(f"Active Peers: {data['count']}")

        for peer in data['peers']:
            print(f"  - {peer['client_id']}: {peer['allowed_ip']}")

        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def test_tunnel_control():
    print_test("TEST 7: Tunnel Start/Stop Control")
    try:
        # Stop tunnel
        response = requests.post(f'{BASE_URL}/tunnel/stop')
        data = response.json()
        if data['success']:
            print_success("Tunnel stopped successfully")

        time.sleep(1)

        # Start tunnel
        response = requests.post(f'{BASE_URL}/tunnel/start')
        data = response.json()
        if data['success']:
            print_success("Tunnel started successfully")

        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def test_cleanup():
    print_test("TEST 8: Cleanup Test Clients")
    try:
        # Unregister test clients
        for client_id in ['integration_test_1', 'integration_test_2']:
            response = requests.post(f'{BASE_URL}/client/unregister', json={
                'client_id': client_id
            })
            if response.json()['success']:
                print_success(f"Cleaned up: {client_id}")

        return True
    except Exception as e:
        print_error(f"Failed: {e}")
        return False


def main():
    print(f"\n{Fore.YELLOW}{'=' * 60}")
    print(f"{Fore.YELLOW}  NOVA-LINK VPN CORE - INTEGRATION TEST SUITE")
    print(f"{Fore.YELLOW}{'=' * 60}\n")

    print(f"{Fore.CYAN}Testing API at: {BASE_URL}")
    print(f"{Fore.YELLOW}Make sure the API server is running!\n")

    time.sleep(2)

    tests = [
        ("Health Check", test_health_check),
        ("Server Info", test_server_info),
        ("Tunnel Status", test_tunnel_status),
        ("Client Registration", test_client_registration),
        ("IP Management", test_ip_management),
        ("Peer Management", test_peer_management),
        ("Tunnel Control", test_tunnel_control),
        ("Cleanup", test_cleanup),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append((test_name, False))
        time.sleep(1)

    # Summary
    print(f"\n{Fore.YELLOW}{'=' * 60}")
    print(f"{Fore.YELLOW}  TEST SUMMARY")
    print(f"{Fore.YELLOW}{'=' * 60}\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{Fore.GREEN}PASSED" if result else f"{Fore.RED}FAILED"
        print(f"  {test_name:<30} {status}")

    print(f"\n{Fore.CYAN}Results: {passed}/{total} tests passed")

    if passed == total:
        print(f"\n{Fore.GREEN}{'=' * 60}")
        print(f"{Fore.GREEN}  ✓ ALL TESTS PASSED!")
        print(f"{Fore.GREEN}  Your VPN Core is ready for team integration!")
        print(f"{Fore.GREEN}{'=' * 60}\n")
    else:
        print(f"\n{Fore.RED}{'=' * 60}")
        print(f"{Fore.RED}  ✗ Some tests failed. Please fix before integration.")
        print(f"{Fore.RED}{'=' * 60}\n")


if __name__ == '__main__':
    main()