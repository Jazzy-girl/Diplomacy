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
    ("Lon", "London", "L", True, True, "E"),
    ("Yor", "Yorkshire", "L", True, False, None),
    ("Wal", "Wales", "L", True, False, None),
    ("Lvp", "Liverpool", "L", True, True, "E"),
    ("Edi", "Edinburgh", "L", True, True, "E"),
    ("Cly", "Clyde", "L", True, False, None),
    ("Nwy", "Norway", "L", True, True, None),
    ("Swe", "Sweden", "L", True, True, None),
    ("StP", "St. Petersburg", "L", True, True, "R"),
    ("Mos", "Moscow", "L", False, True, "R"),
    ("Sev", "Sevastopol", "L", True, True, "R"),
    ("War", "Warsaw", "L", False, True, "R"),
    ("Fin", "Finland", "L", True, False, None),
    ("Den", "Denmark", "L", True, True, None),
    ("Ber", "Berlin", "L", True, True, "G"),
    ("Kie", "Kiel", "L", True, True, "G"),
    ("Mun", "Munich", "L", False, True, "G"),
    ("Hol", "Holland", "L", True, True, None),
    ("Bel", "Belgium", "L", True, True, None),
    ("Par", "Paris", "L", False, True, "F"),
    ("Mar", "Marseilles", "L", True, True, "F"),
    ("Gas", "Gascony", "L", True, False, None),
    ("Bre", "Brest", "L", True, True, "F"),
    ("Spa", "Spain", "L", True, True, None),
    ("Por", "Portugal", "L", True, True, None),
    ("Rom", "Rome", "L", True, True, "I"),
    ("Ven", "Venice", "L", True, True, "I"),
    ("Nap", "Naples", "L", True, True, "I"),
    ("Pie", "Piedmont", "L", True, False, None),
    ("Tus", "Tuscany", "L", True, False, None),
    ("Tri", "Trieste", "L", True, True, "A"),
    ("Bud", "Budapest", "L", False, True, "A"),
    ("Vie", "Vienna", "L", False, True, "A"),
    ("Ser", "Serbia", "L", False, True, None),
    ("Alb", "Albania", "L", True, False, None),
    ("Gre", "Greece", "L", True, True, None),
    ("Bul", "Bulgaria", "L", True, True, "T"),
    ("Rum", "Rumania", "L", True, True, None),
    ("Con", "Constantinople", "L", True, True, "T"),
    ("Smy", "Smyrna", "L", True, True, "T"),
    ("Ank", "Ankara", "L", True, True, "T"),
    ("Arm", "Armenia", "L", True, False, None),
    ("Syr", "Syria", "L", True, False, None),
    ("NAf", "North Africa", "L", True, False, None),
    ("Tun", "Tunis", "L", True, True, None),
]

coast_mapping = {
    "Bul": ["ec", "sc"],
    "Spa": ["nc", "sc"],
    "StP": ["nc", "sc"]
}

coast_full_name = {
    "nc": "North",
    "sc": "South",
    "ec": "East"
}

units = [
    ("Lon", "E", "F", None),
    ("Edi", "E", "F", None),
    ("Lvp", "E", "A", None),
    ("Bre", "F", "F", None),
    ("Par", "F", "A", None),
    ("Mar", "F", "A", None),
    ("Ber", "G", "A", None),
    ("Mun", "G", "A", None),
    ("Kie", "G", "F", None),
    ("Vie", "A", "A", None),
    ("Bud", "A", "A", None),
    ("Tri", "A", "F", None),
    ("Ven", "I", "A", None),
    ("Rom", "I", "A", None),
    ("Nap", "I", "F", None),
    ("Mos", "R", "A", None),
    ("Sev", "R", "F", None),
    ("StP", "R", "A", "nc"),
    ("Con", "T", "A", None),
    ("Smy", "T", "A", None),
    ("Ank", "T", "F", None),
]

data = []
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
    entry = {
        "model": "api.initialunitsetup",
        "pk": pk_counter,
        "fields": {
            "territory_template": territory_pk[terr],
            "country_template": list(countries.keys()).index(country) + 1,
            "unit_type": utype,
            "coast_template": coast_pk[f"{terr}/{coast}"] if coast else None
        }
    }
    data.append(entry)
    pk_counter += 1

# Save JSON
with open("initial.json", "w") as f:
    json.dump(data, f, indent=2)
