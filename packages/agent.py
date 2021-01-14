class Agent(object):

    def __init__(self, name: str, variables=None, preferences_utilities=None):
        if variables is None:
            variables = {}

        if preferences_utilities is None:
            preferences_utilities = {}
        self._name = name
        self._variables = variables
        self._preferences_utilities = preferences_utilities

    @property
    def name(self) -> str:
        return self._name

    @property
    def variables(self) -> dict:
        return self._variables

    @property
    def preferences_utilities(self) -> dict:
        return self._preferences_utilities

    def __str__(self):
        return "Agent({})".format(self.name)

    def __repr__(self):
        return "Agent({}, {}, {})".format(self.name, self.variables, self.preferences_utilities)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            return self.name == other.name

    def add_variable(self, variables: dict):
        for key in variables.keys():
            self._variables[key] = variables.get(key)

    def add_preference_utility(self, utilities: dict):
        for key in utilities.keys():
            self._preferences_utilities[key] = utilities.get(key)

    def clone(self):
        return Agent(self.name, self.variables, self.preferences_utilities)
