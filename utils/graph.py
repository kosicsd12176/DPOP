import pygraphviz as pgv

from packages.node import Node
from utils import constants


def _find_neighbors_relations(node, relations, nodes):
    node_neighbors = []
    node_relations = []
    for r in relations:
        if node.name in r.variables:
            node_relations.append(r)
            meetings = list(r.variables)
            meetings.remove(node.name)
            for n in nodes:
                if n.name in meetings and n not in node_neighbors:
                    node_neighbors.append(n)
    node_neighbors.sort(key=lambda neighbour: neighbour.name)
    return node_neighbors, node_relations


def generate_dfs_tree(variables, relations, agents, root=None):
    # build a node for each of the variables eg a1_m1, a1_m2 etc
    nodes = []
    for key, value in variables.items():
        n = Node(value, agents.get(value.agent))
        nodes.append(n)
    for n in nodes:
        neighbors, rels = _find_neighbors_relations(n, relations, nodes)
        n._neighbors = neighbors
        n.relations = rels

    # Root selection with heuristic : choose the Node with the highest number
    #  of neighbors
    if root is None:
        # heuristic :
        nodes.sort(key=lambda nd: nd.neighbors_count())
        root = nodes[-1]
    else:
        for n in nodes:
            if n.variable == root:
                root = n
                break

    token = []
    root.handle_token(None, token)
    return root


def _visit_tree(root):
    """
    Iterator: visit a tree, yielding each node in DFS order.

    :param root: the root node of the tree.
    """
    yield root
    for c in root.children:
        # Using 'yield from would be nicer, but is only available with python
        #  >= 3.3
        for n in _visit_tree(c):
            yield n


def get_nodes(root: Node):
    nodes = []
    for n in _visit_tree(root):
        nodes.append(n)
    nodes.reverse()
    return nodes

def get_nodes_reverse(root: Node):
        nodes = []
        for n in _visit_tree(root):
            nodes.append(n)
        return nodes

def draw_constraint_graph(meetings: dict, constraints: dict, filename: str):
    G = pgv.AGraph(remincross=True)
    G.add_nodes_from(meetings.keys())
    for constraint in constraints:
        if constraint.constraint_type == constants.EQUALITY_CONSTRAINT:
            G.add_edge(constraint.variables[0], constraint.variables[1], color='green', dir="none")
        else:
            G.add_edge(constraint.variables[0], constraint.variables[1], color='red', dir="none")
        G.draw(filename, prog='dot', format='svg')


def draw_pstree(root: Node, meetings: dict, filename: str):
    G = pgv.AGraph(remincross=True)
    G.add_nodes_from(meetings.keys())
    draw_pstree_edges(G, root)
    G.draw(filename, prog='dot', format='svg')


def draw_pstree_edges(g: pgv.AGraph, parent_node: Node):
    for pseudo_child in parent_node.pseudo_children:
        g.add_edge(parent_node.name, pseudo_child.name, constraint='false', style='dashed')
    for child in parent_node.children:
        g.add_edge(parent_node.name, child.name)
        draw_pstree_edges(g, child)
