import pygraphviz as pgv

from packages.node import Node


def _find_neighbors_relations(node, relations, nodes):
    node_neighbors = []
    node_relations = []
    for r in relations:
        if node.name in r.agent_meetings:
            node_relations.append(r)
            meetings = list(r.agent_meetings)
            meetings.remove(node.name)
            for n in nodes:
                if n.name in meetings and n not in node_neighbors:
                    node_neighbors.append(n)
    node_neighbors.sort(key=lambda neighbour: neighbour.name)
    return node_neighbors, node_relations


def generate_dfs_tree(agent_meetings, relations, root=None):
    # build a node for each of the agent_meetings eg a1_m1, a1_m2 etc
    nodes = []
    for key, value in agent_meetings.items():
        n = Node(value)
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
            if n.agent_meeting == root:
                root = n
                break

    token = []
    root.handle_token(None, token)

    return root


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