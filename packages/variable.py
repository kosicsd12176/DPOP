class Variable:
    def __init__(self, variable_type, utility):
        self.variable = variable_type
        self.utility = utility

    def get_variable_utility(self):
        return  self.variable, self.utility

    def set_variable_utility(self, variable_type, utility):
        self.variable = variable_type
        self.utility = utility





