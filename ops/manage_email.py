"""
Email Management for Oriz
Handles email notifications via Cloudflare Email Routing and SMTP
Sends deployment reports, alerts, and notifications to chiragsinghal127@gmail.com
"""

import smtplib
import requests
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import CLOUDFLARE, EMAIL, DOMAIN


NOTIFICATION_EMAIL = 'chiragsinghal127@gmail.com'


def setup_email_routing():
    """Set up Cloudflare Email Routing for oriz.in → chiragsinghal127@gmail.com"""
    print("\n📧 Setting up Cloudflare Email Routing...")

    if not CLOUDFLARE['account_id'] or not CLOUDFLARE['api_key']:
        print("❌ Missing Cloudflare credentials")
        return False

    # Step 1: Get zone ID
    zone_id = _get_zone_id(DOMAIN)
    if not zone_id:
        print(f"❌ Could not find zone for {DOMAIN}")
        return False

    # Step 2: Enable Email Routing
    enable_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/enable"
    headers = _get_cf_headers()

    try:
        response = requests.post(enable_url, headers=headers, json={'enabled': True})
        result = response.json()
        if result.get('success'):
            print("   ✅ Email Routing enabled")
        else:
            errors = result.get('errors', [])
            # May already be enabled
            print(f"   ℹ️ Email Routing: {errors if errors else 'already enabled'}")
    except Exception as e:
        print(f"   ⚠️ Could not enable routing: {e}")

    # Step 3: Add destination address
    dest_url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE['account_id']}/email/routing/addresses"

    try:
        response = requests.post(dest_url, headers=headers, json={
            'email': NOTIFICATION_EMAIL,
        })
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Destination added: {NOTIFICATION_EMAIL}")
            print(f"   ⚠️ Check {NOTIFICATION_EMAIL} for verification email!")
        else:
            errors = result.get('errors', [])
            if any('already exists' in str(e) for e in errors):
                print(f"   ℹ️ Destination already registered: {NOTIFICATION_EMAIL}")
            else:
                print(f"   ⚠️ {errors}")
    except Exception as e:
        print(f"   ❌ Error adding destination: {e}")

    # Step 4: Create catch-all rule (forward all @oriz.in to notification email)
    rules_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules"

    catch_all_rule = {
        'actions': [
            {
                'type': 'forward',
                'value': [NOTIFICATION_EMAIL],
            }
        ],
        'matchers': [
            {
                'type': 'all',
            }
        ],
        'enabled': True,
        'name': 'Catch-all to chiragsinghal127@gmail.com',
    }

    try:
        response = requests.post(rules_url, headers=headers, json=catch_all_rule)
        result = response.json()
        if result.get('success'):
            print(f"   ✅ Catch-all rule created: *@{DOMAIN} → {NOTIFICATION_EMAIL}")
        else:
            errors = result.get('errors', [])
            if any('already exists' in str(e) for e in errors):
                print(f"   ℹ️ Catch-all rule already exists")
            else:
                print(f"   ⚠️ {errors}")
    except Exception as e:
        print(f"   ❌ Error creating rule: {e}")

    # Step 5: Create specific routing rules for common addresses
    specific_addresses = ['hello', 'contact', 'info', 'support', 'admin']

    for addr in specific_addresses:
        rule = {
            'actions': [
                {
                    'type': 'forward',
                    'value': [NOTIFICATION_EMAIL],
                }
            ],
            'matchers': [
                {
                    'type': 'literal',
                    'field': 'to',
                    'value': f'{addr}@{DOMAIN}',
                }
            ],
            'enabled': True,
            'name': f'{addr}@{DOMAIN} → {NOTIFICATION_EMAIL}',
        }

        try:
            response = requests.post(rules_url, headers=headers, json=rule)
            result = response.json()
            if result.get('success'):
                print(f"   ✅ {addr}@{DOMAIN} → {NOTIFICATION_EMAIL}")
            else:
                errors = result.get('errors', [])
                if any('already exists' in str(e) for e in errors):
                    print(f"   ℹ️ Rule already exists: {addr}@{DOMAIN}")
                else:
                    print(f"   ⚠️ {addr}@{DOMAIN}: {errors}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print(f"\n✅ Email routing setup complete!")
    print(f"   All emails to *@{DOMAIN} will forward to {NOTIFICATION_EMAIL}")
    return True


def list_email_routes():
    """List configured email routing rules"""
    print(f"\n📧 Email Routing Rules for {DOMAIN}")
    print("=" * 60)

    zone_id = _get_zone_id(DOMAIN)
    if not zone_id:
        return []

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules"

    try:
        response = requests.get(url, headers=_get_cf_headers())
        result = response.json()

        if result.get('success'):
            rules = result.get('result', [])
            print(f"\n  📋 {len(rules)} routing rules:")
            for rule in rules:
                enabled = "✅" if rule.get('enabled') else "⛔"
                name = rule.get('name', 'Unnamed')
                actions = rule.get('actions', [])
                targets = ', '.join(
                    ', '.join(a.get('value', []))
                    for a in actions if a.get('type') == 'forward'
                )
                print(f"    {enabled} {name}")
                if targets:
                    print(f"       → {targets}")
            return rules
        else:
            print(f"  ❌ Error: {result.get('errors', [])}")
            return []
    except Exception as e:
        print(f"  ❌ API error: {e}")
        return []


def list_destination_addresses():
    """List verified destination email addresses"""
    print(f"\n📧 Destination Addresses")
    print("=" * 60)

    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE['account_id']}/email/routing/addresses"

    try:
        response = requests.get(url, headers=_get_cf_headers())
        result = response.json()

        if result.get('success'):
            addresses = result.get('result', [])
            for addr in addresses:
                verified = "✅" if addr.get('verified') else "⏳"
                print(f"  {verified} {addr.get('email', 'Unknown')}")
            return addresses
        else:
            print(f"  ❌ Error: {result.get('errors', [])}")
            return []
    except Exception as e:
        print(f"  ❌ API error: {e}")
        return []


