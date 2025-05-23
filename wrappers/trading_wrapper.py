"""

MIT License

Copyright (c) 2025 ignViral

This is a standalone wrapper for the Jailbreak Trading API.
This file can be copy and pasted directly into a new location and it will function fine.

"""

from datetime import date
import json
import os
import requests

# On the first run, the storage folder won't exist, so the program will make it
if not os.path.exists("storage/"):
    os.mkdir("storage")

# Downloads a new dataset daily to account for updates; uses today's if it already exists.
path = f"storage/trading_{str(date.today())}.json"
if not os.path.exists(path):
    data = requests.get(
        "https://badimo.nyc3.digitaloceanspaces.com/trade/frequency/snapshot/month/latest.json"
        ,timeout=10).text.replace("'", '"')
    with open(path, mode="w", encoding="UTF-8") as file:
        file.write(str(data))

with open(path, 'r', encoding="UTF-8") as f:
    unloaded_data = f.read()
    f.close()

loaded_data = json.loads(unloaded_data)

# Generates a list of every item in the game (can be used as a Choice menu in discord bots)
item_list = []

for obj in loaded_data:
    item_list.append(obj["Name"])


# Functions to search for items in the list and gather data; import and use these in your programs!
def search(item: str) -> str | bytes | bytearray:
    """Gather statistics of a trading item using its name"""
    for trading_object in loaded_data:
        if trading_object["Name"] == item:
            return trading_object
    return 404


def generate_trading_data(item: str) -> str:
    """Gather statistics of a trading item using its name and organize
    them neatly into a message to send"""
    search_result = search(item)
    print(search_result)
    item_type = str(search_result["Type"])

    name = str(search_result["Name"])
    wiki_name = name.replace(" ", "_")
    times_traded = str(search_result["TimesTraded"])
    unique_circulation = str(search_result["UniqueCirculation"])
    demand_multiple = str(search_result["DemandMultiple"])

    message = f"""
        **Item Type** » {item_type}
        **Item Name** » {name}
        **Item Wiki** » https://jailbreak.fandom.com/wiki/{wiki_name}\n
        **TIMES TRADED (Last 30d)** » {times_traded} copies -> Times Traded (TT) is the amount of times this item has 
        been traded in the last month. Useful in collection for other metrics & calculating demand/rarity. (see 
        below)\n
        **UNIQUE TT (Last 30d)** » {unique_circulation} copies -> Unique TT is the amount of unique (
        different copies) of this item that have changed inventories at least once this month. Be warned, 
        this currently counts dupes as the same item, so it is not 100% accurate!\n
        **DEMAND MULTIPLE** » {demand_multiple} -> Demand Multiple is the average of how many times any given copy of
        this item that was traded this month changed inventories. Calculated using the forumla Times Traded divided by
        Unique Circulation.\n
        **RARITY** » {int(unique_circulation) / 1000} -> Rarity is a 1-100 scale of predicted rarity 
        of the item based off of the number of unique copies traded at least once this month (Unique TT). The higher 
        the rarity, the more common. The lower, the rarer.\n"""

    return message
