"""
IP Address Allocator
Manages VPN client IP address allocation and tracking
"""
import os
from tinydb import TinyDB, Query
from datetime import datetime


class IPAllocator:
    def __init__(self, db_path='../config/ip_pool.json'):
        """Initialize IP allocator with TinyDB database"""
        # Get absolute path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_path)

        # Create directory if needed
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Initialize database
        self.db = TinyDB(self.db_path)
        self.allocations = self.db.table('allocations')

        # IP pool configuration
        self.subnet = '10.8.0.0/24'
        self.start_ip = 2  # 10.8.0.1 is server
        self.end_ip = 254

        # Initialize IP pool if empty
        if len(self.allocations) == 0:
            self._initialize_pool()

    def _initialize_pool(self):
        """Initialize available IP pool"""
        available_ips = list(range(self.start_ip, self.end_ip + 1))
        self.db.insert({'available_ips': available_ips})

    def _get_available_ips(self):
        """Get list of available IPs"""
        pool = self.db.get(doc_id=1)
        if pool:
            return pool.get('available_ips', [])
        return []

    def _update_available_ips(self, ips):
        """Update available IP list"""
        self.db.update({'available_ips': ips}, doc_ids=[1])

    def allocate_ip(self, client_id, client_name='Unknown'):
        """Allocate an IP address to a client"""
        # Check if client already has an IP
        Client = Query()
        existing = self.allocations.search(Client.client_id == client_id)

        if existing:
            return existing[0]['ip_address']

        # Get available IPs
        available_ips = self._get_available_ips()

        if not available_ips:
            raise Exception("No available IP addresses in the pool")

        # Allocate first available IP
        ip_suffix = available_ips.pop(0)
        ip_address = f"10.8.0.{ip_suffix}"

        # Save allocation
        self.allocations.insert({
            'client_id': client_id,
            'client_name': client_name,
            'ip_address': ip_address,
            'allocated_at': datetime.now().isoformat(),
            'status': 'active'
        })

        # Update available IPs
        self._update_available_ips(available_ips)

        return ip_address

    def release_ip(self, client_id):
        """Release an IP address back to the pool"""
        Client = Query()
        allocation = self.allocations.search(Client.client_id == client_id)

        if not allocation:
            return False

        # Get IP suffix
        ip_address = allocation[0]['ip_address']
        ip_suffix = int(ip_address.split('.')[-1])

        # Add back to available pool
        available_ips = self._get_available_ips()
        available_ips.append(ip_suffix)
        available_ips.sort()
        self._update_available_ips(available_ips)

        # Remove allocation
        self.allocations.remove(Client.client_id == client_id)

        return True

    def get_client_ip(self, client_id):
        """Get IP address for a specific client"""
        Client = Query()
        allocation = self.allocations.search(Client.client_id == client_id)

        if allocation:
            return allocation[0]['ip_address']
        return None

    def list_allocations(self):
        """List all current IP allocations"""
        return self.allocations.all()

    def get_stats(self):
        """Get allocation statistics"""
        available = len(self._get_available_ips())
        allocated = len(self.allocations)
        total = self.end_ip - self.start_ip + 1

        return {
            'total_ips': total,
            'allocated': allocated,
            'available': available,
            'utilization': f"{(allocated / total) * 100:.1f}%"
        }


# Test the allocator
if __name__ == '__main__':
    allocator = IPAllocator()

    print("🧪 Testing IP Allocator...")

    # Test allocation
    ip1 = allocator.allocate_ip('client_001', 'Test Client 1')
    print(f"✅ Allocated IP: {ip1}")

    ip2 = allocator.allocate_ip('client_002', 'Test Client 2')
    print(f"✅ Allocated IP: {ip2}")

    # Test stats
    stats = allocator.get_stats()
    print(f"📊 Stats: {stats}")

    # Test release
    allocator.release_ip('client_001')
    print("✅ Released IP for client_001")

    # List allocations
    print("\n📋 Current Allocations:")
    for allocation in allocator.list_allocations():
        print(f"  {allocation['client_id']}: {allocation['ip_address']}")