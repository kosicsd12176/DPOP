from experiment.packages.meeting import Meeting
from experiment.packages.variable import Variable
import numpy


class Agent:
    def __init__(self):
        self.meetings_domains = []
        self.meetings_utilities = []
        self.variables_domains = []
        self.variables_utilities = []
        self.sum_of_utilities = 0



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

    def get_programmed_meeting_utility(self, value):
        utility_of_meeting = self.meetings_utilities[value-1]
        utility_of_variable = self.variables_utilities[numpy.argmax(self.variables_utilities)]
        time_slot = self.variables_domains[numpy.argmax(self.variables_utilities)]
        utility_programmed_meeting_utility = utility_of_meeting * utility_of_variable
        self.sum_of_utilities += utility_programmed_meeting_utility
        return  utility_programmed_meeting_utility, time_slot




