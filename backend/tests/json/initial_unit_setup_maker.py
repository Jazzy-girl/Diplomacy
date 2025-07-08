import json
from collections import defaultdict

REF_FILE = 'backend/tests/json/templates.json'
OUTPUT_FILE = 'backend/tests/json/retreat_setup_1.json'



"""
EDIT THIS!

--Format--
    territory name : [unit type, country name]
"""
TERRITORY_LIST = {
    'Ruh' : ["A", 'F'],
    'Kie' : ["A", 'F'],
    'Ber' : ["A", 'F'],
    'Mun' : ["A", 'G'],
    'Boh' : ["A", 'G']
}

def get_territory_fks():
    """
    Returns a dict of <territory name> : <TerritoryTemplate PK>
    """

    #key: territory name; values 0: template_pk, 1: unit_type, 2: country_pk
    territory_map = dict()
    country_map = dict()
    unit_map = dict()

    with open(REF_FILE, 'r') as f:
        templates = json.load(f)

    for territory, values in TERRITORY_LIST.items():
        unit_type = values[0]
        country = values[1]
        unit_map[territory] = unit_type
        for obj in templates:
            if obj['model'] == 'api.territorytemplate' and obj['fields']['name'] == territory:
                territory_map[territory] = obj['pk']
            elif obj['model'] == "api.countrytemplate" and obj['fields']['name'] == country:
                country_map[territory] = obj['pk']
            # elif 'Coast' in territory...
    write_output(territory_map, country_map, unit_map)

def write_output(territory_map={}, country_map={}, unit_map={}):
    """
    Writes all the InitialUnitSetup entries into the OUTPUT_FILE json file

    :param dict territory_map: territory name - TerritoryTemplate PK
    :param dict country_map: territory name - CountryTemplate PK
    :param dict unit_map: territory name - unit type (A / F);
    """
    # All army units!
    data = [{"model": "api.initialunitsetup", "pk": pk, "fields" : {"territory_template": territory_map[territory], 
            "country_template" : country_map[territory], "unit_type": unit_map[territory], "coast_template" : None}}
            for pk, territory in enumerate(territory_map.keys())]

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def make():
    get_territory_fks()

if __name__ == "__main__":
    make()