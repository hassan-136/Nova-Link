"""
Unit tests for IP Allocator
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ip_allocator import IPAllocator


def test_allocate_ip():
    """Test IP allocation"""
    allocator = IPAllocator(db_path='test_ip_pool.json')

    # Allocate IP
    ip = allocator.allocate_ip('test_client_1', 'Test Client')
    assert ip == '10.8.0.2'

    # Allocate another IP
    ip2 = allocator.allocate_ip('test_client_2', 'Test Client 2')
    assert ip2 == '10.8.0.3'

    # Clean up
    os.remove('test_ip_pool.json')


def test_release_ip():
    """Test IP release"""
    allocator = IPAllocator(db_path='test_ip_pool.json')

    # Allocate and release
    ip = allocator.allocate_ip('test_client', 'Test')
    success = allocator.release_ip('test_client')
    assert success == True

    # Try to release non-existent client
    success = allocator.release_ip('non_existent')
    assert success == False

    # Clean up
    os.remove('test_ip_pool.json')


def test_get_stats():
    """Test statistics"""
    allocator = IPAllocator(db_path='test_ip_pool.json')

    stats = allocator.get_stats()
    assert stats['total_ips'] == 253
    assert stats['allocated'] == 0
    assert stats['available'] == 253

    # Clean up
    os.remove('test_ip_pool.json')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])