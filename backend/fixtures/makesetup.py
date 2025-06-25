import json
FILE = 'backend/fixtures/initial_templates2.json'
# Define templates and starting data for vanilla Diplomacy
countries = {
    "E": {"name": "England", "scs": 3},
    "F": {"name": "France", "scs": 3},
    "G": {"name": "Germany", "scs": 3},
    "R": {"name": "Russia", "scs": 4},
    "T": {"name": "Turkey", "scs": 3},
    "I": {"name": "Italy", "scs": 3},
    "A": {"name": "Austria", "scs": 3},
}

# Territories, coasts, and initial unit positions taken from Diplomacy standard setup
territories = [
    # Supply Centers (34)
    ("Ank", "Ankara", "L", True, True, "T", True),
    ("Bel", "Belgium", "L", True, True, None, False),
    ("Ber", "Berlin", "L", True, True, "G", True),
    ("Bre", "Brest", "L", True, True, "F", True),
    ("Bud", "Budapest", "L", False, True, "A", True),
    ("Bul", "Bulgaria", "L", True, True, None, False),
    ("Con", "Constantinople", "L", True, True, "T", True),
    ("Den", "Denmark", "L", True, True, None, False),
    ("Edi", "Edinburgh", "L", True, True, "E", True),
    ("Gre", "Greece", "L", True, True, None, False),
    ("Hol", "Holland", "L", True, True, None, False),
    ("Kie", "Kiel", "L", True, True, "G", True),
    ("Lvp", "Liverpool", "L", True, True, "E", True),
    ("Lon", "London", "L", True, True, "E", True),
    ("Mar", "Marseilles", "L", True, True, "F", True),
    ("Mos", "Moscow", "L", False, True, "R", True),
    ("Mun", "Munich", "L", False, True, "G", True),
    ("Nap", "Naples", "L", True, True, "I", True),
    ("Nor", "Norway", "L", True, True, None, False),
    ("Par", "Paris", "L", False, True, "F", True),
    ("Por", "Portugal", "L", True, True, None, False),
    ("Rom", "Rome", "L", True, True, "I", True),
    ("Rum", "Rumania", "L", True, True, None, False),
    ("Ser", "Serbia", "L", False, True, None, False),
    ("Sev", "Sevastopol", "L", True, True, "R", True),
    ("Smy", "Smyrna", "L", True, True, "T", True),
    ("Spa", "Spain", "L", True, True, None, False),
    ("Swe", "Sweden", "L", True, True, None, False),
    ("Stp", "St. Petersburg", "L", True, True, "R", True),
    ("Tri", "Trieste", "L", True, True, "A", True),
    ("Tun", "Tunis", "L", True, True, None, False),
    ("Ven", "Venice", "L", True, True, "I", True),
    ("Vie", "Vienna", "L", False, True, "A", True),
    ("War", "Warsaw", "L", False, True, "R", True),

    # Other Land Territories (22)
    ("Alb", "Albania", "L", True, False, None, False),
    ("Apu", "Apulia", "L", True, False, None, False),
    ("Arm", "Armenia", "L", True, False, None, False),
    ("Boh", "Bohemia", "L", False, False, None, False),
    ("Bur", "Burgundy", "L", False, False, None, False),
    ("Cly", "Clyde", "L", True, False, None, False),
    ("Fin", "Finland", "L", True, False, None, False),
    ("Gal", "Galicia", "L", False, False, None, False),
    ("Gas", "Gascony", "L", True, False, None, False),
    ("Lvn", "Livonia", "L", True, False, None, False),
    ("NAf", "North Africa", "L", True, False, None, False),
    ("Pic", "Picardy", "L", True, False, None, False),
    ("Pie", "Piedmont", "L", True, False, None, False),
    ("Pru", "Prussia", "L", True, False, None, False),
    ("Ruh", "Ruhr", "L", False, False, None, False),
    ("Sil", "Silesia", "L", False, False, None, False),
    ("Syr", "Syria", "L", True, False, None, False),
    ("Tus", "Tuscany", "L", True, False, None, False),
    ("Tyr", "Tyrolia", "L", False, False, None, False),
    ("Ukr", "Ukraine", "L", False, False, None, False),
    ("Wal", "Wales", "L", True, False, None, False),
    ("Yor", "Yorkshire", "L", True, False, None, False),

   # Sea Territories (19)
    ("ADR", "Adriatic Sea", "S", False, False, None, False),
    ("AEG", "Aegean Sea", "S", False, False, None, False),
    ("BAL", "Baltic Sea", "S", False, False, None, False),
    ("BAR", "Barents Sea", "S", False, False, None, False),
    ("BLA", "Black Sea", "S", False, False, None, False),
    ("EAS", "Eastern Mediterranean", "S", False, False, None, False),
    ("ENG", "English Channel", "S", False, False, None, False),
    ("BOT", "Gulf of Bothnia", "S", False, False, None, False),
    ("HEL", "Heligoland Bight", "S", False, False, None, False),
    ("ION", "Ionian Sea", "S", False, False, None, False),
    ("IRI", "Irish Sea", "S", False, False, None, False),
    ("MAO", "Mid-Atlantic Ocean", "S", False, False, None, False),
    ("NAO", "North Atlantic Ocean", "S", False, False, None, False),
    ("NTH", "North Sea", "S", False, False, None, False),
    ("NWG", "Norwegian Sea", "S", False, False, None, False),
    ("SKA", "Skagerrak", "S", False, False, None, False),
    ("TYR", "Tyrrhenian Sea", "S", False, False, None, False),
    ("WES", "Western Mediterranean", "S", False, False, None, False),
    ("LYO", "Gulf of Lyon", "S", False, False, None, False),
]

