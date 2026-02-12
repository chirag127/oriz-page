"""
Oriz Master Automation Script
Manages everything: build, deploy, DNS, email routing
Run with: python ops/run_all.py
"""

import sys
import os
import io
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    CLOUDFLARE, NETLIFY, VERCEL, SURGE, NEOCITIES,
    SPACESHIP, EMAIL, DOMAIN,
    PROJECT_ROOT, DIST_DIR, get_enabled_platforms
)
from build import build_project, ensure_dist_exists, clean_dist


def section(title: str):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def step(msg: str):
    """Print a step message"""
    print(f"  >> {msg}")


def run_all():
    """Master automation: build, deploy, DNS, email — everything."""
    section("ORIZ MASTER AUTOMATION")
    print(f"  Domain:  {DOMAIN}")
    print(f"  Project: {PROJECT_ROOT}")
    print(f"  Email:   {EMAIL['notification_email']}")

    results = {
        'build': False,
        'deploy': {},
        'dns_cloudflare': False,
        'dns_spaceship': False,
        'email_routing': False,
    }

    # ─── PHASE 1: BUILD ───────────────────────────────────────
    section("PHASE 1: BUILD")

    if ensure_dist_exists(DIST_DIR):
        step("Dist already exists, skipping build")
        results['build'] = True
    else:
        step("Building project...")
        clean_dist(DIST_DIR)
        results['build'] = build_project(PROJECT_ROOT)

    if not results['build']:
        print("\n  [FATAL] Build failed. Cannot proceed.")
        return results

    # ─── PHASE 2: DEPLOY TO ALL PLATFORMS ─────────────────────
    section("PHASE 2: MULTI-PLATFORM DEPLOYMENT")

    platforms = get_enabled_platforms()
    step(f"Enabled platforms: {', '.join(platforms) if platforms else 'NONE'}")

    if not platforms:
        step("No platforms enabled. Set ENABLE_<PLATFORM>=True in .env")
    else:
        if 'cloudflare' in platforms:
            try:
                from deploy_cf import deploy_to_cloudflare
                results['deploy']['Cloudflare'] = deploy_to_cloudflare()
            except Exception as e:
                print(f"  [ERROR] Cloudflare: {e}")
                results['deploy']['Cloudflare'] = False

        if 'netlify' in platforms:
            try:
                from deploy_netlify import deploy_to_netlify
                results['deploy']['Netlify'] = deploy_to_netlify()
            except Exception as e:
                print(f"  [ERROR] Netlify: {e}")
                results['deploy']['Netlify'] = False

        if 'vercel' in platforms:
            try:
                from deploy_vercel import deploy_to_vercel
                results['deploy']['Vercel'] = deploy_to_vercel()
            except Exception as e:
                print(f"  [ERROR] Vercel: {e}")
                results['deploy']['Vercel'] = False

        if 'surge' in platforms:
            try:
                from deploy_surge import deploy_to_surge
                results['deploy']['Surge'] = deploy_to_surge()
            except Exception as e:
                print(f"  [ERROR] Surge: {e}")
                results['deploy']['Surge'] = False

        if 'neocities' in platforms:
            try:
                from deploy_neocities import deploy_to_neocities
                results['deploy']['Neocities'] = deploy_to_neocities()
            except Exception as e:
                print(f"  [ERROR] Neocities: {e}")
                results['deploy']['Neocities'] = False

    # ─── PHASE 3: CLOUDFLARE DNS ──────────────────────────────
    section("PHASE 3: CLOUDFLARE DNS MANAGEMENT")

    if CLOUDFLARE.get('api_key') and CLOUDFLARE.get('email'):
        try:
            from dns_cloudflare import setup_oriz_dns, get_zone_id, list_dns_records
            step("Setting up DNS records for oriz.in...")
            results['dns_cloudflare'] = setup_oriz_dns()

            # List current records
            step("Listing current DNS records...")
            zone_id = get_zone_id(DOMAIN)
            if zone_id:
                list_dns_records(zone_id)
        except Exception as e:
            print(f"  [ERROR] Cloudflare DNS: {e}")
    else:
        step("Skipped — missing Cloudflare credentials")

    # ─── PHASE 4: SPACESHIP DNS ───────────────────────────────
    section("PHASE 4: SPACESHIP DNS / NAMESERVERS")

    if SPACESHIP.get('api_key') and SPACESHIP.get('api_secret'):
        try:
            from dns_spaceship import verify_nameservers, get_dns_records
            step("Verifying Cloudflare nameservers...")
            results['dns_spaceship'] = verify_nameservers(DOMAIN)

            step("Listing Spaceship DNS records...")
            get_dns_records(DOMAIN)
        except Exception as e:
            print(f"  [ERROR] Spaceship DNS: {e}")
    else:
        step("Skipped — missing Spaceship credentials")

    # ─── PHASE 5: EMAIL ROUTING ───────────────────────────────
    section("PHASE 5: EMAIL ROUTING")

    if CLOUDFLARE.get('api_key') and CLOUDFLARE.get('email'):
        try:
            from manage_email import setup_email_routing
            step(f"Setting up email routing: *@{DOMAIN} -> {EMAIL['notification_email']}")
            results['email_routing'] = setup_email_routing()
        except Exception as e:
            print(f"  [ERROR] Email routing: {e}")
    else:
        step("Skipped — missing Cloudflare credentials")

    # ─── PHASE 6: FILE INTEGRITY ──────────────────────────────
    section("PHASE 6: FILE INTEGRITY CHECK")

    try:
        from manage_files import verify_build_integrity, analyze_dist
        verify_build_integrity()
        analyze_dist()
    except Exception as e:
        print(f"  [ERROR] File check: {e}")

    # ─── PHASE 7: SEND EMAIL REPORT ──────────────────────────
    section("PHASE 7: DEPLOYMENT REPORT")

    try:
        from manage_email import send_deployment_report
        send_deployment_report(results['deploy'])
    except Exception as e:
        print(f"  [ERROR] Report: {e}")

    # ─── FINAL SUMMARY ────────────────────────────────────────
    section("FINAL SUMMARY")

    print(f"  Build:          {'OK' if results['build'] else 'FAILED'}")

    if results['deploy']:
        for platform, success in results['deploy'].items():
            status = 'OK' if success else 'FAILED'
            print(f"  Deploy {platform:12s} {status}")
    else:
        print("  Deploy:         No platforms enabled")

    print(f"  CF DNS:         {'OK' if results['dns_cloudflare'] else 'FAILED/SKIPPED'}")
    print(f"  Spaceship NS:   {'OK' if results['dns_spaceship'] else 'FAILED/SKIPPED'}")
    print(f"  Email Routing:  {'OK' if results['email_routing'] else 'FAILED/SKIPPED'}")

    deploy_ok = sum(1 for s in results['deploy'].values() if s)
    deploy_total = len(results['deploy'])
    print(f"\n  Deployments: {deploy_ok}/{deploy_total} succeeded")

    all_ok = (
        results['build']
        and deploy_ok == deploy_total
        and results['dns_cloudflare']
        and results['dns_spaceship']
        and results['email_routing']
    )

    if all_ok:
        print("\n  [ALL SYSTEMS GO] Everything managed successfully!")
    else:
        print("\n  [PARTIAL] Some operations had issues — check above for details")

    # Save summary
    summary_file = PROJECT_ROOT / 'deploy_summary.txt'
    summary_lines = [
        f"Oriz Deployment Summary",
        f"=======================",
        f"Build: {'OK' if results['build'] else 'FAILED'}",
    ]
    for p, s in results['deploy'].items():
        summary_lines.append(f"Deploy {p}: {'OK' if s else 'FAILED'}")
    summary_lines.extend([
        f"CF DNS: {'OK' if results['dns_cloudflare'] else 'FAILED/SKIPPED'}",
        f"Spaceship NS: {'OK' if results['dns_spaceship'] else 'FAILED/SKIPPED'}",
        f"Email: {'OK' if results['email_routing'] else 'FAILED/SKIPPED'}",
        f"Result: {deploy_ok}/{deploy_total} deployments OK",
    ])
    summary_file.write_text('\n'.join(summary_lines), encoding='utf-8')

    return results


if __name__ == '__main__':
    results = run_all()

    # Exit with appropriate code
    deploy_ok = sum(1 for s in results.get('deploy', {}).values() if s)
    deploy_total = len(results.get('deploy', {}))
    sys.exit(0 if results['build'] and deploy_ok > 0 else 1)
