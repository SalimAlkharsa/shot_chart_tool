# Maintainence functions
from nba_api.stats.static import players
from nba_api.stats.static import teams
import json
import matplotlib.pyplot as plt
import numpy as np


# Save a set of the player names locally
def save_player_names():
    # Save the player names locally and their IDs
    # Get the player list
    player_list = players.get_players()
    player_names = [player['full_name'] for player in player_list]
    player_ids = [player['id'] for player in player_list]
    # Save the player names and IDs into a single json file player:ID
    player_names_ids = dict(zip(player_names, player_ids))
    with open('player_names.json', 'w') as f:
        json.dump(player_names_ids, f)

# Save a set of the team names locally
def save_team_names():
    # Save the team names and their respective IDs into a json file
    # Get the team list
    team_list = teams.get_teams()
    team_names = [team['full_name'] for team in team_list]
    team_ids = [team['id'] for team in team_list]
    # Save the team names and IDs into a single json file team:ID
    team_names_ids = dict(zip(team_names, team_ids))
    with open('team_names.json', 'w') as f:
        json.dump(team_names_ids, f)

# Test the team colors
def show_team_colors():
    # Open the team colors json file
    with open('team_colors.json', 'r') as f:
        team_colors = json.load(f)
    
    fig, ax = plt.subplots(6, 5, figsize=(12, 12))

    for i, (team, colors) in enumerate(team_colors.items()):
        row, col = divmod(i, 5)
        
        # Convert color strings to RGB tuples
        color_rgb = [tuple(int(c[j:j + 2], 16) / 255 for j in (1, 3, 5)) for c in colors]
        
        # Create an array with color data (stacked vertically)
        color_array = np.vstack(color_rgb)
        
        # Display the color swatch
        ax[row, col].imshow([color_array])
        ax[row, col].axis('off')
        ax[row, col].set_title(team, fontsize=8)

    plt.subplots_adjust(wspace=0.3, hspace=0.5)

    # Set a common title for the entire grid
    plt.suptitle("NBA Team Colors", fontsize=16)
    plt.show()

# Run the functions
#save_player_names()
#save_team_names()
show_team_colors()