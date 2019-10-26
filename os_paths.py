"""File to hold os specific path variables"""

import os
import sys

# Project root
ROOT = sys.path.append(os.path.abspath(__file__))

# Card Logic Folder
CARD_LOGIC_FOLDER = os.path.join(ROOT, "card_logic")

