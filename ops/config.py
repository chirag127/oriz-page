"""
Oriz Deployment Configuration
Centralized configuration for all deployment platforms
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Build configuration
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / 'dist'
BUILD_COMMAND = 'npm run build'
DOMAIN = 'oriz.in'

# Cloudflare Configuration
CLOUDFLARE = {
    'enabled': os.getenv('ENABLE_CLOUDFLARE', 'False').lower() == 'true',
    'account_id': os.getenv('CLOUDFLARE_ACCOUNT_ID'),
    'api_key': os.getenv('CLOUDFLARE_GLOBAL_API_KEY'),
    'email': os.getenv('CLOUDFLARE_EMAIL'),
    'project_name': os.getenv('CLOUDFLARE_PROJECT_NAME', 'oriz'),
    'zone_id': os.getenv('CLOUDFLARE_ZONE_ID'),
}

# Netlify Configuration
NETLIFY = {
    'enabled': os.getenv('ENABLE_NETLIFY', 'False').lower() == 'true',
    'auth_token': os.getenv('NETLIFY_AUTH_TOKEN'),
    'site_id': os.getenv('NETLIFY_SITE_ID'),
}

# Vercel Configuration
VERCEL = {
    'enabled': os.getenv('ENABLE_VERCEL', 'False').lower() == 'true',
    'token': os.getenv('VERCEL_TOKEN'),
    'org_id': os.getenv('VERCEL_ORG_ID'),
    'project_id': os.getenv('VERCEL_PROJECT_ID'),
}

# Surge Configuration
SURGE = {
    'enabled': os.getenv('ENABLE_SURGE', 'False').lower() == 'true',
    'token': os.getenv('SURGE_TOKEN'),
    'domain': os.getenv('SURGE_DOMAIN', 'oriz.surge.sh'),
}

# Neocities Configuration
NEOCITIES = {
    'enabled': os.getenv('ENABLE_NEOCITIES', 'False').lower() == 'true',
    'api_key': os.getenv('NEOCITIES_API_KEY'),
    'sitename': os.getenv('NEOCITIES_SITENAME'),
}

# Spaceship DNS Configuration
SPACESHIP = {
    'api_key': os.getenv('SPACESHIP_API_KEY'),
    'api_secret': os.getenv('SPACESHIP_API_SECRET'),
    'api_url': os.getenv('SPACESHIP_API_URL', 'https://spaceship.dev/api/v1'),
}

# GitHub Configuration
GITHUB = {
    'username': os.getenv('GH_USERNAME'),
    'token': os.getenv('GH_TOKEN'),
}

# Email Configuration
EMAIL = {
    'contact_email': os.getenv('SITE_CONTACT_EMAIL', 'hello@oriz.in'),
    'notification_email': 'chiragsinghal127@gmail.com',
    'owner_name': os.getenv('SITE_OWNER_NAME', 'Chirag Singhal'),
}


def get_enabled_platforms():
    """Return list of enabled deployment platforms"""
    platforms = []
    if CLOUDFLARE['enabled']:
        platforms.append('cloudflare')
    if NETLIFY['enabled']:
        platforms.append('netlify')
    if VERCEL['enabled']:
        platforms.append('vercel')
    if SURGE['enabled']:
        platforms.append('surge')
    if NEOCITIES['enabled']:
        platforms.append('neocities')
    return platforms


def validate_config(platform: str) -> bool:
    """Validate that required config exists for a platform"""
    configs = {
        'cloudflare': ['account_id', 'api_key', 'email'],
        'netlify': ['auth_token', 'site_id'],
        'vercel': ['token'],
        'surge': ['token', 'domain'],
        'neocities': ['api_key', 'sitename'],
    }

    platform_config = globals().get(platform.upper(), {})
    required = configs.get(platform, [])

    for key in required:
        if not platform_config.get(key):
            print(f"❌ Missing {platform.upper()}_{key.upper()}")
            return False
    return True
