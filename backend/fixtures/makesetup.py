import json

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
    ("Ank", "Ankara", "L", True, True, "T"),
    ("Bel", "Belgium", "L", True, True, None),
    ("Ber", "Berlin", "L", True, True, "G"),
    ("Bre", "Brest", "L", True, True, "F"),
    ("Bud", "Budapest", "L", False, True, "A"),
    ("Bul", "Bulgaria", "L", True, True, "T"),
    ("Con", "Constantinople", "L", True, True, "T"),
    ("Den", "Denmark", "L", True, True, None),
    ("Edi", "Edinburgh", "L", True, True, "E"),
    ("Gre", "Greece", "L", True, True, None),
    ("Hol", "Holland", "L", True, True, None),
    ("Kie", "Kiel", "L", True, True, "G"),
    ("Lvp", "Liverpool", "L", True, True, "E"),
    ("Lon", "London", "L", True, True, "E"),
    ("Mar", "Marseilles", "L", True, True, "F"),
    ("Mos", "Moscow", "L", False, True, "R"),
    ("Mun", "Munich", "L", False, True, "G"),
    ("Nap", "Naples", "L", True, True, "I"),
    ("Nor", "Norway", "L", True, True, None),
    ("Par", "Paris", "L", False, True, "F"),
    ("Por", "Portugal", "L", True, True, None),
    ("Rom", "Rome", "L", True, True, "I"),
    ("Rum", "Rumania", "L", True, True, None),
    ("Ser", "Serbia", "L", False, True, None),
    ("Sev", "Sevastopol", "L", True, True, "R"),
    ("Smy", "Smyrna", "L", True, True, "T"),
    ("Spa", "Spain", "L", True, True, None),
    ("Swe", "Sweden", "L", True, True, None),
    ("Stp", "St. Petersburg", "L", True, True, "R"),
    ("Tri", "Trieste", "L", True, True, "A"),
    ("Tun", "Tunis", "L", True, True, None),
    ("Ven", "Venice", "L", True, True, "I"),
    ("Vie", "Vienna", "L", False, True, "A"),
    ("War", "Warsaw", "L", False, True, "R"),

    # Other Land Territories (22)
    ("Alb", "Albania", "L", True, False, None),
    ("Apu", "Apulia", "L", True, False, None),
    ("Arm", "Armenia", "L", True, False, None),
    ("Boh", "Bohemia", "L", False, False, None),
    ("Bur", "Burgundy", "L", False, False, None),
    ("Cly", "Clyde", "L", True, False, None),
    ("Fin", "Finland", "L", True, False, None),
    ("Gal", "Galicia", "L", False, False, None),
    ("Gas", "Gascony", "L", True, False, None),
    ("Lvn", "Livonia", "L", True, False, None),
    ("NAf", "North Africa", "L", True, False, None),
    ("Pic", "Picardy", "L", True, False, None),
    ("Pie", "Piedmont", "L", True, False, None),
    ("Pru", "Prussia", "L", True, False, None),
    ("Ruh", "Ruhr", "L", False, False, None),
    ("Sil", "Silesia", "L", False, False, None),
    ("Syr", "Syria", "L", True, False, None),
    ("Tus", "Tuscany", "L", True, False, None),
    ("Tyr", "Tyrolia", "L", False, False, None),
    ("Ukr", "Ukraine", "L", False, False, None),
    ("Wal", "Wales", "L", True, False, None),
    ("Yor", "Yorkshire", "L", True, False, None),

   # Sea Territories (19)
    ("ADR", "Adriatic Sea", "S", False, False, None),
    ("AEG", "Aegean Sea", "S", False, False, None),
    ("BAL", "Baltic Sea", "S", False, False, None),
    ("BAR", "Barents Sea", "S", False, False, None),
    ("BLA", "Black Sea", "S", False, False, None),
    ("EAS", "Eastern Mediterranean", "S", False, False, None),
    ("ENG", "English Channel", "S", False, False, None),
    ("BOT", "Gulf of Bothnia", "S", False, False, None),
    ("HEL", "Heligoland Bight", "S", False, False, None),
    ("ION", "Ionian Sea", "S", False, False, None),
    ("IRI", "Irish Sea", "S", False, False, None),
    ("MAO", "Mid-Atlantic Ocean", "S", False, False, None),
    ("NAO", "North Atlantic Ocean", "S", False, False, None),
    ("NTH", "North Sea", "S", False, False, None),
    ("NWG", "Norwegian Sea", "S", False, False, None),
    ("SKA", "Skagerrak", "S", False, False, None),
    ("TYR", "Tyrrhenian Sea", "S", False, False, None),
    ("WES", "Western Mediterranean", "S", False, False, None),
    ("LYO", "Gulf of Lyon", "S", False, False, None),
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
    ("Stp", "R", "A", "nc"),
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
for name, full_name, ttype, has_coasts, sc, owner in territories:
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
        }
    }
    if owner:
        entry["fields"]["country_template"] = list(countries.keys()).index(owner) + 1
    data.append(entry)
    territory_pk[name] = pk_counter
    pk_counter += 1

# Add CoastTemplates
for name, full_name, ttype, has_coasts, sc, owner in territories:
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
with open("initial_templates.json", "w") as f:
    json.dump(data, f, indent=2)
