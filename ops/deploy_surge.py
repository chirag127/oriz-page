"""
Deploy Oriz to Surge.sh
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import SURGE, PROJECT_ROOT, DIST_DIR
from build import build_project, ensure_dist_exists


def deploy_to_surge():
    """Deploy to Surge.sh"""
    print("\n🚀 Deploying to Surge.sh...")

    if not SURGE['enabled']:
        print("⚠️ Surge deployment is disabled")
        return False

    if not SURGE['token'] or not SURGE['domain']:
        print("❌ Missing Surge token or domain")
        return False

    # Ensure dist exists
    if not ensure_dist_exists(DIST_DIR):
        print("📦 Building project first...")
        if not build_project(PROJECT_ROOT):
            return False

    # Copy index.html to 200.html for SPA routing
    index_html = DIST_DIR / 'index.html'
    spa_html = DIST_DIR / '200.html'
    if index_html.exists() and not spa_html.exists():
        spa_html.write_text(index_html.read_text(encoding='utf-8'), encoding='utf-8')

    try:
        result = subprocess.run(
            ['npx', 'surge', str(DIST_DIR), SURGE['domain']],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace',
            env={
                **dict(__import__('os').environ),
                'SURGE_TOKEN': SURGE['token'],
            }
        )

        if result.returncode != 0:
            print(f"❌ Deployment failed:\n{result.stderr}")
            return False

        print(f"✅ Deployed to Surge!")
        print(f"   🌐 https://{SURGE['domain']}")
        return True

    except FileNotFoundError:
        print("❌ Surge CLI not found. Install with: npm i -g surge")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("📦 Oriz → Surge.sh Deployment")
    print("=" * 50)

    success = deploy_to_surge()
    sys.exit(0 if success else 1)
