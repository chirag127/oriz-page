"""
Cloudflare DNS Management for Oriz
"""

import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import CLOUDFLARE, DOMAIN


def get_headers() -> dict:
    """Get Cloudflare API headers"""
    return {
        'X-Auth-Email': CLOUDFLARE['email'],
        'X-Auth-Key': CLOUDFLARE['api_key'],
        'Content-Type': 'application/json'
    }


def get_zone_id(domain: str) -> str | None:
    """Get Cloudflare zone ID for a domain"""
    url = f"https://api.cloudflare.com/client/v4/zones?name={domain}"

    try:
        response = requests.get(url, headers=get_headers())
        result = response.json()

        if result.get('success') and result.get('result'):
            return result['result'][0]['id']
        return None
    except Exception as e:
        print(f"❌ Error getting zone: {e}")
        return None


def list_dns_records(zone_id: str):
    """List all DNS records for a zone"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    try:
        response = requests.get(url, headers=get_headers())
        result = response.json()

        if result.get('success'):
            records = result['result']
            print(f"\n📋 DNS Records ({len(records)} total):")
            for record in records:
                proxied = "🟠" if record.get('proxied') else "⚪"
                print(f"   {proxied} {record['type']:6} {record['name']:40} → {record['content'][:50]}")
            return records
        return []
    except Exception as e:
        print(f"❌ Error listing records: {e}")
        return []


def create_dns_record(zone_id: str, record_type: str, name: str, content: str, proxied: bool = True, ttl: int = 1):
    """Create a DNS record"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    data = {
        'type': record_type,
        'name': name,
        'content': content,
        'proxied': proxied,
        'ttl': ttl  # 1 = Auto
    }

    try:
        response = requests.post(url, headers=get_headers(), json=data)
        result = response.json()

        if result.get('success'):
            print(f"✅ Created {record_type}: {name} → {content}")
            return True
        else:
            errors = result.get('errors', [])
            if any('already exists' in str(e) for e in errors):
                print(f"ℹ️ Record already exists: {name}")
                return True
            print(f"❌ Failed: {errors}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def delete_dns_record(zone_id: str, record_id: str):
    """Delete a DNS record"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

    try:
        response = requests.delete(url, headers=get_headers())
        result = response.json()

        if result.get('success'):
            print(f"✅ Deleted record: {record_id}")
            return True
        else:
            print(f"❌ Failed to delete: {result.get('errors', [])}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def update_dns_record(zone_id: str, record_id: str, record_type: str, name: str, content: str, proxied: bool = True):
    """Update an existing DNS record"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

    data = {
        'type': record_type,
        'name': name,
        'content': content,
        'proxied': proxied,
        'ttl': 1
    }

    try:
        response = requests.put(url, headers=get_headers(), json=data)
        result = response.json()

        if result.get('success'):
            print(f"✅ Updated {record_type}: {name} → {content}")
            return True
        else:
            print(f"❌ Failed: {result.get('errors', [])}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def add_pages_custom_domain(project_name: str, domain: str):
    """Add custom domain to Cloudflare Pages project"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE['account_id']}/pages/projects/{project_name}/domains"

    data = {'name': domain}

    try:
        response = requests.post(url, headers=get_headers(), json=data)
        result = response.json()

        if result.get('success'):
            print(f"✅ Added custom domain: {domain}")
            return True
        else:
            errors = result.get('errors', [])
            if any('already exists' in str(e) for e in errors):
                print(f"ℹ️ Domain already linked: {domain}")
                return True
            print(f"⚠️ {errors}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def setup_email_records(zone_id: str, domain: str):
    """Set up MX and email-related DNS records"""
    print(f"\n📧 Setting up email DNS records for {domain}...")

    # Email forwarding MX records (Cloudflare Email Routing)
    email_records = [
        {'type': 'MX', 'name': domain, 'content': 'route1.mx.cloudflare.net', 'priority': 69},
        {'type': 'MX', 'name': domain, 'content': 'route2.mx.cloudflare.net', 'priority': 27},
        {'type': 'MX', 'name': domain, 'content': 'route3.mx.cloudflare.net', 'priority': 3},
        {'type': 'TXT', 'name': domain, 'content': 'v=spf1 include:_spf.mx.cloudflare.net ~all'},
    ]

    for record in email_records:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        data = {
            'type': record['type'],
            'name': record['name'],
            'content': record['content'],
            'proxied': False,
            'ttl': 1,
        }
        if 'priority' in record:
            data['priority'] = record['priority']

        try:
            response = requests.post(url, headers=get_headers(), json=data)
            result = response.json()
            if result.get('success'):
                print(f"   ✅ {record['type']}: {record['content']}")
            else:
                errors = result.get('errors', [])
                if any('already exists' in str(e) for e in errors):
                    print(f"   ℹ️ Already exists: {record['type']} {record['content']}")
                else:
                    print(f"   ❌ {errors}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def setup_oriz_dns(pages_url: str = None):
    """Set up full DNS for oriz.in with concurrent record processing"""
    if pages_url is None:
        project_name = CLOUDFLARE.get('project_name', 'oriz')
        pages_url = f"{project_name}.pages.dev"

    print(f"\n🔧 Setting up DNS for {DOMAIN}")
    print(f"   Pages URL: {pages_url}")

    zone_id = get_zone_id(DOMAIN)
    if not zone_id:
        print(f"❌ Could not find zone for {DOMAIN}")
        return False

    print(f"   Zone ID: {zone_id}")

    # CNAME records to create
    cname_targets = [
        (DOMAIN, pages_url),           # Root domain
        (f'www.{DOMAIN}', pages_url),   # www subdomain
    ]

    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        for name, target in cname_targets:
            future = executor.submit(create_dns_record, zone_id, 'CNAME', name, target)
            futures[future] = name

        for future in as_completed(futures):
            name = futures[future]
            try:
                success = future.result()
                results.append((name, success))
            except Exception as e:
                print(f"❌ {name}: {e}")
                results.append((name, False))

    # Set up email
    setup_email_records(zone_id, DOMAIN)

    # Add custom domains to Pages project
    project_name = CLOUDFLARE.get('project_name', 'oriz')
    add_pages_custom_domain(project_name, DOMAIN)
    add_pages_custom_domain(project_name, f'www.{DOMAIN}')

    success_count = sum(1 for _, s in results if s)
    print(f"\n📊 DNS Setup: {success_count}/{len(results)} records created")
    return success_count == len(results)


if __name__ == '__main__':
    print("=" * 50)
    print("🌐 Cloudflare DNS Management — Oriz")
    print("=" * 50)

    if not CLOUDFLARE['api_key'] or not CLOUDFLARE['email']:
        print("❌ Missing Cloudflare credentials")
        sys.exit(1)

    import sys as _sys
    args = _sys.argv[1:]

    if '--list' in args:
        zone_id = get_zone_id(DOMAIN)
        if zone_id:
            list_dns_records(zone_id)
    elif '--setup' in args:
        setup_oriz_dns()
    elif '--email' in args:
        zone_id = get_zone_id(DOMAIN)
        if zone_id:
            setup_email_records(zone_id, DOMAIN)
    else:
        print("\nUsage:")
        print("  python dns_cloudflare.py --list    List all DNS records")
        print("  python dns_cloudflare.py --setup   Set up DNS for oriz.in")
        print("  python dns_cloudflare.py --email   Set up email DNS records")
