"""
Spaceship DNS Management for Oriz
"""

import requests
import hmac
import hashlib
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import SPACESHIP, DOMAIN


def get_auth_headers():
    """Generate authentication headers for Spaceship API"""
    timestamp = str(int(time.time()))

    # Create HMAC signature
    message = f"{SPACESHIP['api_key']}{timestamp}"
    signature = hmac.new(
        SPACESHIP['api_secret'].encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return {
        'X-Api-Key': SPACESHIP['api_key'],
        'X-Timestamp': timestamp,
        'X-Signature': signature,
        'Content-Type': 'application/json'
    }


def list_domains():
    """List all domains in Spaceship account"""
    url = f"{SPACESHIP['api_url']}/domains"

    try:
        response = requests.get(url, headers=get_auth_headers())
        result = response.json()

        if response.status_code == 200:
            domains = result.get('items', [])
            print(f"\n📋 Domains ({len(domains)} total):")
            for domain in domains:
                print(f"   {domain.get('name', 'Unknown')}")
            return domains
        else:
            print(f"❌ Error: {result}")
            return []
    except Exception as e:
        print(f"❌ API error: {e}")
        return []


def get_dns_records(domain: str):
    """Get DNS records for a domain"""
    url = f"{SPACESHIP['api_url']}/dns/{domain}/records"

    try:
        response = requests.get(url, headers=get_auth_headers())
        result = response.json()

        if response.status_code == 200:
            records = result.get('items', [])
            print(f"\n📋 DNS Records for {domain} ({len(records)} total):")
            for record in records:
                print(f"   {record['type']:6} {record['host']:30} → {record['value'][:50]}")
            return records
        else:
            print(f"❌ Error: {result}")
            return []
    except Exception as e:
        print(f"❌ API error: {e}")
        return []


def create_dns_record(domain: str, record_type: str, host: str, value: str, ttl: int = 3600):
    """Create a DNS record"""
    url = f"{SPACESHIP['api_url']}/dns/{domain}/records"

    data = {
        'type': record_type,
        'host': host,
        'value': value,
        'ttl': ttl
    }

    try:
        response = requests.post(url, headers=get_auth_headers(), json=data)
        result = response.json()

        if response.status_code in [200, 201]:
            print(f"✅ Created {record_type} record: {host} → {value}")
            return True
        else:
            print(f"❌ Error: {result}")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False


def delete_dns_record(domain: str, record_id: str):
    """Delete a DNS record"""
    url = f"{SPACESHIP['api_url']}/dns/{domain}/records/{record_id}"

    try:
        response = requests.delete(url, headers=get_auth_headers())

        if response.status_code in [200, 204]:
            print(f"✅ Deleted record: {record_id}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False


def update_nameservers(domain: str, nameservers: list):
    """Update nameservers for a domain"""
    url = f"{SPACESHIP['api_url']}/domains/{domain}/host-records/nameservers"

    data = {'nameservers': nameservers}

    try:
        response = requests.put(url, headers=get_auth_headers(), json=data)
        result = response.json()

        if response.status_code == 200:
            print(f"✅ Updated nameservers for {domain}")
            return True
        else:
            print(f"❌ Error: {result}")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False


def get_nameservers(domain: str):
    """Get current nameservers for a domain"""
    url = f"{SPACESHIP['api_url']}/domains/{domain}/host-records/nameservers"

    try:
        response = requests.get(url, headers=get_auth_headers())
        result = response.json()

        if response.status_code == 200:
            ns = result.get('nameservers', [])
            print(f"\n🔗 Nameservers for {domain}:")
            for n in ns:
                print(f"   {n}")
            return ns
        else:
            print(f"❌ Error: {result}")
            return []
    except Exception as e:
        print(f"❌ API error: {e}")
        return []


def setup_cloudflare_nameservers(domain: str = None):
    """Set Cloudflare nameservers for a domain"""
    if domain is None:
        domain = DOMAIN

    cloudflare_ns = [
        'howard.ns.cloudflare.com',
        'sierra.ns.cloudflare.com'
    ]

    print(f"\n🔧 Setting Cloudflare nameservers for {domain}")
    print(f"   NS1: {cloudflare_ns[0]}")
    print(f"   NS2: {cloudflare_ns[1]}")

    return update_nameservers(domain, cloudflare_ns)


def verify_nameservers(domain: str = None):
    """Verify nameservers are pointing to Cloudflare"""
    if domain is None:
        domain = DOMAIN

    expected_ns = {'howard.ns.cloudflare.com', 'sierra.ns.cloudflare.com'}
    current_ns = set(get_nameservers(domain))

    if expected_ns == current_ns:
        print(f"\n✅ Nameservers correctly point to Cloudflare")
        return True
    else:
        print(f"\n⚠️ Nameservers mismatch!")
        print(f"   Expected: {expected_ns}")
        print(f"   Current:  {current_ns}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("🌐 Spaceship DNS Management — Oriz")
    print("=" * 50)

    if not SPACESHIP['api_key'] or not SPACESHIP['api_secret']:
        print("❌ Missing Spaceship API credentials")
        sys.exit(1)

    args = sys.argv[1:]

    if '--domains' in args:
        list_domains()
    elif '--records' in args:
        get_dns_records(DOMAIN)
    elif '--ns' in args:
        get_nameservers(DOMAIN)
    elif '--setup-cf-ns' in args:
        setup_cloudflare_nameservers()
    elif '--verify-ns' in args:
        verify_nameservers()
    else:
        print("\nUsage:")
        print("  python dns_spaceship.py --domains      List all domains")
        print(f"  python dns_spaceship.py --records      List DNS records for {DOMAIN}")
        print(f"  python dns_spaceship.py --ns           Get nameservers for {DOMAIN}")
        print(f"  python dns_spaceship.py --setup-cf-ns  Set Cloudflare nameservers")
        print(f"  python dns_spaceship.py --verify-ns    Verify Cloudflare NS setup")
