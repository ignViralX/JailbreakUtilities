"""

MIT License

Copyright (c) 2023 ignViral

This is a barebones standalone wrapper for the Jailbreak Crew Leaderboard API.
This file can be copy and pasted directly into a new location and it will function fine.
If you plan on using the entire Jailbreak Utilities toolset, just import leaderboards from the module, don't use this file.

TODO: Implement members & caching system to generateCrewData()
TODO: Minor code quality improvements

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
    last_battle_played = str(data["LastBattlePlayedUTCStr"]).replace("_", " at ")

    """
    In this demo, "members" is not displayed, as you would need to convert all of the users IDs
    into usernames that are readable to people using this command, and the roblox API likely has
    a rate limit on how often you can do this. It is definitely possible if you implement a caching
    system

    You can look up the members of a crew in-game but not some of the other statistics, so it isn't
    even that helpful to be able to view them on other applications, just convenient. I've put some
    useful segments of code below if you do wish to implement this system.

    UserID to Username API endpoint: 'https://users.roblox.com/v1/users/{username}'; returns a JSON array with a "name" value in it
    Add another file to storage/ like names.json where you can store IDs to Names and reference it before calling API to get a name from an ID
    Iterate through the 'MemberUserIds' value of the crew you are looking at for all of the member's IDs, check cache & then call API if the name isnt there
    Append to the message by adding a line at the bottom **MEMBERS** » {','.join(member_usernames)} where member_usernames is your list of all the names
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

# Optional choice list to give the user when they are selecting their type of order
choices = ['Rating', 'BattlesPlayed', 'BattlesWon']
def fetchLatestLeaderboards(orderBy: str = 'BattlesWon') -> str | bytes | bytearray:
    """Orders top 10 crews based on either Rating, WinPercentage, BattlesPlayed, or BattlesWon; defaults to BattlesWon. Returns two values, the first is the JSON arrays for the top 10 crews which you can use in your development, and the second is a nicely formatted leaderboards message that can be used to send to players."""
   
    # Sort the list of dictionaries in descending order based on 'value'
    sorted_data = sorted(loaded_file, key=lambda x: x[orderBy], reverse=True)

    # Get the top 10 players
    top_10 = sorted_data[:10]

    # Display the leaderboard
    message = """"""
    for i, crew in enumerate(top_10, start=1):
        message = message + (f"#{i}: {crew['ClanName']} ({crew[orderBy]} {orderBy})\n")

    return top_10, message