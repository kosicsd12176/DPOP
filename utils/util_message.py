from itertools import product
from multiprocessing import Process, current_process
import numpy as np
import pandas as pd
from packages.node import Node
from utils.graph import get_nodes, get_nodes_reverse


def generate_util_matrix(node: Node, parent: Node):
    util = np.zeros((8, 8))
    for node_index in range(0, 8):
        node_utility = node.utilities[node_index]
        for parent_index in range(0, 8):
            util[node_index][parent_index] = parent.utilities[parent_index] + node_utility

    return util

counter_cycles = []

def util_message_propagation(node: Node):
    util_join_matrix = {}
    for relation in node.relations:
        if node.parent.name in relation.variables:
            util_join_matrix[node.parent.name] = np.add.outer(node.parent.utilities, node.utilities)
        else:
            for pseudo_parent in node.pseudo_parents:
                counter_cycles.append(pseudo_parent)
                if pseudo_parent.name in relation.variables:
                    util_join_matrix[pseudo_parent.name] = np.add.outer(pseudo_parent.utilities, node.utilities)

    join_utilities = generate_join_utils(util_join_matrix, node)

    node.parent.set_util_message(node.name, join_utilities)
    return counter_cycles



def util_messages(root: Node):
    counter_cycles = []
    for node in get_nodes(root):
        if not node.root:
            cycles = util_message_propagation(node)
            counter_cycles.append(cycles)

    print("NUMBER OF CYCLES: {}".format(len(counter_cycles)))



async def generate_join_utils(util_join_matrix: dict, node: Node):
    keys = list(util_join_matrix.keys())
    keys.append('utility')
    counter = 0
    N = len(util_join_matrix)
    tuples = [ele for ele in product(range(1, 9), repeat=N)]
    join_utilities = pd.DataFrame(data=np.zeros((len(tuples), N + 1), dtype=np.int32), columns=keys)
    for tp in tuples:
        combined_utilities = np.zeros(8, dtype=np.int32)
        for key in range(0, len(keys) - 1):
            node_name = keys[key]
            node_utilities = util_join_matrix[node_name][:, tp[key] - 1]
            combined_utilities += node_utilities
            join_utilities.at[counter, node_name] = tp[key]

            # include util message from children
            for k, util_message in node.util_messages.items():
                if hasattr(util_message, node_name):
                    parent_utilities = util_message.loc[(util_message[node_name] == tp[key])]
                    filtered_utilities = []
                    for i in range(1, 9):
                        filtered_utilities.append(max(parent_utilities.loc[parent_utilities[node.name] == i]['utility']))
                    combined_utilities += filtered_utilities
                else:
                    filtered_utilities = []
                    for i in range(1, 9):
                        filtered_utilities.append(
                            max(util_message.loc[util_message[node.name] == i]['utility']))
                    combined_utilities += filtered_utilities

        join_utilities.at[counter, 'utility'] = max(combined_utilities)
        counter += 1

    return join_utilities



def value_messages(root: Node):
    sum_utilities = 0
    counter_messages = []
    for node in get_nodes_reverse(root):
            sum, counter = value_message_propagation(node)
            sum_utilities += sum
            counter_messages.append(counter)
    print("SUM TOTAL UTILITIES: {}".format(sum_utilities))


counter_constraints = []
counter = []
counter_nodes = 0
def value_message_propagation(node: Node):

    sum = 0
    if node.root:
        node.variable.set_assigment(np.argmax(node.utilities))
        sum  += max(node.utilities)
        print("{} assigment: {} with utilities: {}".format(node.name, node.variable._assigment, node.utilities))

    counter.append(node)
    for relation in node.relations:
        counter_constraints.append(relation)
        if relation.constraint_type == 'equality':
            for child in node.children:
                if child.variable.assigment == -1:
                    if child.name in relation.variables:
                        child.variable.set_assigment(node.variable.assigment)
                        sum += node.utilities[node.variable.assigment]
                        print("{}'s assigment after equality with {}: {}".format(child.name, node.name, child.variable.assigment))

            for pseudo_child in node.pseudo_children:
                if pseudo_child.variable.assigment == -1:
                    if pseudo_child.name in relation.variables:
                        pseudo_child.variable.set_assigment(node.variable.assigment)
                        print("{}'s assigment after equality with pseudoparent {}: {}".format(pseudo_child.name,node.name,pseudo_child.variable.assigment))

        if relation.constraint_type == 'difference':
            for child in node.children:
                if child.variable.assigment == -1:
                    if child.name in relation.variables:
                        for iterator in counter:
                            if child.variable.agent == iterator.variable.agent:
                                child.utilities[iterator.variable.assigment] = -1
                        child.utilities[node.variable.assigment] = -1
                        child.variable.set_assigment(np.argmax(child.utilities))
                        sum += max(child.utilities)
                        print("{}'s assigment after difference with {}: {} with utilities: {}".format(child.name, node.name, child.variable.assigment, child.utilities))


    return sum, counter_constraints





