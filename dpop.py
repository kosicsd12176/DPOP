from experiment.packages.variable import Variable
from experiment.packages.meeting import Meeting
from experiment.agent import Agent

#create agent
agent1 = Agent()

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
print(agent1.get_meeting_and_utilities())
print(agent1.get_variable_and_utilities())

#for i in agent1.get_variable():

