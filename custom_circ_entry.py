"""This file is the code to insert a spanning circulation for a given planar graph input (where entry need not be exterior edge)
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import source.trial.bdy as bdy
from typing import List, Tuple
import circulation