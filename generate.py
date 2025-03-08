import json
import os
import subprocess
import shutil
from bs4 import BeautifulSoup
import sys


def download_heroicons_repo():
    """Download the Heroicons repository from GitHub"""
    print("Downloading Heroicons repository...")

    # Check if the heroicons directory already exists
    if os.path.exists("heroicons"):
        print("Heroicons directory already exists. Removing it to get the latest version...")
        shutil.rmtree("heroicons")

    # Clone the repository
    try:
        subprocess.run(
            ["git", "clone", "https://github.com/tailwindlabs/heroicons.git"],
            check=True
        )
        print("Successfully downloaded Heroicons repository.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading Heroicons repository: {e}")
        return False

def get_version(heroicons_dir):
    """Extract heroicons version from package.json"""
    package_json_path = os.path.join(heroicons_dir, '..', 'package.json')
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)
    return package_data.get('version', 'Unknown')


def process_svg_tag(svg_path):
    """Extract and process SVG content from a file"""
    with open(svg_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    svg = soup.find('svg')
    svg['attrs'] = ''  # Add Cotton-specific attribute placeholder

    svg_content = str(svg)

    # Replace attributes with template variables
    svg_content = svg_content.replace('attrs=""', '{{ attrs }}')
    svg_content = svg_content.replace('stroke-width="1.5"', 'stroke-width="{{ stroke_width }}"')
    svg_content = svg_content.replace('stroke-linecap="round"', 'stroke-linecap="{{ stroke_linecap }}"')
    svg_content = svg_content.replace('stroke-linejoin="round"', 'stroke-linejoin="{{ stroke_linejoin }}"')

    return svg_content


def combine_icon_variants(icon_name, variants):
    """Combine all variants of an icon into a single Django template"""
    template = ""

    # Add the Cotton variables for outline variant
    template += """<c-vars variant="outline" stroke_width="1.5" stroke_linecap="round" stroke_linejoin="round" />\n\n"""

    # Add each variant with Django if statements
    for variant, content in variants.items():
        template += f"{{% if variant == '{variant}' %}}\n"
        template += content + "\n"
        template += "{% endif %}\n\n"

    return template


def generate_cotton_components(heroicons_dir, output_dir):
    """Generate combined Cotton components from Heroicons"""
    # Define style mappings
    styles = {
        'outline': {'source': '24/outline'},
        'solid': {'source': '24/solid'},
        'mini': {'source': '20/solid'},
        'micro': {'source': '16/solid'}
    }

    # Get heroicons version
    heroicons_version = get_version(heroicons_dir)

    # Create icon map for metadata
    icon_map = {
        'heroicons_version': heroicons_version,
        'styles': styles,
        'icons': []
    }

    # Create combined output directory
    os.makedirs(output_dir, exist_ok=True)

    # First, collect all icon names from all styles
    all_icons = set()
    for style, info in styles.items():
        source_path = os.path.join(heroicons_dir, info['source'])
        for file in os.listdir(source_path):
            if file.endswith('.svg'):
                all_icons.add(os.path.splitext(file)[0])

    # Sort icon names
    icon_map['icons'] = sorted(list(all_icons))

    # Process each icon
    for icon_name in all_icons:
        variants = {}

        # Process each style variant if available
        for style, info in styles.items():
            source_path = os.path.join(heroicons_dir, info['source'])
            svg_path = os.path.join(source_path, f"{icon_name}.svg")

            if os.path.exists(svg_path):
                variants[style] = process_svg_tag(svg_path)

        # Create combined template
        if variants:
            combined_content = combine_icon_variants(icon_name, variants)

            # Write to file
            output_file = os.path.join(output_dir, f"{icon_name.replace('-', '_')}.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(combined_content)

            print(f"Generated combined icon: {output_file}")

    # Write icon map to JSON
    with open(os.path.join(output_dir, 'icon_map.json'), 'w', encoding='utf-8') as f:
        json.dump(icon_map, f, indent=2)

    print(f"Generated icon map with {len(all_icons)} icons")


if __name__ == "__main__":
    # Update these paths as needed
    heroicons_dir = "heroicons/optimized"
    output_dir = "django_cotton_heroicons/templates/cotton/heroicon"

    # Download heroicons repository
    if not download_heroicons_repo():
        sys.exit("Failed to download Heroicons repository. Exiting.")

    # Generate components
    generate_cotton_components(heroicons_dir, output_dir)