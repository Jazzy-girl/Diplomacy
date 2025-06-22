import json

names = [
    'England',
    'France',
    'Germany',
    'Russia',
    'Turkey',
    'Italy',
    'Austria'
]

countries = list()
pk = 1
for name in names:
    countries.append({
        'model': 'api.country',
        'pk': pk,
        'fields':{
            'name' : name[0],
            'full_name' : name
        }
    })
    pk+=1

with open ('countries.json', 'w') as f:
    json.dump(countries, f)
    print("exported!")