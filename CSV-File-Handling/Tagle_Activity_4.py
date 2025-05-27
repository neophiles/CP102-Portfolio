# TAGLE, MARC NEIL V.

import csv

cities_per_state = {}
population_per_state = {}
high_city_per_state = {}
low_city_per_state = {}

file_path = r'C:\Users\Marc Neil\OneDrive\Documents\Programming\PYTHON\CP102\Activity 4\census.csv'

with open(file_path, 'r') as csv_file:
    dict_reader = csv.DictReader(csv_file)
    for row in dict_reader:
        if row['STNAME'] == row['CTYNAME']:
            population_per_state[row['STNAME']] = int(row['POPESTIMATE2010'])
            continue
        if row['STNAME'] not in cities_per_state.keys():
            cities_per_state[row['STNAME']] = 1
            high_city_per_state[row['STNAME']] = [row['CTYNAME'], int(row['POPESTIMATE2010'])]
            low_city_per_state[row['STNAME']] = [row['CTYNAME'], int(row['POPESTIMATE2010'])]
        else:
            cities_per_state[row['STNAME']] += 1
            if high_city_per_state[row['STNAME']][1] < int(row['POPESTIMATE2010']):
                high_city_per_state[row['STNAME']] = [row['CTYNAME'], int(row['POPESTIMATE2010'])]
            if low_city_per_state[row['STNAME']][1] > int(row['POPESTIMATE2010']):
                low_city_per_state[row['STNAME']] = [row['CTYNAME'], int(row['POPESTIMATE2010'])]

with open('US2010Census.csv', 'w', newline='') as csv_file:
    field_names = ['State', 'Total Cities', 'Total 2010 Population']
    dict_writer = csv.DictWriter(csv_file, fieldnames=field_names)
    dict_writer.writeheader()
    for (key, value1), value2 in zip(cities_per_state.items(), population_per_state.values()):
        dict_writer.writerow({'State': key, 'Total Cities': value1, 'Total 2010 Population': value2})

# TOTAL CITIES PER STATE
print("STATE - NUMBER OF CITIES")
for key, value in cities_per_state.items():
    print(f"{key} - {value}")
    
# STATE WITH HIGHEST NUMBER OF CITIES
high_cities = max(cities_per_state.values())
high_state = list(key for key in cities_per_state.keys() if cities_per_state[key] == high_cities)

print("\nSTATE WITH HIGHEST NUMBER OF CITIES")
print(f"{high_state[0]}")
print(f"Total Cities: {high_cities}")

# STATE WITH LOWEST NUMBER OF CITIES
low_cities = min(cities_per_state.values())
low_state = list(key for key in cities_per_state.keys() if cities_per_state[key] == low_cities)

print("\nSTATE WITH LOWEST NUMBER OF CITIES")
print(f"{low_state[0]}")
print(f"Total Cities: {low_cities}")

# TOTAL 2010 CENSUS POPULATION PER STATE
print("\nTOTAL 2010 CENSUS POPULATION PER STATE")
for key, value in population_per_state.items():
    print(f"{key} - {value}")

# CITY PER STATE WITH THE HIGHEST 2010 CENSUS
print("\nCITY PER STATE WITH HIGHEST 2010 POPULATION")
for key, value in high_city_per_state.items():
    print(f"{key} ({value[0]}) - {value[1]}")

# CITY PER STATE WITH THE LOWEST 2010 CENSUS
print("\nCITY PER STATE WITH LOWEST 2010 POPULATION")
for key, value in low_city_per_state.items():
    print(f"{key} ({value[0]}) - {value[1]}")