# stating template for now, we will code the contents during the MCell4 Python API Tutorial session

import os
import sys

MCELL_PATH = os.environ.get('MCELL_PATH', '')
sys.path.append(os.path.join(MCELL_PATH, 'lib'))

import mcell as m

print("Import of MCell was sucessful")