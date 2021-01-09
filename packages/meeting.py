


class Meeting:
    def __init__(self, meeting_type, utility):
        self.meeting = meeting_type
        self.utility = utility

    def get_meeting_utility(self):
        return  self.meeting, self.utility

