from experiment.packages.meeting import Meeting
from experiment.packages.variable import Variable


class Agent:
    def __init__(self):
        self.meetings_domains = []
        self.meetings_utilities = []
        self.variables_domains = []
        self.variables_utilities = []


    def set_meeting(self, Meeting):
        domain, utility = Meeting.get_meeting_utility()
        self.meetings_domains.append(domain)
        self.meetings_utilities.append(utility)

    def set_variable(self, Variable):
        domain, utility = Variable.get_variable_utility()
        self.variables_domains.append(domain)
        self.variables_utilities.append(utility)

    def get_meeting_and_utilities(self):
        return self.meetings_domains, self.meetings_utilities

    def get_variable_and_utilities(self):
        return self.variables_domains, self.variables_utilities




