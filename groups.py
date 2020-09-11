from bs4 import BeautifulSoup
import requests

# Player Class
class Player:
    def __init__(self, name, url_code, season):
        self.name = name
        self.url_code = url_code
        self.season = season

# Team Class
class Team:
    def __init__(self, name, url_code, season):
        self.name = name
        self.url_code = url_code
        self.season = season
        self.players = []
        self.set_players()

    # Prints players on team
    def list_players(self):
        player_list = []
        for player in self.players:
            player_list.append(player.name)
        print(player_list)

    # Gets all players and respective codes from team
    def set_players(self):
        url = "https://fbref.com/en/squads/"+self.url_code+"/"+self.season
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find("table", {"class": "stats_table"})
        player_ids = table.find("tbody").find_all("th", {"data-stat": "player"})
        for player_id in player_ids:
            player_name = player_id.contents[0].text
            player_code = player_id.contents[0]['href'][12:20]
            new_player = Player(player_name, player_code, self.season)
            self.players.append(new_player)

# League Class
class League:
    def __init__(self, name, url_code, season):
        self.name = name
        self.url_code = url_code
        self.season = season
        self.teams = []
        self.set_teams()

    # Gets all teams and respective codes from league
    def set_teams(self):
        print("Loading "+self.name+" teams...")
        url = "https://fbref.com/en/comps/"+str(self.url_code)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find("table", {"class": "stats_table"})
        team_ids = table.find_all("td", {"data-stat": "squad"})
        for team_id in team_ids:
            team_name = team_id.contents[2].text
            team_code = team_id.contents[2]['href'][11:19]
            new_team = Team(team_name, team_code, self.season)
            self.teams.append(new_team)
