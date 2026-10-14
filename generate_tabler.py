# generate_tabler.py
import json
import os
from bs4 import BeautifulSoup, Comment

from upstream import clone_release, reset_output_dir

TABLER_REPO_NAME = "tabler-icons-repo" # Local directory name for the cloned repository

def process_svg_tag(svg_path, variant_name): # variant_name is kept for potential future use but not used for this logic
    """Extract and process SVG content from a file for Tabler Icons"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error reading or parsing SVG file {svg_path}: {e}")
        return ""

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    svg = soup.find('svg')
    if not svg:
        print(f"Warning: No <svg> tag found in {svg_path} after attempting to remove comments.")
        return ""

    if 'width' in svg.attrs:
        del svg.attrs['width']
    if 'height' in svg.attrs:
        del svg.attrs['height']

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

    # stroke="currentColor" and fill="currentColor" (or fill="none") from the original SVG
    # will be preserved. Users can override these via {{ attrs }} if they pass
    # stroke="..." or fill="..." on the component tag.
    # No specific replacement for fill="{{ fill }}" is done here anymore.

    return svg_content

def combine_icon_variants(icon_name, variants_content_map):
    """Combine all variants of an icon into a single Django template for Tabler Icons"""
    template_parts = []
    # Simplified <c-vars>: only sets default variant and core stroke presentation attributes.
    # stroke color and fill color will come from the SVG itself or user overrides.
    template_parts.append(
        '<c-vars variant="outline" stroke_width="2" stroke_linecap="round" stroke_linejoin="round" aria-hidden="true" />\n\n'
    )

    for variant_name, svg_string in variants_content_map.items():
        if svg_string:
            template_parts.append(f"{{% if variant == '{variant_name}' %}}\n")
            template_parts.append(svg_string + "\n")
            template_parts.append("{% endif %}\n\n")

    return "".join(template_parts).strip() + "\n"


def get_filled_svg_filename(basename, filled_dir_path):
    """
    Tries to find the correct filename for a filled Tabler icon.
    Returns the full path if found, otherwise None.
    """
    name_with_suffix = f"{basename}-filled.svg"
    path_with_suffix = os.path.join(filled_dir_path, name_with_suffix)
    if os.path.exists(path_with_suffix):
        return path_with_suffix

    name_without_suffix = f"{basename}.svg"
    path_without_suffix = os.path.join(filled_dir_path, name_without_suffix)
    if os.path.exists(path_without_suffix):
        return path_without_suffix

    return None


def generate_cotton_components(tabler_repo_root_dir, output_dir, version):
    """Generate combined Cotton components from Tabler Icons"""
    tabler_icons_base_svg_path = os.path.join(tabler_repo_root_dir, "icons")

    outline_dir = os.path.join(tabler_icons_base_svg_path, 'outline')
    filled_dir = os.path.join(tabler_icons_base_svg_path, 'filled')

    icon_map = {
        'tablericons_version': version,
        'styles_source_subdirs': {'outline': 'outline', 'filled': 'filled'},
        'icons': []
    }

    reset_output_dir(output_dir)

    all_icon_base_names = set()
    if os.path.isdir(outline_dir):
        for filename_svg in os.listdir(outline_dir):
            if filename_svg.endswith('.svg'):
                all_icon_base_names.add(os.path.splitext(filename_svg)[0])
    else:
        print(f"Warning: Outline directory not found: {outline_dir}")
        if os.path.isdir(filled_dir):
            print(f"Attempting to get base names from filled directory: {filled_dir}")
            for filename_svg in os.listdir(filled_dir):
                if filename_svg.endswith('.svg'):
                    base_name = os.path.splitext(filename_svg)[0]
                    if base_name.endswith('-filled'):
                        base_name = base_name[:-len('-filled')]
                    all_icon_base_names.add(base_name)
        else:
            print(f"Warning: Filled directory also not found: {filled_dir}. Cannot collect icon names.")


    icon_map['icons'] = sorted(list(all_icon_base_names))
    if not icon_map['icons']:
        print("Error: No icon base names collected. Exiting generation for Tabler Icons.")
        return

    generated_count = 0
    for icon_base_name in icon_map['icons']:
        variants_processed_content = {}

        outline_svg_filepath = os.path.join(outline_dir, f"{icon_base_name}.svg")
        if os.path.exists(outline_svg_filepath):
            processed_svg_string = process_svg_tag(outline_svg_filepath, 'outline')
            if processed_svg_string:
                variants_processed_content['outline'] = processed_svg_string

        if os.path.isdir(filled_dir):
            filled_svg_filepath = get_filled_svg_filename(icon_base_name, filled_dir)
            if filled_svg_filepath and os.path.exists(filled_svg_filepath):
                processed_svg_string = process_svg_tag(filled_svg_filepath, 'filled')
                if processed_svg_string:
                    variants_processed_content['filled'] = processed_svg_string

        if variants_processed_content:
            combined_html_content = combine_icon_variants(icon_base_name, variants_processed_content)
            output_filename_html = f"{icon_base_name.replace('-', '_')}.html"
            output_filepath_html = os.path.join(output_dir, output_filename_html)

            try:
                with open(output_filepath_html, 'w', encoding='utf-8') as f:
                    f.write(combined_html_content)
                generated_count += 1
            except Exception as e:
                print(f"Error writing template file {output_filepath_html}: {e}")

    print(f"Generated {generated_count} combined icon templates for Tabler Icons in {output_dir} (from {len(icon_map['icons'])} unique base icon names).")

    icon_map_path = os.path.join(output_dir, 'icon_map.json')
    try:
        with open(icon_map_path, 'w', encoding='utf-8') as f:
            json.dump(icon_map, f, indent=2, sort_keys=True)
        print(f"Generated Tabler Icons icon map: {icon_map_path}")
    except Exception as e:
        print(f"Error writing icon map file {icon_map_path}: {e}")

    print(f"Successfully processed Tabler Icons version: {version}")


if __name__ == "__main__":
    output_dir_tabler = "cotton_icons/templates/cotton/tablericon"

    tag = clone_release("tabler/tabler-icons", TABLER_REPO_NAME)
    generate_cotton_components(TABLER_REPO_NAME, output_dir_tabler, version=tag.lstrip("v"))
