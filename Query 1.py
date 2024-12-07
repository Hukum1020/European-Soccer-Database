import csv
import pickle

player_names = {}
player_averages = {}

# Read CSV file to create a mapping of player_api_id to player_name
with open('source/Player.csv', 'r', newline='') as player_names_file:
    csvreader = csv.reader(player_names_file)
    next(csvreader)  # Skip header row
    cnt_gk = 1
    for row in csvreader:
        if cnt_gk % 11 == 1 or cnt_gk == 1:
            player_api_id = row[0]
            player_name = row[1]
            player_names[player_api_id] = player_name
        cnt_gk += 1

# Read CSV file with attributes
with open('source/PlayerAttributes.csv', 'r', newline='') as PlayerAttributes:
    csvreader = csv.reader(PlayerAttributes)
    for row in csvreader:
        try:
            if row[0] in player_names:
                player_api_id = row[0]  # Changed to player_api_id
                # Transforming values to integer to sort non valid values
                last_five_values = []

                for value in row[-5:]:
                    last_five_values.append(int(value))
                
                # Calculating average for last 5 elements of database
                average = sum(last_five_values) / len(last_five_values)

                # Adding players into database
                if player_api_id not in player_averages:
                    player_averages[player_api_id] = []
            
                # Adding player's average score
                player_averages[player_api_id].append(average)

            else:
                continue
            
        except ValueError:
            continue

# Get maximum avg values
selected_players = []
for player_api_id, averages in player_averages.items():
        selected_players.append((player_api_id, max(averages)))

# Sort selected players based on their maximum average scores
sorted_players = sorted(selected_players, key=lambda x: x[1], reverse=True)

# Create a list to store top 10 avg scores
top_10_players = []

# Collect data for top 10 players
for player_api_id, max_average in sorted_players[:10]:
    player_name = player_names.get(player_api_id, "Player_name")
    top_10_players.append({"Player": player_name, "Max Average": max_average})

# Save top 10 player data in pickle format
with open('pkl_compacted/top_10_players.pkl', 'wb') as f:
    pickle.dump(top_10_players, f)