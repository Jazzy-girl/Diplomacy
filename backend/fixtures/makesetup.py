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
    ("Bud", "Budapest", "L", True, False, "A"),
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
    ("Mos", "Moscow", "L", True, False, "R"),
    ("Mun", "Munich", "L", True, False, "G"),
    ("Nap", "Naples", "L", True, True, "I"),
    ("Nor", "Norway", "L", True, True, None),
    ("Par", "Paris", "L", True, False, "F"),
    ("Por", "Portugal", "L", True, True, None),
    ("Rom", "Rome", "L", True, True, "I"),
    ("Rum", "Rumania", "L", True, True, None),
    ("Ser", "Serbia", "L", True, False, None),
    ("Sev", "Sevastopol", "L", True, True, "R"),
    ("Smy", "Smyrna", "L", True, True, "T"),
    ("Spa", "Spain", "L", True, True, None),
    ("Swe", "Sweden", "L", True, True, None),
    ("Stp", "St. Petersburg", "L", True, True, "R"),
    ("Tri", "Trieste", "L", True, True, "A"),
    ("Tun", "Tunis", "L", True, True, None),
    ("Ven", "Venice", "L", True, True, "I"),
    ("Vie", "Vienna", "L", True, False, "A"),
    ("War", "Warsaw", "L", True, False, "R"),

    # Other Land Territories (22)
    ("Alb", "Albania", "L", False, True, None),
    ("Apu", "Apulia", "L", False, True, None),
    ("Arm", "Armenia", "L", False, True, None),
    ("Boh", "Bohemia", "L", False, False, None),
    ("Bur", "Burgundy", "L", False, False, None),
    ("Cly", "Clyde", "L", False, True, None),
    ("Fin", "Finland", "L", False, True, None),
    ("Gal", "Galicia", "L", False, False, None),
    ("Gas", "Gascony", "L", False, True, None),
    ("Lvn", "Livonia", "L", False, True, None),
    ("NAf", "North Africa", "L", False, True, None),
    ("Pic", "Picardy", "L", False, True, None),
    ("Pie", "Piedmont", "L", False, True, None),
    ("Pru", "Prussia", "L", False, True, None),
    ("Ruh", "Ruhr", "L", False, False, None),
    ("Sil", "Silesia", "L", False, False, None),
    ("Syr", "Syria", "L", False, True, None),
    ("Tus", "Tuscany", "L", False, True, None),
    ("Tyr", "Tyrolia", "L", False, False, None),
    ("Ukr", "Ukraine", "L", False, False, None),
    ("Wal", "Wales", "L", False, True, None),
    ("Yor", "Yorkshire", "L", False, True, None),

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
    ("War", "R", "A", None),
    ("Stp", "R", "A", "nc"),
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
with open("initial_templates.json", "w") as f:
    json.dump(data, f, indent=2)
