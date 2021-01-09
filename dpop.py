from experiment.packages.variable import Variable
from experiment.packages.meeting import Meeting

meetings = []
meeting_one = Meeting(1,50)
meeting,utility = meeting_one.get_meeting_utility()
print(meeting_one.get_meeting_utility())

meetings.append(meeting_one.get_meeting_utility())
print(meetings)

