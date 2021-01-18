import numpy

from packages.node import Node
from utils.graph import get_nodes


def generate_util_matrix(node: Node, parent: Node):
    util = numpy.zeros((8, 8))
    for node_index in range(0, 8):
        node_utility = node.utilities[node_index]
        for parent_index in range(0, 8):
            util[node_index][parent_index] = parent.utilities[parent_index] + node_utility

    return util


def util_message_propagation(node: Node):
    util_join_matrix = []
    for relation in node.relations:
        if node.parent.name in relation.variables:
            util_join_matrix.append(generate_util_matrix(node, node.parent))
        else:
            for pseudo_parent in node.pseudo_parents:
                if pseudo_parent.name in relation.variables:
                    util_join_matrix.append(generate_util_matrix(node, pseudo_parent))
    max_utilities = []
    join_util = numpy.zeros((8, 8))
    for matrix in util_join_matrix:
        for node_index in range(0, 8):
            for parent_index in range(0, 8):
                join_util[node_index][parent_index] += matrix[node_index][parent_index]
    for parent_index in range(0, 8):
        max_utilities.append(numpy.argmax(join_util[:, parent_index]) + 1)

    node.parent.set_util_message(node.name, max_utilities)


def util_messages(root: Node):
    for node in get_nodes(root):
        if not node.root:
            util_message_propagation(node)
