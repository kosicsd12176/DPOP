class Node:
    def __init__(self, agent):
        self.agent = agent
        self.root = False

    def set_parent_node(self, node):
        self.parent = node

    def set_children_node(self, node):
        self.children = node

    def set_pseudoparent_node(self, node):
        self.pseudoparent = node

    def set_pseudochildren_node(self, node):
        self.pseudochildren = node

    def set_root(self, value):
        self.root = value


    def get_parent_node(self):
        return self.parent, self.agent

    def get_children_node(self):
        return self.children, self.agent

    def get_pseudoparent_node(self):
        return self.pseudoparent, self.agent

    def get_pseudochildren_node(self):
        return  self.pseudochildren, self.agent

    def get_root(self):
        return self.root