import sys
from pathlib import Path

# Force UTF-8
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))
from dns_cloudflare import list_dns_records, get_zone_id
from config import DOMAIN

def verify():
    print(f"\n--- DNS VERIFICATION for {DOMAIN} ---")
    zone_id = get_zone_id(DOMAIN)
    if not zone_id:
        print("Zone not found.")
        return

    records = list_dns_records(zone_id)

    # Check for about, www, and root
    about_found = False
    www_found = False
    root_found = False

    for r in records:
        name = r.get('name', '')
        rtype = r.get('type', '')
        content = r.get('content', '')

        if name == f"about.{DOMAIN}":
            print(f"✅ FOUND: {rtype:6} {name:25} -> {content}")
            about_found = True
        elif name == f"www.{DOMAIN}":
            if rtype == 'CNAME' and 'pages.dev' in content:
                print(f"❌ FORBIDDEN: {rtype:6} {name:25} -> {content} (Should be removed)")
                www_found = True
        elif name == DOMAIN:
            if rtype == 'CNAME' and 'pages.dev' in content:
                print(f"❌ FORBIDDEN: {rtype:6} {name:25} -> {content} (Should be removed)")
                root_found = True

    if not about_found:
        print("❌ MISSING: about.oriz.in")

    if not www_found and not root_found:
        print("✅ CLEAN: root and www records removed (or never existed as CNAMEs pointing to pages)")
    else:
        print("⚠️ ACTION NEEDED: Some forbidden records still exist.")

if __name__ == "__main__":
    verify()
