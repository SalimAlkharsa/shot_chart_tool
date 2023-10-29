import matplotlib as mpl
import matplotlib.pyplot as plt
import json

class ShotChart:
    def __init__(self, df):
        self.df = df
        self.set_colors()

    def set_colors(self):
        # Open the json file called team_colors.json
        with open('team_colors.json', 'r') as f:
            team_colors = json.load(f)
        # Get the team name from the dataframe
        team_name = self.df.iloc[0]['TEAM_NAME']
        # Get the primary color from the team_colors json file
        self.primary_color = team_colors[team_name][0]
        self.secondary_color = team_colors[team_name][1]
        self.tertiary_color = team_colors[team_name][2]
        pass


    def create_court(self, ax):
        # Set background color to secondary color
        ax.set_facecolor = self.secondary_color
        # Set the color of the court markings
        color = self.primary_color

        # Short corner 3PT lines
        ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
        ax.plot([220, 220], [0, 140], linewidth=2, color=color)
        # 3PT Arc
        ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
        # Lane and Key
        ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
        ax.plot([80, 80], [0, 190], linewidth=2, color=color)
        ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
        ax.plot([60, 60], [0, 190], linewidth=2, color=color)
        ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
        ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
        # Rim
        ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
        # Backboard
        ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Set axis limits
        ax.set_xlim(-250, 250)
        ax.set_ylim(0, 470)
        return ax

    def make_shot_chart(self):
        # Make the shot chart
        # Draw basketball court
        mpl.rcParams['font.family'] = 'Avenir'
        mpl.rcParams['font.size'] = 18
        mpl.rcParams['axes.linewidth'] = 2
        fig = plt.figure(figsize=(4, 3.76))
        ax = fig.add_axes([0, 0, 1, 1])
        ax = self.create_court(ax)
        # Draw the shots
        # Separate the shots into made and missed
        made = self.df[self.df.SHOT_MADE_FLAG == 1]
        missed = self.df[self.df.SHOT_MADE_FLAG == 0]
        # Draw the shots, both territiary, misses are x and makes are o
        ax.scatter(missed.LOC_X, missed.LOC_Y+60, c=self.tertiary_color, marker='x', s=25, linewidths=1)
        ax.scatter(made.LOC_X, made.LOC_Y+60, facecolors='none', edgecolors=self.tertiary_color, marker='o', s=25, linewidths=1)
        plt.show()
        return True