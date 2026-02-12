"""
Deploy Oriz to Neocities
"""

import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import NEOCITIES, PROJECT_ROOT, DIST_DIR
from build import build_project, ensure_dist_exists


def deploy_to_neocities():
    """Deploy to Neocities via API"""
    print("\n🚀 Deploying to Neocities...")

    if not NEOCITIES['enabled']:
        print("⚠️ Neocities deployment is disabled")
        return False

    if not NEOCITIES['api_key']:
        print("❌ Missing Neocities API key")
        return False

    # Ensure dist exists
    if not ensure_dist_exists(DIST_DIR):
        print("📦 Building project first...")
        if not build_project(PROJECT_ROOT):
            return False

    # Neocities API endpoint
    url = "https://neocities.org/api/upload"

    headers = {
        'Authorization': f"Bearer {NEOCITIES['api_key']}"
    }

    # Collect all files to upload
    files_to_upload = []
    for file_path in DIST_DIR.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(DIST_DIR)
            files_to_upload.append((str(relative_path), file_path))

    print(f"📤 Uploading {len(files_to_upload)} files...")

    success_count = 0
    error_count = 0

    # Upload in batches (Neocities allows multiple files per request)
    batch_size = 10
    for i in range(0, len(files_to_upload), batch_size):
        batch = files_to_upload[i:i + batch_size]

        files = []
        for name, path in batch:
            try:
                files.append((name, (name, open(path, 'rb'))))
            except Exception as e:
                print(f"   ⚠️ Could not read {name}: {e}")
                error_count += 1

        try:
            response = requests.post(url, headers=headers, files=files)

            # Close file handles
            for _, (_, f) in files:
                f.close()

            if response.status_code == 200:
                result = response.json()
                if result.get('result') == 'success':
                    success_count += len(batch)
                    print(f"   ✓ Uploaded batch {i // batch_size + 1}")
                else:
                    print(f"   ⚠️ Batch warning: {result}")
            else:
                print(f"   ❌ Batch failed: {response.status_code}")
                error_count += len(batch)

        except Exception as e:
            print(f"   ❌ Upload error: {e}")
            error_count += len(batch)

    if error_count == 0:
        print("✅ Deployed to Neocities!")
        print(f"   🌐 https://{NEOCITIES['sitename']}.neocities.org")
        return True
    else:
        print(f"⚠️ Deployed with {error_count} errors")
        return success_count > 0


if __name__ == '__main__':
    print("=" * 50)
    print("📦 Oriz → Neocities Deployment")
    print("=" * 50)

    success = deploy_to_neocities()
    sys.exit(0 if success else 1)
