import csv
import json
import pickle

def load_midfielders():
    midfielder_list = {}

    # Opening the file
    with open('source/Player.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Creating empty list for midfielders' IDs
        midfielder_ids = [6, 7, 8, 9]

        # Reading rows from the file

        for row in csvreader:
            # If player is a midfielder, add him to ID list
            if (csvreader.line_num - 1) % 11 in midfielder_ids:
                midfielder_list[row['player_api_id']] = row['player_name']
    return midfielder_list

def find_top_scorers(midfielders):
    player_goals = {}  # Dictionary for each player's goals

    # Open matches file
    with open('source/Match.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        next(reader)
        # Go through each row
        for row in reader:
            try:
                # Take info of goals
                goal_data = row['goal']

                # Convert a line into list of dictionaries
                goals_list = json.loads(goal_data)

                # Transform each dict to list
                for goal in goals_list:
                    # Check, if there is 'player1' key and if it is a digit
                    if 'player1' in goal and isinstance(goal['player1'], str) and goal['player1'].isdigit():
                        player_id = goal['player1']
                        # Check if ID matches
                        if player_id in midfielders:
                            # Refresh goals for current player
                            if player_id in player_goals:
                                player_goals[player_id] += 1
                            else:
                                player_goals[player_id] = 1
                            
                        else:
                            continue

            except ValueError:
                continue

    # Find max goals
    max_goal = max(player_goals.values())
    top_scorers = []

    for id, player_goal in player_goals.items():
        if player_goal == max_goal:
            top_scorers.append(midfielders[id])

    return top_scorers

midfielders = load_midfielders()
top_midfielders_scorers = find_top_scorers(midfielders)

# Save in pkl format
with open('pkl_compacted/top_scorers.pkl', 'wb') as file:
    pickle.dump(top_midfielders_scorers, file)

