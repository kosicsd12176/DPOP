from itertools import product

import numpy as np
import pandas as pd
from packages.node import Node
from utils.graph import get_nodes


def generate_util_matrix(node: Node, parent: Node):
    util = np.zeros((8, 8))
    for node_index in range(0, 8):
        node_utility = node.utilities[node_index]
        for parent_index in range(0, 8):
            util[node_index][parent_index] = parent.utilities[parent_index] + node_utility

    return util


def util_message_propagation(node: Node):
    util_join_matrix = {}
    for relation in node.relations:
        if node.parent.name in relation.variables:
            util_join_matrix[node.parent.name] = np.add.outer(node.parent.utilities, node.utilities)
        else:
            for pseudo_parent in node.pseudo_parents:
                if pseudo_parent.name in relation.variables:
                    util_join_matrix[pseudo_parent.name] = np.add.outer(pseudo_parent.utilities, node.utilities)

    join_utilities = generate_join_utils(util_join_matrix, node)

    node.parent.set_util_message(node.name, join_utilities)


def util_messages(root: Node):
    for node in get_nodes(root):
        if not node.root:
            util_message_propagation(node)


def generate_join_utils(util_join_matrix: dict, node: Node):
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
            if node_name in node.util_messages.keys():
                util_message = node.util_messages[node_name]
                filtered_utilities = util_message.loc[(util_message[node_name] == tp[key])
                                                      & (util_message[node.name].isin(list(range(1, 8))))]
                combined_utilities += filtered_utilities['utility']

        join_utilities.at[counter, 'utility'] = max(combined_utilities)
        counter += 1

    return join_utilities