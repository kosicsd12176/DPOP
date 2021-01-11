class Agent(object):

    def __init__(self, name: str, agent_meetings=None, preferences_utilities=None):
        if agent_meetings is None:
            agent_meetings = {}

        if preferences_utilities is None:
            preferences_utilities = {}
        self._name = name
        self._agent_meetings = agent_meetings
        self._preferences_utilities = preferences_utilities

    @property
    def name(self) -> str:
        return self._name

    @property
    def agent_meetings(self) -> dict:
        return self._agent_meetings

    @property
    def preferences_utilities(self) -> dict:
        return self._preferences_utilities

    def __str__(self):
        return "Agent({})".format(self.name)

    def __repr__(self):
        return "Agent({}, {}, {})".format(self.name, self.agent_meetings, self.preferences_utilities)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            return self.name == other.name

    def add_agent_meeting(self, agent_meetings: dict):
        for key in agent_meetings.keys():
            self._agent_meetings[key] = agent_meetings.get(key)

    def add_preference_utility(self, utilities: dict):
        for key in utilities.keys():
            self._preferences_utilities[key] = utilities.get(key)

    def clone(self):
        return Agent(self.name, self.agent_meetings, self.preferences_utilities)
