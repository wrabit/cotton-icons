# generate_lucide.py
import json
import os
import subprocess
import shutil
from bs4 import BeautifulSoup, Comment
import sys

LUCIDE_REPO_NAME = "lucide-repo"  # Local directory name for the cloned repository


def download_lucide_repo():
    """Download the Lucide Icons repository from GitHub"""
    print("Downloading Lucide Icons repository...")
    repo_url = "https://github.com/lucide-icons/lucide.git"

    if os.path.exists(LUCIDE_REPO_NAME):
        print(f"Directory '{LUCIDE_REPO_NAME}' already exists. Removing it to get the latest version...")
        shutil.rmtree(LUCIDE_REPO_NAME)

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, LUCIDE_REPO_NAME],
            check=True, capture_output=True, text=True
        )
        print("Successfully downloaded Lucide Icons repository.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading Lucide Icons repository: {e}")
        print(f"Git Stderr: {e.stderr}")
        return False


def get_version(repo_root_dir):
    """Extract version from GitHub API releases (Lucide is a monorepo without version in root package.json)"""
    import urllib.request
    import re
    try:
        # Get the latest release from GitHub API
        req = urllib.request.Request(
            "https://api.github.com/repos/lucide-icons/lucide/releases/latest",
            headers={"User-Agent": "cotton-icons"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            tag = data.get("tag_name", "")
            # Strip 'v' prefix if present
            return tag.lstrip('v') if tag else "Unknown"
    except Exception as e:
        print(f"Warning: Could not get version from GitHub API: {e}")
        return "Unknown"


def process_svg_tag(svg_path):
    """Extract and process SVG content from a file for Lucide Icons"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error reading or parsing SVG file {svg_path}: {e}")
        return ""

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    svg = soup.find('svg')
    if not svg:
        print(f"Warning: No <svg> tag found in {svg_path} after attempting to remove comments.")
        return ""

    # Remove width and height attributes (let CSS control sizing)
    if 'width' in svg.attrs:
        del svg.attrs['width']
    if 'height' in svg.attrs:
        del svg.attrs['height']

    # Add attrs placeholder for Cotton
    svg['attrs'] = ''
    svg_content = str(svg)
    svg_content = svg_content.replace('attrs=""', '{{ attrs }}')

    # Template common stroke presentation attributes
    svg_content = svg_content.replace('stroke-width="2"', 'stroke-width="{{ stroke_width }}"')
    svg_content = svg_content.replace('stroke-linecap="round"', 'stroke-linecap="{{ stroke_linecap }}"')
    svg_content = svg_content.replace('stroke-linejoin="round"', 'stroke-linejoin="{{ stroke_linejoin }}"')

    return svg_content


def create_icon_template(svg_content):
    """Create a Django Cotton template for a Lucide icon"""
    template_parts = []
    # Lucide icons are stroke-based, similar to outline style
    template_parts.append(
        '<c-vars stroke_width="2" stroke_linecap="round" stroke_linejoin="round" />\n\n'
    )
    template_parts.append(svg_content + "\n")

    return "".join(template_parts).strip() + "\n"


def generate_cotton_components(lucide_repo_root_dir, output_dir):
    """Generate Cotton components from Lucide Icons"""
    lucide_icons_path = os.path.join(lucide_repo_root_dir, "icons")

    if not os.path.isdir(lucide_icons_path):
        print(f"Error: Icons directory not found: {lucide_icons_path}")
        return

    lucide_version = get_version(lucide_repo_root_dir)
    print(f"Lucide Icons version detected: {lucide_version}")

    icon_map = {
        'lucideicons_version': lucide_version,
        'icons': []
    }

    os.makedirs(output_dir, exist_ok=True)

    # Collect all icon base names
    all_icon_base_names = set()
    for filename in os.listdir(lucide_icons_path):
        if filename.endswith('.svg'):
            all_icon_base_names.add(os.path.splitext(filename)[0])

    icon_map['icons'] = sorted(list(all_icon_base_names))
    if not icon_map['icons']:
        print("Error: No icon names collected. Exiting generation for Lucide Icons.")
        return

    generated_count = 0
    for icon_base_name in icon_map['icons']:
        svg_filepath = os.path.join(lucide_icons_path, f"{icon_base_name}.svg")

        if os.path.exists(svg_filepath):
            processed_svg = process_svg_tag(svg_filepath)
            if processed_svg:
                html_content = create_icon_template(processed_svg)
                output_filename = f"{icon_base_name.replace('-', '_')}.html"
                output_filepath = os.path.join(output_dir, output_filename)

                try:
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    generated_count += 1
                except Exception as e:
                    print(f"Error writing template file {output_filepath}: {e}")

    print(f"Generated {generated_count} icon templates for Lucide Icons in {output_dir}")

    icon_map_path = os.path.join(output_dir, 'icon_map.json')
    try:
        with open(icon_map_path, 'w', encoding='utf-8') as f:
            json.dump(icon_map, f, indent=2, sort_keys=True)
        print(f"Generated Lucide Icons icon map: {icon_map_path}")
    except Exception as e:
        print(f"Error writing icon map file {icon_map_path}: {e}")

    print(f"Successfully processed Lucide Icons version: {lucide_version}")


if __name__ == "__main__":
    output_dir_lucide = "cotton_icons/templates/cotton/lucideicon"

    if not download_lucide_repo():
        sys.exit("Failed to download Lucide Icons repository. Exiting.")

    generate_cotton_components(LUCIDE_REPO_NAME, output_dir_lucide)
