"""File to house classes for card logic files to inherit off of"""

import os
import importlib.machinery
import yugidb.yugi_db as db

from abc import ABC
from os_paths import CARD_LOGIC_FOLDER

# The functions to load
LOAD_FUNCTIONS = [
    "summon"
]

class CardLogic(metaclass=ABC):
    """
    Class to manage card logic. Register to this class in order to get
    various classes
    """

    def summon(self):
        pass


    def get_logic(self, uid):
        """
        Tries to load the card logic class module and get the class
        through subclasses.
        TODO: Classes must be directly inherited. Need to add more to recurse check.
        """

        subclass_name = "C_{}.py".format(str(uid))
        # Try to load the file into memory first and then return the value.
        loader = importlib.machinery.SourceFileLoader(
            CARD_LOGIC_FOLDER,
            subclass_name
        )

        loader.load_module()
        # Get the sub class value that we want
        for cls in CardLogic.__subclasses__:
            if cls.__name__ == subclass_name:
                return cls.summon
        
        return None

class Card:
    """
    Represents a card class. 
    Goes through each class defined in card_logic and loads them as needed in order to
    get card value.
    """

    # Public values
    uid = None
    name = None
    stats = None

    # Define the number of cards available for this particular value
    count = 1

    def __init__(self, name_or_id):
        """Receives a card id or name to load card logic and meta-data."""
        try:
            # Have id, try to get name
            self.uid = int(name_or_id)
            self.name = db.find_card_with_id(self.uid)["name"]
        except ValueError:
            # Have name instead, get the id
            self.name = name_or_id
            self.uid = db.find_card(self.name)["id"]
        
        # Get the stats of the cards from db and store into object
        # Can be lazy evaluation or stored into one giant lookup for
        # better commpression.
        self.stats = db.get_card_stat(self.uid)
        self.

    def _load_logic(self):
        """Loads the particular card logic from card_logic folder."""
        # Use the id to load the database logic
        
