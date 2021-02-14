from pandas import DataFrame

from packages.agent import Agent
from packages.variable import Variable


class Node(object):

    def __init__(self, variable: Variable, agent: Agent):
        self._variable = variable
        self._neighbors = []
        self.relations = []
        self.parent = None
        self.pseudo_parents = []
        self.pseudo_children = []
        self.children = []
        self._visited = []
        self._utilities = []
        for utility in agent.preferences_utilities.items():
            self._utilities.append(variable.utility * utility[1])
        self.root = False
        self._util_messages = {}
        self._util_message_sent = False
        self._value_message_sent = False

    @property
    def name(self) -> str:
        return self._variable.name

    @property
    def variables(self) -> list:
        return [self._variable]

    @property
    def variable(self) -> Variable:
        return self._variable

    @property
    def set_variable(self, value):
         self._variable = value

    @property
    def utilities(self) -> list:
        return self._utilities

    @property
    def util_messages(self) -> dict:
        return self._util_messages

    @property
    def util_message_sent(self) -> bool:
        return self._util_message_sent

    @property
    def value_message_sent(self) -> bool:
        return self._value_message_sent

    def set_util_message(self, node_name: str, message: DataFrame):
        self._util_messages[node_name] = message

    def set_util_message_sent(self, value: bool):
        self._util_message_sent = value

    def set_value_message_sent(self, value: bool):
        self._value_message_sent = value

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
