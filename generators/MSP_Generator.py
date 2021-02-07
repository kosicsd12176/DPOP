from anytree import NodeMixin, LevelOrderIter, PreOrderIter
from anytree.exporter import DotExporter
import random
import sys

TIME_SLOT_UTIL = [[10, 20, 30, 40, 50, 60, 70, 80],
                  [80, 70, 60, 50, 40, 30, 20, 10],
                  [10, 10, 10, 10, 10, 10, 10, 10]]

MEETING_UTIL = ['100', '70', '50', '30', '10']

MAX_MEETINGS = 8

TOTAL_MEETINGS = 0


class Meeting:

    def __init__(self, mid, participants, type):
        self.mid = mid
        self.participants = participants
        self.type = type


class Agent:

    # instance attributes
    def __init__(self):
        self.time_utils = random.choice(TIME_SLOT_UTIL)
        self.meetings = []


class AgentNode(Agent, NodeMixin):

    def __init__(self, name, parent=None, children=None):
        super(AgentNode, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def createGRP(self):
        global TOTAL_MEETINGS

        agentChildren = list(self.children)

        if len(self.meetings) < MAX_MEETINGS:
            if len(agentChildren) > 0:
                for item in agentChildren + [self]:
                    participants = {agent.name: random.choice(MEETING_UTIL) for agent in agentChildren + [self]}
                    meeting = Meeting(TOTAL_MEETINGS + 1, participants, "GRP")
                    item.meetings.append(meeting)

                TOTAL_MEETINGS += 1

            else:
                pass
        else:
            pass

    def createSIB(self):
        global TOTAL_MEETINGS

        agentSiblings = list(self.siblings)

        if len(self.meetings) < MAX_MEETINGS:
            if len(agentSiblings) > 0:
                numberOfParticipants = random.randint(1, len(agentSiblings))

                # Choose a random subset of agent siblings
                agentSiblings = random.sample(agentSiblings, numberOfParticipants)

                for item in agentSiblings + [self]:
                    participants = {agent.name: random.choice(MEETING_UTIL) for agent in agentSiblings + [self]}
                    meeting = Meeting(TOTAL_MEETINGS + 1, participants, "SIB")
                    item.meetings.append(meeting)

                TOTAL_MEETINGS += 1

            else:
                pass
        else:
            pass

    def createPTC(self):
        global TOTAL_MEETINGS

        agentChildren = list(self.children)

        if len(self.meetings) < MAX_MEETINGS:
            if len(agentChildren) > 0:
                numberOfParticipants = random.randint(1, len(agentChildren))

                # Choose a random subset of agent children
                agentChildren = random.sample(agentChildren, numberOfParticipants)

                for item in agentChildren + [self]:
                    participants = {agent.name: random.choice(MEETING_UTIL) for agent in agentChildren + [self]}
                    meeting = Meeting(TOTAL_MEETINGS + 1, participants, "PTC")
                    item.meetings.append(meeting)

                TOTAL_MEETINGS += 1

            else:
                pass
        else:
            pass


class AgentHierarchy:
    def __init__(self, numOfAgents):
        self.numOfAgents = numOfAgents
        self.root = None

    def createHierarchy(self):
        totalAgents = self.numOfAgents

        # totalAgents = 20
        agentNum = 1
        level = 1
        nodeName = "A" + str(agentNum)
        root = AgentNode(nodeName)
        agentNum += 1
        currentParent = root
        availableNodes = []
        availableNodesInner = []

        while agentNum <= totalAgents:

            nodeName = "A" + str(agentNum)

            if len(currentParent.children) < level + 1:
                currentNode = AgentNode(nodeName, parent=currentParent)
                availableNodes.append(currentNode)
                agentNum += 1

            else:

                level += 1
                N = len(availableNodes)

                while (N > 0) & (agentNum <= totalAgents):

                    nodeName = "A" + str(agentNum)
                    currentParent = availableNodes[0]

                    if len(currentParent.children) < level + 1:
                        currentNode = AgentNode(nodeName, parent=currentParent)
                        availableNodesInner.append(currentNode)
                        agentNum += 1

                    else:
                        currentParent = availableNodes.pop(0)
                        N -= 1

                availableNodes = availableNodesInner

        DotExporter(root).to_dotfile("simulations/DCOP_Tree_" + str(self.numOfAgents) + ".dot")

        self.root = root
        return root

    def createMeetingsBFS(self):
        for agent in [node for node in LevelOrderIter(self.root)]:

            meeting_type = random.randint(1, 20)

            if meeting_type < 10:
                agent.createGRP()
            elif meeting_type < 19:
                agent.createPTC()
            elif meeting_type >= 19:
                agent.createSIB()

    def createMeetingsDFS(self):
        for agent in [node for node in PreOrderIter(self.root)]:

            meeting_type = random.randint(1, 20)

            if meeting_type < 10:
                agent.createGRP()
            elif meeting_type < 20:
                agent.createPTC()
            elif meeting_type >= 19:
                agent.createSIB()

    def printGeneratorOutputDetail(self):

        numOfVariables = 0

        for agent in [node for node in LevelOrderIter(self.root)]:
            numOfVariables += len(agent.meetings)
        print("NumberOfAgents;TotalMeetings;TotalVariables")
        print(str(self.numOfAgents) + "," + str(TOTAL_MEETINGS) + ',' + str(numOfVariables))

        print("AgentNumber;MeetingID;Utility")
        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.meetings:
                print(agent.name.replace('A', '') + "," + str(item.mid) + "," + item.participants[agent.name])

        print("AgentNumber;TimeSlot;TimeSlotUtility")
        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.time_utils:
                print(agent.name.replace('A', '') + "," + str(agent.time_utils.index(item) + 1) + "," + str(item))

    def printGeneratorOutput(self):

        numOfVariables = 0

        for agent in [node for node in LevelOrderIter(self.root)]:
            numOfVariables += len(agent.meetings)

        print(str(self.numOfAgents) + "," + str(TOTAL_MEETINGS) + ',' + str(numOfVariables))

        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.meetings:
                print(agent.name.replace('A', '') + "," + str(item.mid) + "," + item.participants[agent.name])

        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.time_utils:
                print(agent.name.replace('A', '') + "," + str(agent.time_utils.index(item) + 1) + "," + str(item))

    def printStatistics(self):

        numOfVariables = 0

        for agent in [node for node in LevelOrderIter(self.root)]:
            numOfVariables += len(agent.meetings)

        print("Number of Agents: " + str(self.numOfAgents))
        print("Number of Meetings: " + str(TOTAL_MEETINGS))
        print("Number of Variables: " + str(numOfVariables))

        print("-----------------------------")

        cntGRP = 0
        cntPTC = 0
        cntSIB = 0

        meetingList = []
        for agent in [node for node in LevelOrderIter(self.root)]:

            for item in agent.meetings:
                if item.mid not in meetingList:
                    meetingList.append(item.mid)
                    if item.type == 'GRP':
                        cntGRP += 1
                    elif item.type == 'PTC':
                        cntPTC += 1
                    elif item.type == 'SIB':
                        cntSIB += 1

        print("GRP: " + str(cntGRP))
        print("PTC: " + str(cntPTC))
        print("SIB: " + str(cntSIB))

    def export_to_file(self):

        with open("simulations/MSP_Problem_" + str(self.numOfAgents) + ".txt", "w") as f:

            numOfVariables = 0

            for agent in [node for node in LevelOrderIter(self.root)]:
                numOfVariables += len(agent.meetings)

            f.write(str(self.numOfAgents) + "," + str(TOTAL_MEETINGS) + ',' + str(numOfVariables) + '\n')

            for agent in [node for node in LevelOrderIter(self.root)]:

                for item in agent.meetings:
                    f.write(
                        agent.name.replace('A', '') + "," + str(item.mid) + "," + item.participants[agent.name] + '\n')

            for agent in [node for node in LevelOrderIter(self.root)]:

                for item in agent.time_utils:
                    f.write(agent.name.replace('A', '') + "," + str(agent.time_utils.index(item) + 1) + "," + str(
                        item) + '\n')

            return f.name


def problem_generator(agents_number):
    H = AgentHierarchy(agents_number)
    H.createHierarchy()
    H.createMeetingsBFS()
    H.createMeetingsDFS()
    filepath = H.export_to_file()
    H.printStatistics()
    return filepath
