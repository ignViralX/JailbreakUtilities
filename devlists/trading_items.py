"""

MIT License

Copyright (c) 2023 ignViral

This file contains static and dynamic lists for the name of every trading item in the game.

"""

from datetime import date
import json
import os
import requests

# Dynamic

# On the first run, the storage folder won't exist, so the program will make it
if not os.path.exists("storage/"):
    os.mkdir("storage")


def generate_dynamic_trading_list():
    """Generates and returns a dynamic list of all tradable or untradable items"""
    path = f"storage/trading_{str(date.today())}.json"

    # Downloads a new dataset daily to account for updates; uses today's if it already exists.
    if not os.path.exists(path):
        data = requests.get(
            "https://badimo.nyc3.digitaloceanspaces.com/trade/frequency/snapshot/month/latest.json"
            , timeout=10).text.replace("'", '"')

        with open(path, mode="w", encoding="UTF-8") as file:
            file.write(str(data))

    with open(path, 'r', encoding="UTF-8") as f:
        unloaded_data = f.read()
        f.close()

    loaded_data = json.loads(unloaded_data)

    # Generates the list of item names
    item_list = []
    for obj in loaded_data:
        item_list.append(obj["Name"])

    return item_list
