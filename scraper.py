from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, url_code, season, player_name):
        self.url_code = url_code
        self.season = season
        self.player_name = player_name
        self.valid_comps = ["Premier League", "Championship", "Serie A", "La Liga", "Bundesliga", "Ligue 1", "Coupe de France", "Copa del Rey", "DFB-Pokal", "Coppa Italia", "FA Cup", "Europa Lg", "Champions Lg"]

    # Creates soup using player's url code, the season, and the specific page
    def make_soup(self, page):
        url = "https://fbref.com/en/players/"+self.url_code+"/matchlogs/"+self.season+"/"+page+"/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    # Prepares scraper for summary scrape
    def summary_scrape(self):
        soup = self.make_soup("summary")
        excluded_stats = ["round","result","game_started","match_report"]

        # Unique to summary_scrape, gets players name, height, weight
        match_header = [self.player_name]
        height = ""
        weight = ""
        try:
            height = soup.find("span", {"itemprop": "height"}).text[:-2]
        except:
            pass
        try:
            weight = soup.find("span", {"itemprop": "weight"}).text[:-2]
        except:
            pass
        match_header.append(height)
        match_header.append(weight)

        return self.scrape(match_header, soup, excluded_stats)

    # Each of these gets soup using specific page and sends to scraper, excluding unwanted stats
    def passing_scrape(self):
        soup = self.make_soup("passing")
        excluded_stats = ["date","dayofweek","comp","round","venue","result","squad","opponent","game_started","position","minutes","passes_completed","passes","passes_pct","passes_progressive_distance","assists","xa","match_report"]
        match_header = []
        return self.scrape(match_header, soup, excluded_stats)

    def pass_types_scrape(self):
        soup = self.make_soup("passing_types")
        excluded_stats = ["date","dayofweek","comp","round","venue","result","squad","opponent","game_started","position","minutes","passes","passes_completed","match_report"]
        match_header = []
        return self.scrape(match_header, soup, excluded_stats)

    def gca_scrape(self):
        soup = self.make_soup("gca")
        excluded_stats = ["date","dayofweek","comp","round","venue","result","squad","opponent","game_started","position","minutes","sca","gca","match_report"]
        match_header = []
        return self.scrape(match_header, soup, excluded_stats)

    def defense_scrape(self):
        soup = self.make_soup("defense")
        excluded_stats = ["date","dayofweek","comp","round","venue","result","squad","opponent","game_started","position","minutes","tackles","pressures","blocks","interceptions","tackles_interceptions","match_report"]
        match_header = []
        return self.scrape(match_header, soup, excluded_stats)

    def possession_scrape(self):
        soup = self.make_soup("possession")
        excluded_stats = ["date","dayofweek","comp","round","venue","result","squad","opponent","game_started","position","minutes","touches","dribbles_completed","dribbles","nutmegs","carries","carry_progressive_distance","match_report"]
        match_header = []
        return self.scrape(match_header, soup, excluded_stats)

    def misc_scrape(self):
        soup = self.make_soup("misc")
        excluded_stats = ["date","dayofweek","comp","round","venue","result","squad","opponent","game_started","position","minutes","cards_red","cards_yellow","cards_yellow_red","crosses","interceptions","tackles_won","match_report"]
        match_header = []
        return self.scrape(match_header, soup, excluded_stats)

    # Actual scraper
    def scrape(self, match_header, soup, excluded_stats):
        matches = []
        # Locates data table
        data_tables = soup.find("table", {"class": "stats_table"}).find("tbody").find_all("tr", {"class": ""})
        for data_table in data_tables:
            # If this row is for valid competition and not for goalkeeper...
            if data_table.find("td", {"data-stat": "comp"}).find("a").text in self.valid_comps and data_table.find("td", {"data-stat": "position"}).text != "GK":
                match = []
                # If it's the summary (first) array, add header
                if len(match_header) > 0:
                    for head_datum in match_header:
                        match.append(head_datum)
                data = data_table.contents
                for datum in data:
                    # If stat is wanted, add it to the match array
                    if datum.get("data-stat") not in excluded_stats:
                        text = datum.text
                        stat = datum.get("data-stat")
                        # Specifically to remove country codes from teams in European competitions
                        if len(match_header) > 0 and (stat == "squad" or stat == "opponent") and text[0].islower():
                            space_position = text.find(" ")
                            match.append(text[space_position+1:])
                        else:
                            match.append(text)

                matches.append(match)
        return matches
