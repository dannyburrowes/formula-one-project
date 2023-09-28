import requests

data = requests.get(f"http://ergast.com/api/f1/qualifying.json?limit=10000&offset=9000").json()


data2 = data['MRData']['RaceTable']['Races'][7]

print(data2)

for i in range(6,  8):
    print(i)


print(len(data2))

