class Constraint(object):

    def __init__(self, name: str, constraint_type: str, variables=None):
        if variables is None:
            variables = []
        self._name = name
        self._constraint_type = constraint_type
        self._variables = variables

    @property
    def name(self) -> str:
        return self._name

    @property
    def constraint_type(self) -> str:
        return self._constraint_type

    @property
    def variables(self) -> list:
        return self._variables