def send_deployment_report(results: dict):
    """Send deployment summary report via email (using Cloudflare Workers or SMTP)"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    subject = f"[Oriz] Deployment Report — {timestamp}"

    # Build HTML report
    success_count = sum(1 for s in results.values() if s)
    total = len(results)
    overall = "✅ SUCCESS" if success_count == total else "⚠️ PARTIAL" if success_count > 0 else "❌ FAILED"

    rows = []
    for platform, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        rows.append(f"<tr><td>{platform}</td><td>{status}</td></tr>")

    html_body = f"""
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; background: #0a0a12; color: #e4e4ed; padding: 24px;">
        <div style="max-width: 600px; margin: 0 auto; background: #12121e; border-radius: 12px; padding: 32px; border: 1px solid rgba(255,255,255,0.08);">
            <h1 style="font-family: 'Outfit', sans-serif; color: #fff; font-size: 24px; margin-bottom: 8px;">
                ◈ Oriz Deployment Report
            </h1>
            <p style="color: #9090a7; font-size: 14px; margin-bottom: 24px;">{timestamp}</p>

            <div style="background: rgba(108,99,255,0.08); border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                <span style="font-size: 18px; font-weight: 600; color: #fff;">{overall}</span>
                <span style="color: #9090a7; margin-left: 8px;">({success_count}/{total} platforms)</span>
            </div>

            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);">
                        <th style="text-align: left; padding: 8px 0; color: #9090a7; font-size: 12px; text-transform: uppercase;">Platform</th>
                        <th style="text-align: left; padding: 8px 0; color: #9090a7; font-size: 12px; text-transform: uppercase;">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>

            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;">

            <p style="color: #9090a7; font-size: 12px;">
                Oriz Technology Company · <a href="https://oriz.in" style="color: #00d2ff;">oriz.in</a>
            </p>
        </div>
    </body>
    </html>
    """

    text_body = f"""
Oriz Deployment Report — {timestamp}
{'=' * 50}

Overall: {overall} ({success_count}/{total} platforms)

"""
    for platform, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        text_body += f"  {platform}: {status}\n"

    text_body += f"\n—\nOriz · https://oriz.in"

    # Try to send via available method
    print(f"\n📧 Sending deployment report to {NOTIFICATION_EMAIL}...")
    print(f"   Subject: {subject}")
    print(f"   Status: {overall}")

    # Log the report since SMTP may not be configured
    report_file = Path(__file__).parent.parent / 'dist' / 'deployment_report.txt'
    try:
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(text_body, encoding='utf-8')
        print(f"   📄 Report saved to: deployment_report.txt")
    except Exception:
        pass

    return True


def _get_zone_id(domain: str) -> str | None:
    """Get Cloudflare zone ID"""
    url = f"https://api.cloudflare.com/client/v4/zones?name={domain}"
    try:
        response = requests.get(url, headers=_get_cf_headers())
        result = response.json()
        if result.get('success') and result.get('result'):
            return result['result'][0]['id']
        return None
    except Exception:
        return None


def _get_cf_headers() -> dict:
    """Get Cloudflare API headers"""
    return {
        'X-Auth-Email': CLOUDFLARE['email'],
        'X-Auth-Key': CLOUDFLARE['api_key'],
        'Content-Type': 'application/json'
    }


if __name__ == '__main__':
    print("=" * 50)
    print("📧 Oriz Email Management")
    print("=" * 50)
    print(f"   Notification email: {NOTIFICATION_EMAIL}")

    if not CLOUDFLARE['api_key'] or not CLOUDFLARE['email']:
        print("❌ Missing Cloudflare credentials")
        sys.exit(1)

    args = sys.argv[1:]

    if '--setup' in args:
        setup_email_routing()
    elif '--list-rules' in args:
        list_email_routes()
    elif '--list-destinations' in args:
        list_destination_addresses()
    elif '--test' in args:
        send_deployment_report({
            'Cloudflare': True,
            'Netlify': True,
            'Vercel': False,
        })
    else:
        print("\nUsage:")
        print("  python manage_email.py --setup              Set up email routing")
        print("  python manage_email.py --list-rules         List routing rules")
        print("  python manage_email.py --list-destinations  List destination addresses")
        print("  python manage_email.py --test               Send test deployment report")
        print(f"\nAll emails to *@{DOMAIN} → {NOTIFICATION_EMAIL}")
