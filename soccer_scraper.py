from groups import Player, Team, League
from scraper import Scraper
from calculator import Calculator
from timer import Timer

# openpyxl setup
try:
	from openpyxl import Workbook
	from openpyxl import load_workbook
	xlInstalled = True
except ImportError:
	print("Please install openpyxl if you want Excel output!")
	xlInstalled = False

# League URL codes
leagues = {"EPL": 9, "EPL2": 10, "SERIEA": 11, "LALIGA": 12, "LIGUE1": 13, "BUNDESLIGA": 20}

# User input
print()
league = input("Choose [EPL], [EPL2], [SERIEA], [LALIGA], [LIGUE1], or [BUNDESLIGA]: ")
season = input("Choose season ('2019-2020', for example): ")

# If invalid input...
while league not in leagues.keys():
    print("Invalid league. Try again.")
    league = input("Choose [EPL], [EPL2], [SERIEA], [LALIGA], [LIGUE1], or [BUNDESLIGA]: ")

# Excel file setup
if xlInstalled:
    excelFile = input("Excel file for output: ")
    if not excelFile.endswith(".xlsx") or not excelFile.endswith(".xls"):
        excelFile += ".xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Raw Data"
    ws2 = wb.create_sheet("Averages",1)
    titles = ["Player","Height (cm)","Weight (kg)","Date","Day of Week","Competition","Venue","Team","Opponent","Position","Minutes","Goals","Assists","PKs","PK Attempts","Shots","Shots on Target","Yellows","Reds","Touches","Pressures","Tackles","Interceptions","Blocks","xG","Non-Pen xG","xA","Shot-Creating Actions","Goal-Creating Actions","Passes Completed","Passes Attempted","Pass Completion %","Prog. Pass Distance","Carries","Prog. Carry Distance","Dribbles Successful","Dribbles Attempted","Total Pass Distance","Short Passes Completed","Short Passes Attempted","Short Pass Completion %","Med Passes Completed","Med Passes Attempted","Med Pass Completion %","Long Passes Completed","Long Passes Attempted","Long Pass Completion %","Key Passes","Passes into Final Third","Passes into Penalty Area","Crosses into Penalty Area","Total Progressive Passes","Passes Live","Passes Dead","Free Kicks","Through Balls","Passes under Pressure","Pitch Switches","Crosses","Corners","Corners In","Corners Out","Corners Straight","Passes Ground","Passes Low","Passes High","Passes Left Foot","Passes Right Foot","Passes Head","Throw-Ins","Passes Other Body Part","Passes Offside","Passes Out of Bounds","Passes Intercepted","Passes Blocked","SCA via Live Pass","SCA via Dead Pass","SCA via Dribble","SCA via Shot","SCA via Foul Drawn","GCA via Live Pass","GCA via Dead Pass","GCA via Dribble","GCA via Shot","GCA via Foul Drawn","Forced Own Goals","Tackles Won","Tackles Def. Third","Tackles Mid Third","Tackles Att Third","Tackles vs Dribblers","Tackles vs Dribblers Attempted","Tackles vs Dribblers Success %","Times Dribbled Past","Pressures Successful","Pressures Success %","Pressures Def Third","Pressures Mid Third","Pressures Att Third","Blocked Shots","Saved Shots","Blocked Passes","Clearances","Errors","Touches in Def Pen","Touches in Def Third","Touches in Mid Third","Touches in Att Third","Touches in Att Pen","Live Touches","Dribble Success %","Players Dribbled Past","Carry Total Distance","Times Targeted for Pass","Times Received Pass","Pass Reception %","Miscontrols","Times Dispossessed","Fouls Committed","Fouls Drawn","Offsides","PKs Won","PKs Conceded","Own Goals","Loose Balls Recovered","Aerials Won","Aerials Lost","Aerial Win %"]
    ws.append(titles)
    avg_titles = ["Player","Height (cm)","Weight (kg)","Team","Position","Minutes","Goals","Assists","PKs","PK Attempts","Shots","Shots on Target","Yellows","Reds","Touches","Pressures","Tackles","Interceptions","Blocks","xG","Non-Pen xG","xA","Shot-Creating Actions","Goal-Creating Actions","Passes Completed","Passes Attempted","Pass Completion %","Prog. Pass Distance","Carries","Prog. Carry Distance","Dribbles Successful","Dribbles Attempted","Total Pass Distance","Short Passes Completed","Short Passes Attempted","Short Pass Completion %","Med Passes Completed","Med Passes Attempted","Med Pass Completion %","Long Passes Completed","Long Passes Attempted","Long Pass Completion %","Key Passes","Passes into Final Third","Passes into Penalty Area","Crosses into Penalty Area","Total Progressive Passes","Passes Live","Passes Dead","Free Kicks","Through Balls","Passes under Pressure","Pitch Switches","Crosses","Corners","Corners In","Corners Out","Corners Straight","Passes Ground","Passes Low","Passes High","Passes Left Foot","Passes Right Foot","Passes Head","Throw-Ins","Passes Other Body Part","Passes Offside","Passes Out of Bounds","Passes Intercepted","Passes Blocked","SCA via Live Pass","SCA via Dead Pass","SCA via Dribble","SCA via Shot","SCA via Foul Drawn","GCA via Live Pass","GCA via Dead Pass","GCA via Dribble","GCA via Shot","GCA via Foul Drawn","Forced Own Goals","Tackles Won","Tackles Def. Third","Tackles Mid Third","Tackles Att Third","Tackles vs Dribblers","Tackles vs Dribblers Attempted","Tackles vs Dribblers Success %","Times Dribbled Past","Pressures Successful","Pressures Success %","Pressures Def Third","Pressures Mid Third","Pressures Att Third","Blocked Shots","Saved Shots","Blocked Passes","Clearances","Errors","Touches in Def Pen","Touches in Def Third","Touches in Mid Third","Touches in Att Third","Touches in Att Pen","Live Touches","Dribble Success %","Players Dribbled Past","Carry Total Distance","Times Targeted for Pass","Times Received Pass","Pass Reception %","Miscontrols","Times Dispossessed","Fouls Committed","Fouls Drawn","Offsides","PKs Won","PKs Conceded","Own Goals","Loose Balls Recovered","Aerials Won","Aerials Lost","Aerial Win %"]
    ws2.append(avg_titles)

