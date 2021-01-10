from experiment.packages.variable import Variable
from experiment.packages.meeting import Meeting
from experiment.agent import Agent
from experiment.node import Node


#create agent
agent1 = Agent()
agent2 = Agent()
agent3 = Agent()

#set agent's first meeting with utility
meeting = Meeting(1,50)
agent1.set_meeting(meeting)

#set agent's second meeting with utility
meeting.set_meeting_utility(2,50)
agent1.set_meeting(meeting)

#set agent's variable with utility
variable = Variable(1,1)
agent1.set_variable(variable)

variable.set_variable_utility(2,2)
agent1.set_variable(variable)

variable.set_variable_utility(3,3)
agent1.set_variable(variable)

variable.set_variable_utility(4,4)
agent1.set_variable(variable)

variable.set_variable_utility(5,0)
agent1.set_variable(variable)

variable.set_variable_utility(6,5)
agent1.set_variable(variable)

variable.set_variable_utility(7,10)
agent1.set_variable(variable)

variable.set_variable_utility(8,20)
agent1.set_variable(variable)

node1 = Node(agent1)
node2 = Node(agent2)
node3 = Node(agent3)

node1.set_parent_node(node2)
node2.set_children_node(node1)
node2.set_parent_node(node3)
node3.set_children_node(agent2)



print(agent1.get_programmed_meeting_utility(1))
