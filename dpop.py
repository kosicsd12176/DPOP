import sys

from packages.variable import Variable
from packages.agent import Agent
from packages.node import Node
from generators.generator import problem_generator
from utils.constraint_builder import constraint_builder
from utils.fileparser import load_dcop_from_file
from utils.graph import generate_dfs_tree, draw_pstree


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
    root = generate_dfs_tree(variables, constraints)
    draw_pstree(root, variables, "simulations/pseudotree_{}.svg".format(dcop["agents_number"]))


def test():
    # create agent
    agent1 = Agent("a1")
    agent2 = Agent("a2")
    agent3 = Agent("a3")

    # set agent's first meeting with utility
    # meeting = Meeting(1, 50)
    # agent1.set_meeting(meeting)
    meeting = Variable("1", "1", 50)
    agent1.add_variable({meeting.name: meeting})

    # set agent's second meeting with utility
    meeting = Variable("1", "2", 50)
    agent1.add_variable({meeting.name: meeting})

    # set agent's variable with utility
    agent1.add_preference_utility({1: 1})
    agent1.add_preference_utility({2: 2})
    agent1.add_preference_utility({3: 3})
    agent1.add_preference_utility({4: 4})
    agent1.add_preference_utility({5: 0})
    agent1.add_preference_utility({6: 5})
    agent1.add_preference_utility({7: 10})
    agent1.add_preference_utility({8: 20})

    node1 = Node(Variable("1", "1", 50))
    node2 = Node(agent2)
    node3 = Node(agent3)

    node1.set_parent_node(node2)
    node2.set_children_node(node1)
    node2.set_parent_node(node3)
    node3.set_children_node(agent2)