# Builds league
print()
chosen_league = League(league, leagues[league], season)

# Creates timer for time estimate
timer = Timer(chosen_league)

# For each player in each team...
for team in chosen_league.teams:
# team = Team("Celta Vigo","f25da7fb",season)

    print()
    print("------------ "+team.name+" ------------   (Est. time remaining: "+timer.time_remaining()+")")

    for player in team.players:

        print("Scraping "+player.name+"...")

        # Scrape player data from each page using Scraper, with 3 attempts in case of anomalous error which sometimes occurs
        attempts = 0
        successful = False
        while attempts < 3 and not successful:
            try:
                scraper = Scraper(player.url_code, player.season, player.name)
                summary = scraper.summary_scrape()
                passes = scraper.passing_scrape()
                pass_types = scraper.pass_types_scrape()
                gca = scraper.gca_scrape()
                defense = scraper.defense_scrape()
                possession = scraper.possession_scrape()
                misc = scraper.misc_scrape()
                successful = True
            except:
                attempts += 1
                pass

        # Populate main Excel sheet with raw player data
        index = 0
        for match in summary:

            calc = Calculator(match)

            calc.add_data(passes, index)
            calc.add_data(pass_types, index)
            calc.add_data(gca, index)
            calc.add_data(defense, index)
            calc.add_data(possession, index)
            calc.add_data(misc, index)

            ws.append(calc.get_match())
            index+=1

        # Calculates and populates Averages tab
        new_summary = Scraper(player.url_code, player.season, player.name).summary_scrape()
        if len(new_summary) > 0:

            # Player's name, height, weight, club, position
            average_header = [new_summary[0][0],new_summary[0][1],new_summary[0][2],new_summary[0][7],new_summary[0][9]]

            avg_calc = Calculator(average_header)

            avg_calc.calc_averages(new_summary, 10)
            avg_calc.calc_averages(passes, 0)
            avg_calc.calc_averages(pass_types, 0)
            avg_calc.calc_averages(gca, 0)
            avg_calc.calc_averages(defense, 0)
            avg_calc.calc_averages(possession, 0)
            avg_calc.calc_averages(misc, 0)

            ws2.append(avg_calc.get_averages())

wb.save(excelFile)
print()
print("Finished! The Excel file is located in the program directory.")
