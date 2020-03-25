"""
Map the string representation of different entities to known resources
such as DBpedia
"""

import os
import json
import sys

import numpy as np
import pandas as pd

DATA_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

