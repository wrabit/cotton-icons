# generate_lucide.py
import json
import os
from bs4 import BeautifulSoup, Comment

from upstream import clone_release, reset_output_dir

LUCIDE_REPO_NAME = "lucide-repo"  # Local directory name for the cloned repository


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
    # Icons are decorative by default; the hyphenated c-vars key lets a caller's
    # aria-hidden="false" replace the default instead of duplicating the attribute.
    svg.attrs.pop('aria-hidden', None)
    svg['attrs'] = ''
    svg_content = str(svg)
    svg_content = svg_content.replace('attrs=""', '{{ attrs }}')
    svg_content = svg_content.replace('{{ attrs }}', '{{ attrs }} aria-hidden="{{ aria_hidden }}"')

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
        '<c-vars stroke_width="2" stroke_linecap="round" stroke_linejoin="round" aria-hidden="true" />\n\n'
    )
    template_parts.append(svg_content + "\n")

    return "".join(template_parts).strip() + "\n"


def write_alias_templates(icons_path, output_dir, icon_names):
    """Mirror Lucide's deprecated aliases as forwarding components.

    Lucide records renamed and duplicate icons in each icon's JSON ``aliases``
    and its packages re-export them with a deprecation notice, so old names
    keep working. Each alias here is a template that proxies all attributes
    to the real icon, so it renders identically.
    """
    namespace = os.path.basename(output_dir)
    aliases = {}
    for icon_name in icon_names:
        meta_path = os.path.join(icons_path, f"{icon_name}.json")
        if not os.path.exists(meta_path):
            continue
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        for alias in meta.get("aliases", []):
            alias_name = alias["name"] if isinstance(alias, dict) else alias
            if alias_name in icon_names:
                print(f"Warning: alias {alias_name} of {icon_name} clashes with an icon, skipped")
                continue
            reason = alias.get("deprecationReason", "alias") if isinstance(alias, dict) else "alias"
            aliases[alias_name] = icon_name
            template = (
                f"{{# Deprecated alias of {icon_name} ({reason}) #}}\n"
                f'<c-{namespace}.{icon_name} :attrs="attrs" />\n'
            )
            with open(os.path.join(output_dir, f"{alias_name.replace('-', '_')}.html"), "w", encoding="utf-8") as f:
                f.write(template)
    return aliases


def generate_cotton_components(lucide_repo_root_dir, output_dir, version, source="icons"):
    """Generate Cotton components from a Lucide icon directory (``icons`` or ``lab``)"""
    lucide_icons_path = os.path.join(lucide_repo_root_dir, source)

    if not os.path.isdir(lucide_icons_path):
        print(f"Error: Icons directory not found: {lucide_icons_path}")
        return

    icon_map = {
        'lucideicons_version': version,
        'source': source,
        'icons': []
    }

    reset_output_dir(output_dir)

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

    icon_map['aliases'] = write_alias_templates(lucide_icons_path, output_dir, set(icon_map['icons']))
    print(f"Generated {len(icon_map['aliases'])} alias templates in {output_dir}")

    icon_map_path = os.path.join(output_dir, 'icon_map.json')
    try:
        with open(icon_map_path, 'w', encoding='utf-8') as f:
            json.dump(icon_map, f, indent=2, sort_keys=True)
        print(f"Generated Lucide Icons icon map: {icon_map_path}")
    except Exception as e:
        print(f"Error writing icon map file {icon_map_path}: {e}")

    print(f"Successfully processed Lucide Icons version: {version}")


if __name__ == "__main__":
    tag = clone_release("lucide-icons/lucide", LUCIDE_REPO_NAME)
    generate_cotton_components(LUCIDE_REPO_NAME, "cotton_icons/templates/cotton/lucideicon", version=tag)
    # Lucide Lab moved into the main repo in 1.27.0; it ships as its own namespace
    # so experimental icons are visible at the call site and can never shadow main ones.
    generate_cotton_components(LUCIDE_REPO_NAME, "cotton_icons/templates/cotton/lucidelab", version=tag, source="lab")
