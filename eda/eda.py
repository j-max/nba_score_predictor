from nba_api.stats.endpoints import  leaguegamefinder, teamdetails, commonteamyears
import pandas as pd
import json
from nba_api.stats.endpoints import leaguestandingsv3, commonplayerinfo, CommonAllPlayers, commonallplayers
from nba_api.stats.static.players import get_active_players
import sys
sys.path.append("../src")

from data_collection import get_regular_season_games

# What is the correlation between ppg and age in the last full NBA Season (2019-2020)?

# This request, on January 23, 2021, returns 519 players
players = get_active_players()

# Example of a player response: Steven Adams
response = commonplayerinfo.CommonPlayerInfo(players[0]['id']).get_json() 
headers = json.loads(response)['resultSets'][0]['headers']
df = pd.DataFrame(json.loads(response)['resultSets'][0]['rowSet'])
df.columns = headers

# Gather all of the team ids
team_ids = commonteamyears.CommonTeamYears().get_dict()
team_ids = team_ids['resultSets'][0]['rowSet']

# Convert to dictionary with team abbreviations
team_ids = {team_id[-1]: team_id[1] for team_id in team_ids if team_id[-1] != None} 


# The query results in 4598 players in the dataset
all_players = commonallplayers.CommonAllPlayers().get_dict()
all_players = all_players['resultSets'][0]['rowSet']

# The query results in 536 players in the 2019-2020 season
players_2020 = commonallplayers.CommonAllPlayers(is_only_current_season=1 ).get_dict()
players_2020 = players_2020['resultSets'][0]['rowSet']

df_players_2020 = commonallplayers.CommonAllPlayers(is_only_current_season=1 ).get_data_frames()[0]
chi_2020 = df_players_2020[df_players_2020['TEAM_ABBREVIATION']=='CHI']
