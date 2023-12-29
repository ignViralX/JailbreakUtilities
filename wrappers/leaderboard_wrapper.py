"""

MIT License

Copyright (c) 2023 ignViral

This is a bare bones standalone wrapper for the Jailbreak Crew Leaderboard API.
This file can be copy and pasted directly into a new location and it will function fine.

TODO: Implement members & caching system to generateCrewData()

"""

from datetime import date
from typing import Any
import json
import os
import requests

# On the first run, the storage folder won't exist, so the program will make it
if not os.path.exists("storage/"):
    os.mkdir("storage")

# Downloads a new dataset daily to account for updates or uses todays dataset if it already exists
path = f"storage/leaderboards_{str(date.today())}.json"
if not os.path.exists(path):
    data = requests.get(
        "https://badimo.nyc3.digitaloceanspaces.com/crew_leaderboard/snapshot/top/50/season/3/latest.json"
        ,timeout=10).text
    
    with open(path, mode="w", encoding="UTF-8") as file:
        file.write(str(data))

with open(path, 'r', encoding="UTF-8") as f:
    data = f.read()
    f.close()

loaded_data = json.loads(data)

# Generates a list of every crew in the game (can be used as a Choice menu in discord bots)
crew_list = []

for obj in loaded_data:
    crew_list.append(obj["ClanName"])


# Functions to search for crews statistics or get ordered leaderboards
def search(crew_name: str) -> str | bytes | bytearray:
    """Gather raw statistics of a crew using its name"""
    for loaded_object in loaded_data:
        if loaded_object["ClanName"] == crew_name:
            return loaded_object
    return 404


def generate_crew_data(crew_name: str) -> str:
    """Gather statistics of a crew using its name and organize them neatly into a message."""
    json_data = search(crew_name)

    owner_username = requests.get(f"""https://users.roblox.com/v1/users/
                                  {str(json_data['OwnerUserId'])}""",timeout=10).json()['name']
    crew_name = str(json_data["ClanName"])
    battles_played = str(json_data["BattlesPlayed"])
    battles_won = str(json_data["BattlesWon"])
    rating = str(json_data["Rating"])
    last_battle_played = str(json_data["LastBattlePlayedUTCStr"]).replace("_", " at ")

    win_rate = int(battles_won) / int(battles_played) * 100
    message = f"""
        **CREW NAME** » {crew_name}
        **OWNER** » {owner_username}
        **RATING** » {rating}\n
        **BATTLES WON (Season)** » {battles_won}/{battles_played} ({win_rate}% WR)
        win rate) 
        -> This shows the amount of battles this crew has won out of the amount they have played, 
        and their win percentage. Data limited to this season.\n
        **LATEST BATTLE (UTC)** » {last_battle_played}
        -> This displays the last time, in UTC, that this crew participated in a battle.
        Displayed in YYYY-MM-DD_hh:mm:ss format.\n"""

    return message


# Optional choice list to give the user when they are selecting their type of order
choices = ['Rating', 'BattlesPlayed', 'BattlesWon']


def fetch_latest_leaderboards(order_by: str = 'BattlesWon') -> tuple[list[Any], str | Any]:
    """Orders top 10 crews based on either Rating, WinPercentage, BattlesPlayed, or BattlesWon.
    Returns the Top 10 crews JSON arrays and then a nicely formatted leaderboard message."""

    # Sort the list of dictionaries in descending order based on 'value'
    sorted_data = sorted(loaded_data, key=lambda x: x[order_by], reverse=True)

    # Get the top 10 players
    top_10 = sorted_data[:10]

    # Display the leaderboard
    message = """"""
    for i, crew in enumerate(top_10, start=1):
        message = message + f"#{i}: {crew['ClanName']} ({crew[order_by]} {order_by})\n"

    return top_10, message

