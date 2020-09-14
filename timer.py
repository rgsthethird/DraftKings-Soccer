from groups import Player, Team, League
from datetime import datetime

class Timer:
    def __init__(self, league):
        self.start_time = datetime.now()
        self.league_size = len(league.teams)
        self.teams_completed = 0

    def time_remaining(self):

        if self.teams_completed == 0:
            self.teams_completed += 1
            return "N/A"

        curr_time = datetime.now()
        difference = curr_time-self.start_time

        time_remaining = difference*(self.league_size/self.teams_completed)-difference
        seconds = time_remaining.total_seconds()
        hours = round(seconds // 3600)
        minutes = round((seconds % 3600) // 60)
        seconds = round(seconds % 60)
        time_string = ""
        if(hours > 0):
            time_string = str(hours)+"h"+str(minutes)+"m"+str(seconds)+"s"
        else:
            time_string = str(minutes)+"m"+str(seconds)+"s"

        self.teams_completed += 1
        return time_string
