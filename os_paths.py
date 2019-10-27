"""File to hold os specific path variables"""

import os
import sys

# Project root
ROOT = os.path.abspath(__file__)
sys.path.append(ROOT)

# Card Logic Folder
CARD_LOGIC_FOLDER = os.path.join(ROOT, "card_logic")

