class Variable(object):

    def __init__(self, agent: str, meeting: str, utility: int):
        self._name = "a{}_m{}".format(agent, meeting)
        self._agent = agent
        self._meeting = meeting
        self._utility = utility

    @property
    def name(self) -> str:
        return self._name

    @property
    def agent(self) -> str:
        return self._agent

    @property
    def meeting(self) -> str:
        return self._meeting

    @property
    def utility(self) -> int:
        return self._utility

    def __str__(self):
        return "Meeting({})".format(self.name)

    def __repr__(self):
        return "Meeting({}, {}, {}, {})".format(self.name, self.agent, self.meeting, self.utility)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            return self.name == other.name

    def clone(self):
        return Variable(self.agent, self.meeting, self.utility)
