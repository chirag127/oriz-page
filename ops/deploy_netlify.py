"""
Deploy Oriz to Netlify
"""

import requests
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import NETLIFY, PROJECT_ROOT, DIST_DIR
from build import build_project, ensure_dist_exists


def deploy_to_netlify():
    """Deploy to Netlify using CLI or API"""
    print("\n🚀 Deploying to Netlify...")

    if not NETLIFY['enabled']:
        print("⚠️ Netlify deployment is disabled")
        return False

    if not NETLIFY['auth_token']:
        print("❌ Missing Netlify auth token")
        return False

    # Ensure dist exists
    if not ensure_dist_exists(DIST_DIR):
        print("📦 Building project first...")
        if not build_project(PROJECT_ROOT):
            return False

    try:
        # Use Netlify CLI
        cmd = ['npx', 'netlify', 'deploy', '--prod', '--dir=dist']

        if NETLIFY.get('site_id'):
            cmd.extend(['--site', NETLIFY['site_id']])

        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace',
            env={
                **dict(__import__('os').environ),
                'NETLIFY_AUTH_TOKEN': NETLIFY['auth_token'],
            }
        )

        if result.returncode != 0:
            print(f"❌ Deployment failed:\n{result.stderr}")
            # Try API method as fallback
            return deploy_via_api()

        print("✅ Deployed to Netlify!")

        # Extract URL from output
        for line in result.stdout.split('\n'):
            if 'Website URL' in line or 'https://' in line:
                print(f"   🌐 {line.strip()}")

        return True

    except FileNotFoundError:
        print("⚠️ Netlify CLI not found, using API...")
        return deploy_via_api()
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


def deploy_via_api():
    """Deploy using Netlify API (zip upload)"""
    import zipfile
    import io

    print("📤 Deploying via Netlify API...")

    # Create zip of dist folder
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in DIST_DIR.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(DIST_DIR)
                zip_file.write(file_path, arcname)

    zip_buffer.seek(0)

    # Deploy via API
    url = f"https://api.netlify.com/api/v1/sites/{NETLIFY['site_id']}/deploys"
    headers = {
        'Authorization': f"Bearer {NETLIFY['auth_token']}",
        'Content-Type': 'application/zip',
    }

    try:
        response = requests.post(url, headers=headers, data=zip_buffer.read())

        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Deployed to Netlify!")
            print(f"   🌐 {result.get('ssl_url', result.get('url'))}")
            return True
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ API error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("📦 Oriz → Netlify Deployment")
    print("=" * 50)

    success = deploy_to_netlify()
    sys.exit(0 if success else 1)
