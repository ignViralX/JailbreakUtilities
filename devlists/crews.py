"""

MIT License

Copyright (c) 2023 ignViral

This file contains dynamic lists for the name of every crew in the game.
The static list for crews is in crews_static.txt, good for fallback when API is down. 
These lists only include crews that have participated in a Crew Battle this in-game season.

"""

from datetime import date
import json
import os
import requests

# Dynamic

# On the first run, the storage folder won't exist, so the program will make it
if not os.path.exists("storage/"):
    os.mkdir("storage")


def generate_dynamic_crew_list():
    """Generates and returns a dynamic list of all crew names th is season"""
    path = f"storage/crews_{str(date.today())}.json"

    # Downloads a new dataset daily to account for updates; uses today's if it already exists.
    if not os.path.exists(path):
        data = requests.get("""
            https://badimo.nyc3.digitaloceanspaces.com/crew_leaderboard/snapshot/top/50/season/3/latest.json
            """, timeout=10).text

        with open(path, mode="w", encoding="UTF-8") as file:
            file.write(str(data))

    with open(path, 'r', encoding="UTF-8") as f:
        unloaded_data = f.read()
        f.close()

    loaded_data = json.loads(unloaded_data)

    # Generates the list of crew names
    crew_list = []
    for obj in loaded_data:
        crew_list.append(obj["ClanName"])

    return crew_list
