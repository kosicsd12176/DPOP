from packages.variable import Variable


class Node(object):

    def __init__(self, variable: Variable):
        self._variable = variable
        self._neighbors = []
        self.relations = []
        self.parent = None
        self.pseudo_parents = []
        self.pseudo_children = []
        self.children = []
        self._visited = []
        self.root = False

    @property
    def name(self) -> str:
        return self._variable.name

    @property
    def variables(self) -> list:
        return [self._variable]

    @property
    def variable(self) -> Variable:
        return self._variable

    def handle_token(self, sender, token):
        token = token[:]
        self._visited.append(sender)
        if sender is None:
            self.root = True
            self._propagate(token)

        elif self.parent is None and not self.root:
            self.parent = sender
            self.pseudo_parents = [
                n for n in self._neighbors if n in token and n != sender
            ]
            self._neighbors.sort(
                key=lambda x: x.count_neighbors_in_token(token), reverse=True
            )
            self._propagate(token)

        else:
            if sender in self.children:
                pass
            else:
                self.pseudo_children.append(sender)

    def _propagate(self, token):
        token.append(self)

        # heuristic :
        # sort our neighbors based on the number of their neighbors are
        # already in the token
        self._neighbors.sort(
            key=lambda x: x.count_neighbors_in_token(token), reverse=True
        )

        for n in self._neighbors:
            if n not in self._visited:
                if n not in self.pseudo_parents:
                    self.children.append(n)
                n.handle_token(self, token)

    def count_neighbors_in_token(self, token):
        c = 0
        for n in self._neighbors:
            if n in token:
                c += 1
        return c

    def neighbors_count(self):
        return len(self._neighbors)

    def __repr__(self):
        return "Node " + self.variable.name

    def __str__(self):
        return "Node " + self.variable.name
