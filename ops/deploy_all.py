"""
Deploy Oriz to ALL enabled platforms
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import get_enabled_platforms, PROJECT_ROOT, DIST_DIR
from build import build_project, ensure_dist_exists


def deploy_all():
    """Deploy to all enabled platforms"""
    print("=" * 60)
    print("🚀 Oriz Multi-Platform Deployment")
    print("=" * 60)

    # Build once for all platforms
    print("\n📦 Building project...")
    if not ensure_dist_exists(DIST_DIR):
        if not build_project(PROJECT_ROOT):
            print("❌ Build failed. Aborting deployment.")
            return False

    platforms = get_enabled_platforms()

    if not platforms:
        print("⚠️ No deployment platforms enabled!")
        print("   Set ENABLE_<PLATFORM>=True in .env")
        return False

    print(f"\n📋 Enabled platforms: {', '.join(platforms)}")

    results = {}

    # Deploy to each platform
    if 'cloudflare' in platforms:
        from deploy_cf import deploy_to_cloudflare
        results['Cloudflare'] = deploy_to_cloudflare()

    if 'netlify' in platforms:
        from deploy_netlify import deploy_to_netlify
        results['Netlify'] = deploy_to_netlify()

    if 'vercel' in platforms:
        from deploy_vercel import deploy_to_vercel
        results['Vercel'] = deploy_to_vercel()

    if 'surge' in platforms:
        from deploy_surge import deploy_to_surge
        results['Surge'] = deploy_to_surge()

    if 'neocities' in platforms:
        from deploy_neocities import deploy_to_neocities
        results['Neocities'] = deploy_to_neocities()

    # Send email notification with results
    try:
        from manage_email import send_deployment_report
        send_deployment_report(results)
    except Exception as e:
        print(f"⚠️ Email notification skipped: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 Deployment Summary")
    print("=" * 60)

    for platform, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"   {platform}: {status}")

    success_count = sum(1 for s in results.values() if s)
    total = len(results)

    print(f"\n   Total: {success_count}/{total} platforms succeeded")

    return success_count == total


if __name__ == '__main__':
    success = deploy_all()
    sys.exit(0 if success else 1)
