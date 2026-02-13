import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dns_cloudflare import list_dns_records, get_zone_id
from config import DOMAIN

def audit():
    zone_id = get_zone_id(DOMAIN)
    records = list_dns_records(zone_id)
    print("\n--- SPECIFIC DNS AUDIT ---")
    targets = [f"about.{DOMAIN}", f"www.{DOMAIN}", DOMAIN]
    for r in records:
        name = r.get('name', '')
        if name in targets:
            print(f"{r.get('type'):6} {name:30} -> {r.get('content')}")

if __name__ == "__main__":
    audit()
