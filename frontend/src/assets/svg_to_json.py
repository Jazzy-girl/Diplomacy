import xml.etree.ElementTree as ET
import json

def parse_svg_to_json(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Handle namespaces (Inkscape includes them)
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    territories = {}

    for path in root.findall('.//svg:path', ns):
        id_ = path.attrib.get('id')
        d = path.attrib.get('d')

        if id_ and d:
            territories[id_] = {
                'path': d,
                # Optional placeholders for future game data
                'type': 'l',  # l = land, w = water — set manually later
                'neighbors': [],
                'unit_center': None,
                'sc': None
            }

    return territories

# Example usage
svg_file = 'map.svg'
output_json = 'territories.json'

territories = parse_svg_to_json(svg_file)

with open(output_json, 'w') as f:
    json.dump(territories, f, indent=2)

print(f"Exported {len(territories)} territories to {output_json}")
