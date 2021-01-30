import sys

from packages.variable import Variable
from packages.agent import Agent
from packages.node import Node
import pandas as pd
import numpy as np
from generators.generator import problem_generator
from utils.constraint_builder import constraint_builder
from utils.fileparser import load_dcop_from_file
from utils.graph import generate_dfs_tree, draw_pstree, get_nodes, draw_constraint_graph
from utils.util_message import util_messages, value_messages


def dcop_process(args):
    try:
        agents_number = int(args.agents_number)
    except ValueError:
        print("Provide Number!")
        sys.exit()

    filepath = problem_generator(agents_number)
    dcop = load_dcop_from_file(filepath)
    variables = dcop["variables"]
    constraints = constraint_builder(dcop["agents_number"], dcop["meetings_number"], variables)
    root = generate_dfs_tree(variables, constraints, dcop["agents"])
    util_messages(root)
    value_messages(root)
    draw_pstree(root, variables, "simulations/pseudotree_{}.svg".format(dcop["agents_number"]))
    draw_constraint_graph(variables, constraints, "simulations/constraint_graph_{}.svg".format(dcop["agents_number"]))




