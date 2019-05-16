from utils.timeutils import convert_start_and_end_time


class Epoch:
    """object that holds epoch info"""

    def __init__(self, name=None, start_time=None, end_time=None):
        self.name = name
        self.start_time, self.end_time = convert_start_and_end_time(start_time, end_time)