coast_mapping = {
    "Bul": ["ec", "sc"],
    "Spa": ["nc", "sc"],
    "Stp": ["nc", "sc"]
}

coast_full_name = {
    "nc": "North",
    "sc": "South",
    "ec": "East"
}

units = [
    ("Lon", "E", "F", "Lon"),
    ("Edi", "E", "F", "Edi"),
    ("Lvp", "E", "A", None),
    ("Bre", "F", "F", "Bre"),
    ("Par", "F", "A", None),
    ("Mar", "F", "A", None),
    ("Ber", "G", "A", None),
    ("Mun", "G", "A", None),
    ("Kie", "G", "F", "Kie"),
    ("Vie", "A", "A", None),
    ("Bud", "A", "A", None),
    ("Tri", "A", "F", "Tri"),
    ("Ven", "I", "A", None),
    ("Rom", "I", "A", None),
    ("Nap", "I", "F", "Nap"),
    ("Mos", "R", "A", None),
    ("Sev", "R", "F", "Sev"),
    ("War", "R", "A", None),
    ("Stp", "R", "F", "sc"),
    ("Con", "T", "A", None),
    ("Smy", "T", "A", None),
    ("Ank", "T", "F", "Ank"),
]

data = []
names = [
    'England',
    'France',
    'Germany',
    'Russia',
    'Turkey',
    'Italy',
    'Austria'
]

pk = 1
for name in names:
    entry = {
        'model': 'api.countrytemplate',
        'pk': pk,
        'fields':{
            'name' : name[0],
            'full_name' : name
        }
    }
    data.append(entry)
    pk+=1

pk_counter = 1
territory_pk = {}
coast_pk = {}
# Add TerritoryTemplate
for name, full_name, ttype, has_coasts, sc, owner, home_center in territories:
    entry = {
        "model": "api.territorytemplate",
        "pk": pk_counter,
        "fields": {
            "name": name,
            "full_name": full_name,
            "sc_exists": sc,
            "territory_type": ttype,
            "has_coasts": has_coasts,
            "country_template": None,
            "home_center": home_center
        }
    }
    if owner:
        entry["fields"]["country_template"] = list(countries.keys()).index(owner) + 1
    data.append(entry)
    territory_pk[name] = pk_counter
    pk_counter += 1

# Add CoastTemplates
for name, full_name, ttype, has_coasts, sc, owner, home_center in territories:
    if ttype != "L" or not has_coasts:
        continue
    if name in coast_mapping:
        for coast in coast_mapping[name]:
            coast_name = f"{name}/{coast}"
            coast_full = f"{full_name} {coast_full_name[coast]} Coast"
            coast_entry = {
                "model": "api.coasttemplate",
                "pk": pk_counter,
                "fields": {
                    "territory_template": territory_pk[name],
                    "name": coast_name,
                    "full_name": coast_full
                }
            }
            coast_pk[coast_name] = pk_counter
            data.append(coast_entry)
            pk_counter += 1
    else:
        coast_name = name
        coast_full = f"{full_name} Coast"
        coast_entry = {
            "model": "api.coasttemplate",
            "pk": pk_counter,
            "fields": {
                "territory_template": territory_pk[name],
                "name": coast_name,
                "full_name": coast_full
            }
        }
        coast_pk[coast_name] = pk_counter
        data.append(coast_entry)
        pk_counter += 1

# Add InitialUnitSetup
for terr, country, utype, coast in units:
    coast_name = ''
    if coast:
        if len(coast) == 3:
            coast_name = coast
        else:
            coast_name = f"{terr}/{coast}"
    entry = {
        "model": "api.initialunitsetup",
        "pk": pk_counter,
        "fields": {
            "territory_template": territory_pk[terr],
            "country_template": list(countries.keys()).index(country) + 1,
            "unit_type": utype,
            "coast_template": coast_pk[coast_name] if coast else None
        }
    }
    data.append(entry)
    pk_counter += 1


# Save JSON
with open(FILE, "w") as f:
    json.dump(data, f, indent=2)
