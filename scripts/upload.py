#!/usr/bin/env python3
"""
Universal upload script for mem_shards
Handles absolute/relative paths, uploads images, and creates mem_shards from markdown


Usage:
  upload.py file.md                    # Uses local (default)
  MEMSHARD_ENV=local upload.py file.md # Explicit local
  MEMSHARD_ENV=stage upload.py file.md # Uses stage
  MEMSHARD_ENV=prod upload.py file.md  # Uses production

Or use the shell wrapper:
  ./upload file.md                     # Uses local
  ./upload local file.md               # Explicit local
  ./upload stage file.md               # Uses stage
  ./upload prod file.md                # Uses production
"""

import os
import sys
import json
import re
import requests
from pathlib import Path
from typing import Optional, List, Tuple
import shutil

# Load configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / 'config.json'

if not CONFIG_FILE.exists():
    print(f"Error: config.json not found at {CONFIG_FILE}")
    sys.exit(1)

with open(CONFIG_FILE) as f:
    config = json.load(f)

# Environment detection
MEMSHARD_ENV = os.environ.get('MEMSHARD_ENV', 'local').lower()

# Build environment configurations from config.json
ENV_CONFIG = {}
for env_key, env_data in config['environments'].items():
    ENV_CONFIG[env_key] = {
        'url': env_data['url'],
        'token_file': Path.home() / f'.memshard_token_{env_key}',
        'name': env_data['name']
    }

# Validate environment
if MEMSHARD_ENV not in ENV_CONFIG:
    print(f"Error: Invalid environment '{MEMSHARD_ENV}'. Must be: {', '.join(ENV_CONFIG.keys())}")
    sys.exit(1)

# Configuration
API_BASE_URL = ENV_CONFIG[MEMSHARD_ENV]['url']
TOKEN_FILE = ENV_CONFIG[MEMSHARD_ENV]['token_file']
ENV_NAME = ENV_CONFIG[MEMSHARD_ENV]['name']

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(color: str, message: str):
    """Print colored message"""
    print(f"{color}{message}{Colors.NC}")

def get_token() -> Optional[str]:
    """Get authentication token from file or request new one"""
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text().strip()
        if token:
            print_color(Colors.GREEN, f"✓ Using cached token for {ENV_NAME} environment")
            return token
    
    print_color(Colors.YELLOW, f"No token found for {ENV_NAME} environment. Please authenticate.")
    username = input("Username: ")
    password = input("Password: ")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/token/",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        token = response.json()['token']
        
        # Save token
        TOKEN_FILE.write_text(token)
        TOKEN_FILE.chmod(0o600)
        
        print_color(Colors.GREEN, f"✓ Token saved to {TOKEN_FILE}")
        return token
    except requests.exceptions.RequestException as e:
        print_color(Colors.RED, f"✗ Authentication failed: {e}")
        return None

