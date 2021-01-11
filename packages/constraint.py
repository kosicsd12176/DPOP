class Constraint(object):

    def __init__(self, name: str, constraint_type: str, agent_meetings=None):
        if agent_meetings is None:
            agent_meetings = []
        self._name = name
        self._constraint_type = constraint_type
        self._agent_meetings = agent_meetings

    @property
    def name(self) -> str:
        return self._name

    @property
    def constraint_type(self) -> str:
        return self._constraint_type

    @property
    def agent_meetings(self) -> list:
        return self._agent_meetings
