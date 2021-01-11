from experiment.packages.meeting import Meeting
from experiment.packages.variable import Variable
import numpy


class Agent:
    def __init__(self):
        self.meetings_domains = []
        self.meetings_utilities = []
        self.preferences_domains = []
        self.preferences_utilities = []




    def set_meeting(self, Meeting):
        domain, utility = Meeting.get_meeting_utility()
        self.meetings_domains.append(domain)
        self.meetings_utilities.append(utility)


    def set_preference(self, Variable):
        domain, utility = Variable.get_variable_utility()
        self.preferences_domains.append(domain)
        self.preferences_utilities.append(utility)

    def get_meeting_and_utilities(self):
        return self.meetings_domains, self.meetings_utilities

    def get_variable_and_utilities(self):
        return self.preferences_domains, self.preferences_utilities





