"""

MIT License

Copyright (c) 2023 ignViral

This file contains a static dictionary that turns item names from the Trading API list
into formatted, more readable names (i.e. HyperOrangeLvl1 -> Hyper Orange Level 1)
If an item does not have a dictionary entry here, that means that it's API name is it's
normal name.

This file is an active work-in-progress and is not finished. New items are added
with every update to the repository.

"""

# Static (there is no dynamic here; this cannot be automatically done)

staticItemNamesDictionary = {
    "Model3":"Model 3", "EscapeBot":"Escape Bot", "BlackHawk":"Black Hawk",
    "LittleBird":"Little Bird"
}
