"""

MIT License

Copyright (c) 2023 ignViral

This file contains static and dynamic lists for the name of every trading item in the game.

"""

from datetime import date
import json
import os
import requests

# Static (good fallback for if the API is down or if you are being rate limited for some reason)

staticItemList = ['Model3', 'La Matador', 'Volt', 'EscapeBot', 'Eternal Flame', 'Pickup', 'Radiant Red', 'Eclaire',
                  'Deja', 'Native', 'Roadster', 'Speed', 'Money', 'BlackHawk', 'Deep Purple', 'Flower', 'Drone',
                  'LittleBird', 'Cybertruck', 'Ray', 'Dirtbike', 'FalconS', 'Stallion', 'Fiasco', 'HyperOrange Lvl1',
                  'Challenger', 'Meteor Magnet', 'Shell Mark-5', 'Radiant Green', 'Interrogator', 'Electrostatic',
                  'DuneBuggy', 'Spike', 'Longhorn', 'Successor', 'Harpoon', 'Laviolette', 'Taxi', 'Aperture', 'Concept',
                  'Ray 9', 'Volt', 'JetSki', 'HyperPink Lvl1', 'Rainbow', 'HyperYellow Lvl1', 'Landmine', 'BoxOCash',
                  'Gunfire', 'HyperGreen Lvl1', 'Boxer', 'HyperPurple Lvl1', 'HyperDiamond Lvl1', 'HyperRed Lvl1',
                  'Stunt', 'Wingo', 'Desert Crawler', 'Surus', 'Tesla', 'LeEclair', 'Semi Truck', 'Bandana',
                  'Radiant Purple', 'Brulee', 'Cosmic', 'Patrol', 'Jet', 'Police', 'Pixel', 'ATV', 'Snake', 'Power1',
                  'UFO', 'Delorean', 'Black', 'NASCAR 75th', 'Radiant Ice', 'Air Tail', 'Flame Spitter',
                  'FlagsOfEurope', 'Frost', 'Parisian', 'Blue', 'Posh', 'Cow', 'Galaxy Wave', 'ClassicVar2',
                  'Super Lime', 'HyperBlue Lvl1', 'Hot Orange', 'Block Wing', 'BelgianWaffle', 'Tank Wing', 'MoltenM12',
                  'Red', 'Trailblazer', 'Darkest Purple', 'Monster', 'SUV', 'Tow Truck', 'Gold', 'NitroTank', 'Melons',
                  'Radiant Yellow', 'Javelin', 'Classic', 'Sentinel', 'Teddy Bear', 'Trophy Wings', 'Piggy',
                  'Prison Bus', 'Radiant Orange', 'Mystic', 'EXP1', 'Buoy', 'Ambulance', 'White', 'Tiny Toy', 'Badger',
                  'ClassicVar1', 'Aquatic', 'Yellow', 'Shogun', 'Abstracts', 'Megalodon', 'Green', 'Orange', 'Halo',
                  'Poseidon', 'Volleyball', 'Proto-8', 'Mighty', 'King', 'Tokyo', 'Carbon Fire', 'Magic Purple',
                  'Macaron', 'Arachnid', 'Touchdown', 'Cruiser', 'Beignet', 'Slashers', 'ToriiGate', 'Berlin Graffiti',
                  'Ice', 'Flamethrower', 'Paint', 'Steed', 'Ladybug', 'Firetruck', 'DragonBreath', 'Performance',
                  'Racer', 'HyperOrange Lvl2', 'Peach', 'Champion', 'Radioactive', 'Tank', 'Manga', 'Bubble Wand',
                  'Retro Racer', 'Spares', 'Jet', 'Deep Purple Flame', 'Scorch', 'Cyan', 'Trion', 'Camper', 'JB8',
                  'Candy Cane', 'Turbine', 'Lightning', 'Torero', 'Celsior', 'Scope', 'Bloxy', 'Travel Case', 'Gulf',
                  'Drop Weapons', 'ClassicVar3', '3Billion', 'Crown', 'GTR', 'Purple', 'Lightning', 'Racing Wing',
                  'Diamond', 'Tsutek', 'Torpedo', 'Swirl', 'Reactor', 'Vault Door', 'Agent', 'Shell Classic',
                  'Police Chase', 'Two Sided', 'Sawblade', 'RC Antenna', 'Racer', 'Hottest Pink', 'Tracer',
                  'HelloItsVG', 'Terminator', 'Ball', 'Classic', 'Dual Rockets', 'T.Rex Bone', 'Pastel Blue', 'Roll-X',
                  'Goliath', 'Shogun', 'LeaningWingOfPisa', 'Forest Green', 'Rally', 'Pink', 'AerialSupport',
                  'DigitalConfetti', 'Cartoon', 'NoobFreak', 'HyperPurple Lvl2', 'Wooden Toy', 'Construction',
                  'Volt4x4', 'Flaming', 'Bandit', 'Road Warrior', 'Superstar', 'Matte', 'Frit', 'Propeller', 'Billion',
                  'Overdrive', 'Jack Rabbit', 'Rocket', 'Badonuts', 'Volcano', 'Fall Chrome', 'HyperYellow Lvl2',
                  'Spyglass', 'DoYouLift', 'HyperDiamond Lvl2', 'Drip', 'Beachball', 'DragonChaser', 'HyperPink Lvl2',
                  'HyperGreen Lvl2', 'Pixel', 'RFX', 'Hold E', 'UFO', 'Robowing', 'Star Wing', 'Rattler', 'Galaxy',
                  'Orange Pixel', 'Wireframe', 'BatWings', 'White Marble', 'HyperRed Lvl2', 'Boomerang', 'RX-1', 'JDM',
                  'Space-R', 'Bacon', 'Crimson Racer', 'Sendoff', 'TroubleWing', 'Pastel Violet', 'Camo', 'Tiger',
                  'FlatBlack', 'Live Glider', 'Track Toy', 'Unknown Signal', 'Donut', 'Sloop', 'Cyclone', 'Grey',
                  'Galactic Carbon', 'Banana Car', 'Arachnid', 'Cash Spitter', 'ICEBreaker', 'Revolver', 'Snow Log',
                  'Forged', 'Checker', 'Crew Capsule', 'Lava', 'Tesseract', 'Raptor', 'Dragster', 'Energized', 'Zebra',
                  'Blue Pixel', 'Live2020',
                  'Speed', 'Windmill', 'Sand', 'Bull', 'Fire', 'WagonWheel', 'Bull', 'Tumbleweed', 'Line', 'Realistic',
                  'Turning Key', 'Winter Camo', 'Armor', 'Darkest Blue', 'Real Green', 'Spare', '5B Flags',
                  'Triple Fin', 'Trade Sail', 'Water Gun', 'Beam Hybrid', 'Cucaracha', 'Orange Chute', 'Pastel Green',
                  'Deathtrap', 'Blade', 'Wavy', 'Laser Cannon', 'CrashNation', 'Offroad', 'Pastel Yellow',
                  'Rumble Siren', 'CatchMe', 'HyperOrange Lvl3', 'Camo Radar', 'Pastel Orange', 'Lines', '4 Billion',
                  'Circuits', 'Tall Arch', 'Money', 'Winner', 'Hypno', 'Cruiseliner', 'ChampionTrumpets', 'Pastel Gray',
                  'Pastel Brown', 'Field', 'Watermelon', 'MyUsernamesThis', 'Nemesis', 'Countdown', 'Vantablack',
                  'Flamethrower', 'Navy Blue', 'Black Ice', 'City', 'TreadedSport', 'Dual Flags', 'Kanagawa', 'Train',
                  'Nuclear Waste', 'HyperBlue Lvl2', 'DenisDaily', 'ColorsOfItaly', 'Sakura Pink', 'Beadlock',
                  'Deathray', 'Thrusters', 'Distorted', 'Arch', 'VFX', 'Blue Chute', 'UKHeritage', 'KreekCraft',
                  'EuroCloverleaf', 'Snowstorm', 'Pastel Pink', 'NapkinNate', 'Maroon', 'Jetpack', 'Compass', 'Stance',
                  'Bicycle', 'Darkest Red', 'Glowing Yellow', 'HyperPurple Lvl3', 'Parisian', 'Criminal', 'Bonded',
                  'Military Green', 'Tuner', 'Thin', 'ShipWheel', 'Planetary', 'Diamond Engrave', 'Fore',
                  'Patchy Jeans', 'JapaneseLantern', 'Dino', 'Fire Brigade', 'Darkest Marine', 'RedS3', 'Rubber Ducky',
                  'HyperDiamond Lvl3', 'Snowflake', 'Jailbreak', 'Baller', 'Monster', 'Hotdog', 'Japanese',
                  'Desert Camo', 'Surfboard Rack', 'Phindr', 'Dragon Scales', 'Earth', 'BlueS3', 'Mark5',
                  'Shell Speaker', 'Darkest Green', 'HyperYellow Lvl3', 'Bloxy', 'RTX', 'Park Bench', 'Void',
                  'Star Badge', 'Afterburner', 'Darkest Brown', 'HyperOrange Lvl4', 'HyperGreen Lvl3', 'Doubloon',
                  'Sakura', 'Ionize', 'Icicle', 'TreadedThick', 'Red Eyes', 'Tiny Wing', 'Spinner', '5Star',
                  'Spider Leg', 'Tailfin', 'EnduranceWing', 'Mecha Arm', 'PghLFilms', 'Lightning', 'Clown',
                  'Earthquake', 'HyperPink Lvl3', 'Old Town Road', 'Brickset', 'Brickset', '3Billion', 'Velocity',
                  'Airhorn', 'SubCarbon', 'Radar', '2Billion', 'HyperRed Lvl3', 'Soccer', 'HyperDiamond Lvl4',
                  'Unified', 'EightLeg', 'HyperOrange Lvl5', 'ClassicSport', 'HyperPurple Lvl4', 'Vecchio',
                  'HyperDiamond Lvl5', 'Clickbait', 'JBMS', 'Blue Eyes', 'HyperGreen Lvl5', 'HyperRed Lvl4',
                  'Snow Face',
                  'HyperYellow Lvl4', 'HyperRed Lvl5', 'HyperBlue Lvl5', 'Bicycle Rack', 'KraoESP', 'HyperPurple Lvl5',
                  'DatBrian', 'Police', 'Center Lock', 'ClassicThick', 'HyperYellow Lvl5', 'Meep Meep', 'Red50',
                  'HyperGreen Lvl4', 'Steamer', 'Quack', 'Daytona', 'TikiTorch', 'Volt Wing', 'NASCAR 75th', 'Blue50',
                  'Iron Rock', 'Snow Shovel', 'Ahooga', 'Treaded', 'HyperBlue Lvl3', 'HyperBlue Lvl4', 'HyperPink Lvl5',
                  'Glider', 'HyperPink Lvl4', 'Jailbreak Army', 'LeapYear']

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

    # Generates the list
    item_list = []
    for obj in loaded_data:
        item_list.append(obj["Name"])

    return item_list