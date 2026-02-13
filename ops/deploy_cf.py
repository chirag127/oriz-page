"""
Deploy Oriz to Cloudflare Pages
"""

import requests
import subprocess
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import CLOUDFLARE, PROJECT_ROOT, DIST_DIR
from build import build_project, ensure_dist_exists


def deploy_to_cloudflare():
    """Deploy to Cloudflare Pages using Wrangler CLI"""
    print("\n🚀 Deploying to Cloudflare Pages...")

    if not CLOUDFLARE['enabled']:
        print("⚠️ Cloudflare deployment is disabled")
        return False

    if not CLOUDFLARE['account_id'] or not CLOUDFLARE['api_key']:
        print("❌ Missing Cloudflare credentials")
        return False

    # Ensure dist exists
    if not ensure_dist_exists(DIST_DIR):
        print("📦 Building project first...")
        if not build_project(PROJECT_ROOT):
            return False

    project_name = CLOUDFLARE.get('project_name', 'oriz')

    # Ensure project exists
    create_cloudflare_project()

    try:
        # Use wrangler pages deploy
        result = subprocess.run(
            [
                'npx', 'wrangler', 'pages', 'deploy', 'dist',
                '--project-name', project_name,
                '--commit-dirty=true'
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace',
            env={
                **dict(__import__('os').environ),
                'CLOUDFLARE_ACCOUNT_ID': CLOUDFLARE['account_id'],
                # Global API Key auth requires both API_KEY and EMAIL
                'CLOUDFLARE_API_KEY': CLOUDFLARE['api_key'],
                'CLOUDFLARE_EMAIL': CLOUDFLARE['email'],
            }
        )

        if result.returncode != 0:
            print(f"❌ Deployment failed:\n{result.stderr}")
            return False

        print(f"✅ Deployed to Cloudflare Pages!")
        print(f"   🌐 https://{project_name}.pages.dev")

        # Extract deployment URL from output
        for line in result.stdout.split('\n'):
            if 'https://' in line and '.pages.dev' in line:
                print(f"   📍 {line.strip()}")

        return True

    except FileNotFoundError:
        print("❌ Wrangler CLI not found. Install with: npm install -g wrangler")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


def create_cloudflare_project():
    """Create a new Cloudflare Pages project via API"""
    print("📁 Creating Cloudflare Pages project...")

    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE['account_id']}/pages/projects"

    headers = {
        'X-Auth-Email': CLOUDFLARE['email'],
        'X-Auth-Key': CLOUDFLARE['api_key'],
        'Content-Type': 'application/json'
    }

    data = {
        'name': CLOUDFLARE.get('project_name', 'oriz'),
        'production_branch': 'main',
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get('success'):
            print(f"✅ Project created: {result['result']['name']}")
            return True
        else:
            errors = result.get('errors', [])
            if any('already exists' in str(e) for e in errors):
                print("ℹ️ Project already exists")
                return True
            print(f"❌ Failed to create project: {errors}")
            return False

    except Exception as e:
        print(f"❌ API error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("📦 Oriz → Cloudflare Pages Deployment")
    print("=" * 50)

    success = deploy_to_cloudflare()
    sys.exit(0 if success else 1)
