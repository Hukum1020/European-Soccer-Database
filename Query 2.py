import csv
from datetime import datetime
import pickle

# Calculating age of a player
def calculate_age(birthday):
    today = datetime.now()
    delta = today - birthday
    return delta.days // 365

# Reading CSV and creating dictionaries 
players = []

with open('source/Player.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['birthday'] = datetime.strptime(row['birthday'], '%d/%m/%Y %H:%M')
        row['age'] = calculate_age(row['birthday'])
        players.append(row)

# Getting top 10 oldest players
oldest_players = sorted(players, key=lambda x: x['birthday'])[:10]

sorted_oldest_players = []
for player in oldest_players:
    sorted_oldest_players.append((player['player_name'], float(player['height'])))

sorted_oldest_players = sorted(sorted_oldest_players, key=lambda x: x[1], reverse=True)

with open('pkl_compacted/sorted_oldest_players.pkl', 'wb') as f:
    pickle.dump(sorted_oldest_players, f)