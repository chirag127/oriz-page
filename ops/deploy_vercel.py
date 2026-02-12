"""
Deploy Oriz to Vercel
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import VERCEL, PROJECT_ROOT, DIST_DIR
from build import build_project, ensure_dist_exists


def deploy_to_vercel():
    """Deploy to Vercel using CLI"""
    print("\n🚀 Deploying to Vercel...")

    if not VERCEL['enabled']:
        print("⚠️ Vercel deployment is disabled")
        return False

    if not VERCEL['token']:
        print("❌ Missing Vercel token")
        return False

    # Ensure dist exists
    if not ensure_dist_exists(DIST_DIR):
        print("📦 Building project first...")
        if not build_project(PROJECT_ROOT):
            return False

    try:
        # Create vercel.json for static deployment
        vercel_config = PROJECT_ROOT / 'vercel.json'
        if not vercel_config.exists():
            vercel_config.write_text('{"outputDirectory": "dist"}')

        # Deploy using Vercel CLI
        result = subprocess.run(
            [
                'npx', 'vercel', 'deploy', '--prod',
                '--yes', '--token', VERCEL['token']
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            print(f"❌ Deployment failed:\n{result.stderr}")
            return False

        print("✅ Deployed to Vercel!")

        # Extract URL from output
        for line in result.stdout.split('\n'):
            if 'https://' in line and 'vercel' in line:
                print(f"   🌐 {line.strip()}")

        return True

    except FileNotFoundError:
        print("❌ Vercel CLI not found. Install with: npm i -g vercel")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("📦 Oriz → Vercel Deployment")
    print("=" * 50)

    success = deploy_to_vercel()
    sys.exit(0 if success else 1)
