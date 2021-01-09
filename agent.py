from experiment.packages.meeting import Meeting
from experiment.packages.variable import Variable


class Agent:
    def __init__(self):
        self.meetings = []
        self.variables = []

    def set_meeting(self, Meeting):
        self.meetings.pop(Meeting.get_meeting_utility())

    def set_variable(self, Variable):
        self.variables.pop(Variable.get_variable_utility())






