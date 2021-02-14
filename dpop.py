import sys
import time
import threading

from packages.agent_thread import AgentThread
from packages.variable import Variable
from packages.agent import Agent
from packages.node import Node
from generators.generator import problem_generator
from utils.constraint_builder import constraint_builder
from utils.fileparser import load_dcop_from_file
from utils.graph import generate_dfs_tree, draw_pstree, get_nodes, get_nodes_dict
from utils.util_message import util_messages, value_messages

start = time.perf_counter()


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
    print("NUMBER OF THE CONSTRAINS: {}".format(len(constraints)))
    root = generate_dfs_tree(variables, constraints, dcop["agents"])
    agents = dcop["agents"]
    threads = []
    nodes_dict = get_nodes_dict(root)
    cycles = []
    for name, agent in agents.items():
        t = AgentThread(agent, nodes_dict, cycles)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    # util_messages(root, agents)
    value_messages(root)
    draw_pstree(root, variables, "simulations/pseudotree_{}.svg".format(dcop["agents_number"]))
