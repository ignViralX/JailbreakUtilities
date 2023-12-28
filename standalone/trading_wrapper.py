"""

MIT License

Copyright (c) 2023 ignViral

This is a standalone wrapper for the Jailbreak Trading API.
This file can be copy and pasted directly into a new location and it will function fine.
If you plan on using the entire Jailbreak Utilities toolset, just import trading from the module.

TODO: Minor code quality improvements

"""

import json, os, requests
from datetime import date

# On the first run, the storage folder won't exist, so the program will make it
if not os.path.exists("storage/"):
    os.mkdir("storage")

# Downloads a new dataset daily to account for updates; uses today's if it already exists.
path = f"storage/trading_{str(date.today())}.json"
if not os.path.exists(path):
    data = requests.get(
        "https://badimo.nyc3.digitaloceanspaces.com/trade/frequency/snapshot/month/latest.json").text.replace("'", '"')
    with open(path, mode="w") as file:
        file.write(str(data))

file = open(path)
loaded_file = json.load(file)

# Generates a list of every item in the game (can be used as a Choice menu in discord bots)
item_list = []

for obj in loaded_file:
    item_list.append(obj["name"])


# Functions to search for items in the list and gather data; import and use these in your applications!
def search(item: str) -> str | bytes | bytearray:
    """Gather statistics of a trading item using its name"""
    for trading_object in loaded_file:
        if trading_object["name"] == item:
            return trading_object


def generate_trading_data(item: str) -> str:
    """Gather statistics of a trading item using its name and organize them neatly into a message to send"""
    search_result = search(item)
    item_type = str(search_result["type"])

    name = str(search_result["name"])
    wiki_name = name.replace(" ", "_")
    times_traded = str(search_result["TimesTraded"])
    unique_circulation = str(search_result["UniqueCirculation"])
    demand_multiple = str(search_result["demand_multiple"])

    message = f"""
        **ITEM type** » {item_type}
        **ITEM name** » {name}
        **ITEM WIKI** » https://jailbreak.fandom.com/wiki/{wiki_name}\n
        **TIMES TRADED (Last 30d)** » {times_traded} copies
        -> Times Traded (TT) is the amount of times this item has been traded in the last month. Useful in collection for other metrics & calculating demand/rarity. (see below)\n
        **UNIQUE TT (Last 30d)** » {unique_circulation} copies
        -> Unique TT is the amount of unique (different copies) of this item that have changed inventories at least once this month. Be warned, this currently counts dupes as the same item, so it is not 100% accurate!\n
        **DEMAND MULTIPLE** » {demand_multiple}
        -> Demand Multiple is the average of how many times any given copy of this item that was traded this month changed inventories. Calculated using the forumla Times Traded divided by Unique Circulation.\n
        **RARITY** » {int(unique_circulation) / 1000}
        -> Rarity is a 1-100 scale of predicted rarity of the item based off of the number of unique copies traded at least once this month (Unique TT). The higher the rarity, the more common. The lower, the rarer.\n
        """

    return message
