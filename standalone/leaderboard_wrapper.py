"""

MIT License

Copyright (c) 2023 ignViral

This is a barebones standalone wrapper for the Jailbreak Crew Leaderboard API.
This file can be copy and pasted directly into a new location and it will function fine.
If you plan on using the entire Jailbreak Utilities toolset, just import leaderboards from the module, don't use this file.

TODO: Implement members & caching system to generateCrewData()
TODO: Format the UTC Latest Battle time to be more readable

"""

import json, os, requests
from datetime import date

# On the first run, the storage folder won't exist, so the program will make it
if not os.path.exists("storage/"):
    os.mkdir("storage")

# Downloads a new dataset daily to account for updates; if todays has already been downloaded, uses it instead of a fresh download.
path = f"storage/leaderboards_{str(date.today())}.json"
if not os.path.exists(path):
    data = (requests.get("https://badimo.nyc3.digitaloceanspaces.com/crew_leaderboard/snapshot/top/50/season/3/latest.json").text)
    with open(path, mode="w") as file:
        file.write(str(data))

file = open(path)
loaded_file = json.load(file)

# Generates a list of every crew in the game (can be used as a Choice menu in discord bots)
crew_list = []

for obj in loaded_file:
    crew_list.append(obj["ClanName"])

# Functions to search for crews statistics or get ordered leaderboards
def search(crewName: str) -> str | bytes | bytearray:
    """Gather raw statistics of a crew using its name"""
    for object in loaded_file:
        if object["ClanName"] == crewName:
            return(object)
    
def generateCrewData(crewName: str) -> str:
    """Gather statistics of a crew using its name and organize them neatly into a message to send"""
    data = search(crewName)

    owner_username = requests.get(f"https://users.roblox.com/v1/users/{str(data['OwnerUserId'])}").json()['name']
    crew_name = str(data["ClanName"])
    battles_played = str(data["BattlesPlayed"])
    battles_won = str(data["BattlesWon"])
    rating = str(data["Rating"])
    last_battle_played = str(data["LastBattlePlayedUTCStr"])

    """
    In this demo, "members" is not displayed, as you would need to convert all of the users IDs
    into usernames that are readable to people using this command, and the roblox API likely has
    a rate limit on how often you can do this. I plan on implementing a caching system to manage
    this in the future, but for now either implement it yourself or just use the other data!

    You can look up the members of a crew in-game but not some of the other statistics, so it isn't
    even that helpful to be able to view them on other applications, just convenient.

    UserID to Username API endpoint: 'https://users.roblox.com/v1/users/{username}'; returns a JSON array with a "name" value
    members = data["MemberUserIds"]
    """

    message = f"""
        **CREW NAME** » {crew_name}
        **OWNER** » {owner_username}
        **RATING** » {rating}\n
        **BATTLES WON (Season)** » {battles_won}/{battles_played} ({(int(battles_won)/int(battles_played))*100}% win rate)
        -> This shows the amount of battles this crwe has won out of the amount they have played, and their win percentage. Data limited to this season.\n
        **LATEST BATTLE (UTC)** » {last_battle_played}
        -> This displays the last time, in UTC, that this crew participated in a battle. Displayed in YYYY-MM-DD_hh:mm:ss format.\n
        """

    return message