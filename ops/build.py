"""
Build utilities for Oriz deployment
"""

import subprocess
import sys
from pathlib import Path


def build_project(project_root: Path) -> bool:
    """Build the project using npm"""
    print("🔨 Building project...")

    try:
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=project_root,
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            print(f"❌ Build failed:\n{result.stderr}")
            return False

        print("✅ Build completed successfully")
        return True

    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def ensure_dist_exists(dist_dir: Path) -> bool:
    """Ensure the dist directory exists and contains index.html"""
    if not dist_dir.exists():
        print(f"❌ Dist directory not found: {dist_dir}")
        print("   Run 'npm run build' first")
        return False

    # Check for index.html
    if not (dist_dir / 'index.html').exists():
        print("❌ index.html not found in dist")
        return False

    print(f"✅ Dist directory ready: {dist_dir}")
    return True


def clean_dist(dist_dir: Path) -> bool:
    """Remove the dist directory for a clean build"""
    import shutil

    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
            print("🧹 Cleaned dist directory")
            return True
        except Exception as e:
            print(f"❌ Failed to clean dist: {e}")
            return False
    return True


if __name__ == '__main__':
    from config import PROJECT_ROOT, DIST_DIR

    print("=" * 50)
    print("🔨 Oriz Build")
    print("=" * 50)

    clean_dist(DIST_DIR)
    success = build_project(PROJECT_ROOT)
    sys.exit(0 if success else 1)
