import sys

from packages.agent import Agent
from packages.variable import Variable
from utils import constants


def line_parser(line, line_counter):
    agent, var, utility = line.rstrip("\n").split(constants.DCOP_FILE_DELIMITER)
    try:
        utility = int(utility)
    except ValueError:
        print("Error in input text format at line {}!".format(line_counter))
        sys.exit()
    return {"agent": agent, "var": var, "utility": utility}


def load_dcop_from_file(filename):
    agents_number = 0
    meetings_number = 0
    variables_number = 0
    line_counter = 0
    variables = {}
    agents = {}
    file = open(filename, encoding="utf-8")
    for line in file:
        if line_counter == 0:
            fields = line.split(constants.DCOP_FILE_DELIMITER)
            agents_number = int(fields[0])
            meetings_number = int(fields[1])
            variables_number = int(fields[2])
        elif line_counter <= variables_number:
            line_values = line_parser(line, line_counter)
            agent = line_values["agent"]
            meeting = line_values["var"]
            utility = line_values["utility"]
            agent_meeting = Variable(agent, meeting, utility)
            agent_meeting_dist = {agent_meeting.name: agent_meeting}
            variables["a{}_m{}".format(agent, meeting)] = agent_meeting
            if agent in agents.keys():
                agents.get(agent).add_variable(agent_meeting_dist)
            else:
                agents[agent] = Agent(agent, agent_meeting_dist)
        else:
            line_values = line_parser(line, line_counter)
            agent = line_values["agent"]
            timeslot = line_values["var"]
            utility = line_values["utility"]
            if agent in agents.keys():
                agents.get(agent).add_preference_utility({timeslot: utility})
            else:
                agents[agent] = Agent(agent, preferences_utilities={timeslot: utility})

        line_counter += 1

    return {"agents_number": agents_number, "meetings_number": meetings_number,
            "variables_number": variables_number, "variables": variables, "agents": agents}
