


class Meeting:
    def __init__(self, meeting, utility):
        self.meeting = meeting
        self.utility = utility

    def get_meeting_utility(self):
        return  self.meeting, self.utility

    def set_meeting_utility(self, meeting, utility):
        self.meeting = meeting
        self.utility = utility