def upload_image(file_path: Path, alt_text: str, token: str) -> Optional[dict]:
    """Upload an image file to the server"""
    print_color(Colors.BLUE, f"  → Uploading image: {file_path.name}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'image': (file_path.name, f, 'image/jpeg')}
            data = {'alt_text': alt_text}
            headers = {'Authorization': f'Token {token}'}
            
            response = requests.post(
                f"{API_BASE_URL}/api/images/",
                files=files,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            print_color(Colors.GREEN, f"  ✓ Uploaded: {result['url']}")
            return result
    except Exception as e:
        print_color(Colors.RED, f"  ✗ Failed to upload {file_path.name}: {e}")
        return None

def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """Parse frontmatter from markdown content"""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    frontmatter_text, markdown_content = match.groups()
    
    # Parse frontmatter
    metadata = {}
    for line in frontmatter_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    return metadata, markdown_content.strip()

def rebuild_markdown_with_frontmatter(metadata: dict, content: str) -> str:
    """Rebuild markdown file with updated frontmatter"""
    frontmatter_lines = ['---']
    for key, value in metadata.items():
        frontmatter_lines.append(f'{key}: {value}')
    frontmatter_lines.append('---')
    frontmatter_lines.append('')
    frontmatter_lines.append(content)
    
    return '\n'.join(frontmatter_lines)

def find_local_images(md_content: str, md_file_path: Path) -> List[Tuple[str, Path]]:
    """
    Find all local image references in markdown content
    Returns list of (markdown_path, absolute_file_path) tuples
    """
    # Regex to find markdown images: ![alt](path)
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, md_content)
    
    local_images = []
    for alt_text, img_path in matches:
        # Skip external URLs
        if img_path.startswith(('http://', 'https://', '//')):
            continue
        
        # Resolve relative paths relative to the markdown file location
        md_dir = md_file_path.parent
        abs_img_path = (md_dir / img_path).resolve()
        
        if abs_img_path.exists():
            local_images.append((img_path, abs_img_path))
            print_color(Colors.BLUE, f"  Found local image: {img_path} → {abs_img_path}")
        else:
            print_color(Colors.YELLOW, f"  Warning: Image not found: {abs_img_path}")
    
    return local_images

def process_markdown_with_images(md_file: Path, token: str) -> Optional[Path]:
    """
    Process markdown file:
    1. Find thumbnail in frontmatter
    2. Find all local images in content
    3. Upload them
    4. Replace local paths with server URLs
    5. Save as .original and create new version
    """
    print_color(Colors.BLUE, f"\n📄 Processing markdown: {md_file}")
    
    # Read original content
    content = md_file.read_text()
    
    # Parse frontmatter
    metadata, markdown_content = parse_frontmatter(content)
    
    # Check for thumbnail in frontmatter
    thumbnail_path = metadata.get('thumbnail', '').strip()
    thumbnail_uploaded = False
    
    if thumbnail_path and not thumbnail_path.startswith('http'):
        # Thumbnail is a local path, need to upload it
        print_color(Colors.BLUE, f"\n📤 Found local thumbnail: {thumbnail_path}")
        
        # Resolve thumbnail path relative to markdown file
        md_dir = md_file.parent
        abs_thumbnail_path = (md_dir / thumbnail_path).resolve()
        
        if abs_thumbnail_path.exists():
            result = upload_image(abs_thumbnail_path, "Thumbnail", token)
            if result:
                metadata['thumbnail'] = result['url']
                thumbnail_uploaded = True
                print_color(Colors.GREEN, f"  ✓ Thumbnail uploaded: {result['url']}")
        else:
            print_color(Colors.YELLOW, f"  Warning: Thumbnail not found: {abs_thumbnail_path}")
            # Remove invalid thumbnail path
            if 'thumbnail' in metadata:
                del metadata['thumbnail']
    
    # Find local images in content
    local_images = find_local_images(markdown_content, md_file)
    
    if not local_images and not thumbnail_uploaded:
        print_color(Colors.YELLOW, "  No local images found, uploading as-is")
        return md_file
    
    print_color(Colors.BLUE, f"\n📤 Uploading {len(local_images)} content images...")
    
    # Upload images and build replacement map
    replacements = {}
    for original_path, abs_path in local_images:
        # Use filename as alt text if not in markdown
        alt_text = abs_path.stem
        result = upload_image(abs_path, alt_text, token)
        
        if result:
            replacements[original_path] = result['url']
    
    # Create backup
    backup_file = md_file.with_suffix(md_file.suffix + '.original')
    if not backup_file.exists():
        shutil.copy2(md_file, backup_file)
        print_color(Colors.GREEN, f"\n✓ Original saved: {backup_file}")
    
    # Replace paths in content
    new_content = markdown_content
    for old_path, new_url in replacements.items():
        # Escape special regex characters in path
        old_path_escaped = re.escape(old_path)
        pattern = f'!\\[([^\\]]*)\\]\\({old_path_escaped}\\)'
        replacement = f'![\\1]({new_url})'
        new_content = re.sub(pattern, replacement, new_content)
        print_color(Colors.GREEN, f"  ✓ Replaced: {old_path} → {new_url}")
    
    # Rebuild markdown with updated frontmatter
    final_content = rebuild_markdown_with_frontmatter(metadata, new_content)
    
    # Write new version
    md_file.write_text(final_content)
    print_color(Colors.GREEN, f"✓ Updated markdown: {md_file}")
    
    return md_file

def upload_memshard(md_file: Path, token: str) -> bool:
    """Upload markdown file as mem_shard"""
    print_color(Colors.BLUE, f"\n🚀 Uploading mem_shard: {md_file.name}")
    
    try:
        with open(md_file, 'rb') as f:
            files = {'markdown_file': (md_file.name, f, 'text/markdown')}
            headers = {'Authorization': f'Token {token}'}
            
            response = requests.post(
                f"{API_BASE_URL}/api/mem_shards/",
                files=files,
                headers=headers
            )
            
            # Check status first before trying to parse JSON
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                result = response.json()
            except json.JSONDecodeError as je:
                print_color(Colors.RED, f"\n✗ Upload failed: Invalid JSON response")
                print_color(Colors.RED, f"  Response status: {response.status_code}")
                print_color(Colors.RED, f"  Response text: {response.text[:500]}")
                return False
            
            print_color(Colors.GREEN, f"\n✅ SUCCESS!")
            print_color(Colors.GREEN, f"  Action: {'Created' if result.get('created', True) else 'Updated'}")
            print_color(Colors.GREEN, f"  ID: {result['id']}")
            print_color(Colors.GREEN, f"  Title: {result['title']}")
            print_color(Colors.GREEN, f"  Slug: {result['slug']}")
            print_color(Colors.GREEN, f"  URL: {result['url']}")
            print_color(Colors.GREEN, f"  Status: {result['status']}")
            
            return True
    except requests.exceptions.RequestException as e:
        print_color(Colors.RED, f"\n✗ Upload failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print_color(Colors.RED, f"  Response status: {e.response.status_code}")
                print_color(Colors.RED, f"  Response text: {e.response.text[:500]}")
            except:
                pass
        return False

def upload_single_image(file_path: Path, alt_text: str, token: str) -> bool:
    """Upload a single image and copy markdown to clipboard"""
    result = upload_image(file_path, alt_text, token)
    
    if result:
        markdown = result['markdown']
        print_color(Colors.GREEN, f"\n✅ Image uploaded successfully!")
        print_color(Colors.GREEN, f"  URL: {result['url']}")
        print_color(Colors.GREEN, f"  Markdown: {markdown}")
        
        # Try to copy to clipboard
        try:
            import subprocess
            subprocess.run(['pbcopy'], input=markdown.encode(), check=True)
            print_color(Colors.GREEN, f"  ✓ Markdown copied to clipboard!")
        except:
            pass
        
        return True
    
    return False

def upload_folder(folder_path: Path, token: str) -> Tuple[int, int]:
    """
    Upload all .md files from a folder
    Returns (success_count, total_count)
    """
    print_color(Colors.BLUE, f"\n📁 Uploading all mem_shards from: {folder_path}")
    
    # Find all .md files
    md_files = sorted(folder_path.glob('*.md'))
    
    if not md_files:
        print_color(Colors.YELLOW, "  No .md files found in folder")
        return 0, 0
    
    print_color(Colors.GREEN, f"  Found {len(md_files)} markdown files\n")
    
    success_count = 0
    total_count = len(md_files)
    
    for idx, md_file in enumerate(md_files, 1):
        print_color(Colors.BLUE, f"\n{'='*60}")
        print_color(Colors.BLUE, f"Processing {idx}/{total_count}: {md_file.name}")
        print_color(Colors.BLUE, f"{'='*60}")
        
        try:
            # Process markdown with images
            processed_file = process_markdown_with_images(md_file, token)
            if processed_file:
                success = upload_memshard(processed_file, token)
                if success:
                    success_count += 1
                    print_color(Colors.GREEN, f"  ✓ {idx}/{total_count} completed")
                else:
                    print_color(Colors.RED, f"  ✗ {idx}/{total_count} failed to upload")
            else:
                print_color(Colors.RED, f"  ✗ {idx}/{total_count} failed to process")
        except Exception as e:
            print_color(Colors.RED, f"  ✗ Error processing {md_file.name}: {e}")
    
    # Summary
    print_color(Colors.BLUE, f"\n{'='*60}")
    print_color(Colors.GREEN, f"📊 UPLOAD SUMMARY")
    print_color(Colors.BLUE, f"{'='*60}")
    print_color(Colors.GREEN, f"  ✓ Successful: {success_count}/{total_count}")
    if success_count < total_count:
        print_color(Colors.RED, f"  ✗ Failed: {total_count - success_count}/{total_count}")
    print_color(Colors.BLUE, f"{'='*60}\n")
    
    return success_count, total_count


def main():
    # Print environment info
    print_color(Colors.BLUE, f"\n{'='*60}")
    print_color(Colors.BLUE, f"🌍 Environment: {ENV_NAME}")
    print_color(Colors.BLUE, f"🔗 API URL: {API_BASE_URL}")
    print_color(Colors.BLUE, f"{'='*60}\n")
    
    if len(sys.argv) < 2:
        print_color(Colors.RED, "Usage:")
        print_color(Colors.YELLOW, "  Upload image:     upload.py <image_file> [alt_text]")
        print_color(Colors.YELLOW, "  Upload mem_shard: upload.py <markdown_file.md>")
        print_color(Colors.YELLOW, "  Upload folder:    upload.py -f <folder_path>")
        print_color(Colors.YELLOW, "\nEnvironment Selection:")
        print_color(Colors.YELLOW, "  Set MEMSHARD_ENV=local|stage|prod (default: local)")
        print_color(Colors.YELLOW, "  Or use wrapper: ./upload [local|stage|prod] <file>")
        print_color(Colors.YELLOW, "\nExamples:")
        print_color(Colors.YELLOW, "  upload.py /path/to/photo.jpg \"My Photo\"")
        print_color(Colors.YELLOW, "  upload.py /absolute/path/to/post.md")
        print_color(Colors.YELLOW, "  upload.py ./relative/path/to/post.md")
        print_color(Colors.YELLOW, "  upload.py -f ./bulk_mem_shards/")
        print_color(Colors.YELLOW, "  ./upload stage post.md")
        print_color(Colors.YELLOW, "  ./upload prod -f ./bulk/")
        sys.exit(1)
    
    # Check for folder upload flag
    if sys.argv[1] == '-f':
        if len(sys.argv) < 3:
            print_color(Colors.RED, "✗ Please specify a folder path after -f")
            sys.exit(1)
        
        folder_arg = sys.argv[2]
        folder_path = Path(folder_arg).resolve()
        
        if not folder_path.exists():
            print_color(Colors.RED, f"✗ Folder not found: {folder_path}")
            sys.exit(1)
        
        if not folder_path.is_dir():
            print_color(Colors.RED, f"✗ Not a directory: {folder_path}")
            sys.exit(1)
        
        # Get authentication token
        token = get_token()
        if not token:
            sys.exit(1)
        
        # Upload all files in folder
        success_count, total_count = upload_folder(folder_path, token)
        sys.exit(0 if success_count == total_count else 1)
    
    # Single file upload (original behavior)
    file_arg = sys.argv[1]
    file_path = Path(file_arg).resolve()
    
    if not file_path.exists():
        print_color(Colors.RED, f"✗ File not found: {file_path}")
        sys.exit(1)
    
    print_color(Colors.BLUE, f"📁 Working with: {file_path}")
    
    # Get authentication token
    token = get_token()
    if not token:
        sys.exit(1)
    
    # Determine file type
    if file_path.suffix.lower() == '.md':
        # Process markdown with images
        processed_file = process_markdown_with_images(file_path, token)
        if processed_file:
            success = upload_memshard(processed_file, token)
            sys.exit(0 if success else 1)
        else:
            sys.exit(1)
    else:
        # Upload single image
        alt_text = sys.argv[2] if len(sys.argv) > 2 else file_path.stem
        success = upload_single_image(file_path, alt_text, token)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
