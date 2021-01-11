from packages.agent import Agent
from packages.agentmeeting import AgentMeeting
from utils import constants


def load_dcop_from_file(filename):
    agents_number = 0
    meetings_number = 0
    agent_meetings_number = 0
    line_counter = 0
    agent_meetings = {}
    agents = {}
    file = open(filename, encoding="utf-8")
    for line in file:
        if line_counter == 0:
            fields = line.split(constants.DCOP_FILE_DELIMITER)
            agents_number = int(fields[0])
            meetings_number = int(fields[1])
            agent_meetings_number = int(fields[2])
        elif line_counter <= agent_meetings_number:
            agent, meeting, utility = line.split(constants.DCOP_FILE_DELIMITER)
            agent_meeting = AgentMeeting(agent, meeting, utility)
            agent_meeting_dist = {agent_meeting.name: agent_meeting}
            agent_meetings["a{}_m{}".format(agent, meeting)] = agent_meeting
            if agent in agents.keys():
                agents.get(agent).add_agent_meeting(agent_meeting_dist)
            else:
                agents[agent] = Agent(agent, agent_meeting_dist)
        else:
            agent, timeslot, utility = line.split(constants.DCOP_FILE_DELIMITER)
            if agent in agents.keys():
                agents.get(agent).add_preference_utility({timeslot: utility})

        line_counter += 1

    return {"agents_number": agents_number, "meetings_number": meetings_number,
            "agent_meetings_number": agent_meetings_number, "agent_meetings": agent_meetings, "agents": agents}
