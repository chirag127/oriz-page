import sys
import requests
from pathlib import Path

# Force UTF-8 output
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))
from dns_cloudflare import list_dns_records, get_zone_id
from config import DOMAIN

def final_check():
    print(f"--- FINAL HEALTH CHECK FOR {DOMAIN} ---")

    # 1. DNS Check
    zone_id = get_zone_id(DOMAIN)
    records = list_dns_records(zone_id)

    print("\n[DNS RECORDS]")
    targets = [f"about.{DOMAIN}", f"www.{DOMAIN}", DOMAIN]
    for r in records:
        name = r.get('name', '')
        if name in targets:
            print(f"{r.get('type'):6} {name:30} -> {r.get('content')}")

    # 2. HTTP Check
    urls = {
        "Main Site (Cloudflare)": f"https://about.{DOMAIN}",
        "Netlify": "https://chirag127.netlify.app",
        "Vercel": "https://chirag127-6r7f25peu-whyiswhengmailcoms-projects.vercel.app",
        "Surge": "https://chirag127.surge.sh",
        "Neocities": "https://chirag127.neocities.org"
    }

    print("\n[HTTP REACHABILITY]")
    for label, url in urls.items():
        try:
            resp = requests.get(url, timeout=10)
            print(f"{label:22}: {resp.status_code} {resp.reason} ({url})")
        except Exception as e:
            print(f"{label:22}: FAILED - {e}")

if __name__ == "__main__":
    final_check()
