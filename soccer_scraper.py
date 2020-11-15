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
leagues = {"EPL": 9, "SERIEA": 11, "LALIGA": 12, "LIGUE1": 13, "BUNDESLIGA": 20}

# User input
print()
league = input("Choose [EPL], [SERIEA], [LALIGA], [LIGUE1], or [BUNDESLIGA]: ")
season = input("Choose season ('2019-2020', for example): ")

# If invalid input...
while league not in leagues.keys():
    print("Invalid league. Try again.")
    league = input("Choose [EPL], [SERIEA], [LALIGA], [LIGUE1], or [BUNDESLIGA]: ")

# Excel file setup
if xlInstalled:
    excelFile = input("Excel file for output: ")
    if not excelFile.endswith(".xlsx") or not excelFile.endswith(".xls"):
        excelFile += ".xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Raw Data"
    titles = ["Player","Height (cm)","Weight (kg)","Date","Day of Week","Competition","Venue","Result","Team","Opponent","Position","Minutes","Goals","Assists","PKs","PK Attempts","Shots","Shots on Target","Yellows","Reds","Touches","Pressures","Tackles","Interceptions","Blocks","xG","Non-Pen xG","xA","Shot-Creating Actions","Goal-Creating Actions","Passes Completed","Passes Attempted","Pass Completion %","Prog. Pass Distance","Carries","Prog. Carry Distance","Dribbles Successful","Dribbles Attempted","Total Pass Distance","Short Passes Completed","Short Passes Attempted","Short Pass Completion %","Med Passes Completed","Med Passes Attempted","Med Pass Completion %","Long Passes Completed","Long Passes Attempted","Long Pass Completion %","Key Passes","Passes into Final Third","Passes into Penalty Area","Crosses into Penalty Area","Total Progressive Passes","Passes Live","Passes Dead","Free Kicks","Through Balls","Passes under Pressure","Pitch Switches","Crosses","Corners","Corners In","Corners Out","Corners Straight","Passes Ground","Passes Low","Passes High","Passes Left Foot","Passes Right Foot","Passes Head","Throw-Ins","Passes Other Body Part","Passes Offside","Passes Out of Bounds","Passes Intercepted","Passes Blocked","SCA via Live Pass","SCA via Dead Pass","SCA via Dribble","SCA via Shot","SCA via Foul Drawn","SCA via Defense","GCA via Live Pass","GCA via Dead Pass","GCA via Dribble","GCA via Shot","GCA via Foul Drawn","GCA via Defense","Forced Own Goals","Tackles Won","Tackles Def. Third","Tackles Mid Third","Tackles Att Third","Tackles vs Dribblers","Tackles vs Dribblers Attempted","Tackles vs Dribblers Success %","Times Dribbled Past","Pressures Successful","Pressures Success %","Pressures Def Third","Pressures Mid Third","Pressures Att Third","Blocked Shots","Saved Shots","Blocked Passes","Clearances","Errors","Touches in Def Pen","Touches in Def Third","Touches in Mid Third","Touches in Att Third","Touches in Att Pen","Live Touches","Dribble Success %","Players Dribbled Past","Carry Total Distance","Times Targeted for Pass","Times Received Pass","Pass Reception %","Miscontrols","Times Dispossessed","Fouls Committed","Fouls Drawn","Offsides","PKs Won","PKs Conceded","Own Goals","Loose Balls Recovered","Aerials Won","Aerials Lost","Aerial Win %","Clean Sheet","Total Minutes","AvgMinutes","AvgGoals","AvgAssists","AvgPKs","Avg PK Attempts","AvgShots","Avg Shots on Target","AvgYellows","AvgReds","AvgTouches","AvgPressures","AvgTackles","AvgInterceptions","AvgBlocks","AvgxG","Avg Non-Pen xG","AvgxA","Avg Shot-Creating Actions","Avg Goal-Creating Actions","Avg Passes Completed","Avg Passes Attempted","Avg Pass Completion %","Avg Prog. Pass Distance","AvgCarries","Avg Prog. Carry Distance","Avg Dribbles Successful","Avg Dribbles Attempted","Avg Total Pass Distance","Avg Short Passes Completed","Avg Short Passes Attempted","Avg Short Pass Completion %","Avg Med Passes Completed","Avg Med Passes Attempted","Avg Med Pass Completion %","Avg Long Passes Completed","Avg Long Passes Attempted","Avg Long Pass Completion %","Avg Key Passes","Avg Passes into Final Third","Avg Passes into Penalty Area","Avg Crosses into Penalty Area","Avg Total Progressive Passes","Avg Passes Live","Avg Passes Dead","Avg Free Kicks","Avg Through Balls","Avg Passes under Pressure","Avg Pitch Switches","Avg Crosses","Avg Corners","Avg Corners In","Avg Corners Out","Avg Corners Straight","Avg Passes Ground","Avg Passes Low","Avg Passes High","Avg Passes Left Foot","Avg Passes Right Foot","Avg Passes Head","AvgThrow-Ins","Avg Passes Other Body Part","Avg Passes Offside","Avg Passes Out of Bounds","Avg Passes Intercepted","Avg Passes Blocked","Avg SCA via Live Pass","Avg SCA via Dead Pass","Avg SCA via Dribble","Avg SCA via Shot","Avg SCA via Foul Drawn","Avg SCA via Defense","Avg GCA via Live Pass","Avg GCA via Dead Pass","Avg GCA via Dribble","Avg GCA via Shot","Avg GCA via Foul Drawn","Avg GCA via Defense","Avg Forced Own Goals","Avg Tackles Won","Avg Tackles Def. Third","Avg  Tackles Mid Third","Avg Tackles Att Third","Avg Tackles vs Dribblers","Avg Tackles vs Dribblers Attempted","Avg Tackles vs Dribblers Success %","Avg Times Dribbled Past","Avg Pressures Successful","Avg Pressures Success %","Avg Pressures Def Third","Avg Pressures Mid Third","Avg Pressures Att Third","Avg Blocked Shots","Avg Saved Shots","Avg Blocked Passes","AvgClearances","AvgErrors","Avg Touches in Def Pen","Avg Touches in Def Third","Avg Touches in Mid Third","Avg Touches in Att Third","Avg Touches in Att Pen","Avg Live Touches","Avg Dribble Success %","Avg Players Dribbled Past","Avg Carry Total Distance","Avg Times Targeted for Pass","Avg Times Received Pass","Avg Pass Reception %","AvgMiscontrols","Avg Times Dispossessed","Avg Fouls Committed","Avg Fouls Drawn","AvgOffsides","Avg PKs Won","Avg PKs Conceded","Avg Own Goals","Avg Loose Balls Recovered","Avg Aerials Won","Avg Aerials Lost","Avg Aerial Win %","Avg Clean Sheets"]
    ws.append(titles)

# Builds league
print()
chosen_league = League(league, leagues[league], season)

# Creates timer for time estimate
timer = Timer(chosen_league)

# For each player in each team...
for team in chosen_league.teams:

    print()
    print("------------ "+team.name+" ------------   (Est. time remaining: "+timer.time_remaining()+")")

    for player in team.players:
        
        # Added this try/except to save Excel file, in case program breaks midway
        # One can fairly easily alter the program to only gather data after it finds the relevant team
        try:
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
                    new_summary = Scraper(player.url_code, player.season, player.name).summary_scrape()
                    successful = True
                except:
                    attempts += 1
                    pass

            # Adds clean sheets to end of misc
            match_index = 0
            for match in summary:
                result = match[7]
                if ("W" in result or "D" in result) and "0" in result:
                    misc[match_index].append("1")
                else:
                    misc[match_index].append("0")
                match_index += 1

            # Calculates averages per 90 using Calculator class
            total_min = 0
            if len(new_summary) > 0:

                # Calculate total and average minutes
                for match in new_summary:
                    try:
                        total_min += int(match[11])
                    except:
                        pass
                average_minutes = round(total_min/len(new_summary),2)

                # Calculate averages per game
                avg_calc = Calculator([])

                avg_calc.calc_averages(new_summary, 11)
                avg_calc.calc_averages(passes, 0)
                avg_calc.calc_averages(pass_types, 0)
                avg_calc.calc_averages(gca, 0)
                avg_calc.calc_averages(defense, 0)
                avg_calc.calc_averages(possession, 0)
                avg_calc.calc_averages(misc, 0)

                # Calculates and returns averages per 90
                averages = avg_calc.get_averages(average_minutes)

            # Populate Excel sheet with raw player data
            index = 0
            for match in summary:

                calc = Calculator(match)

                calc.add_data(passes, index)
                calc.add_data(pass_types, index)
                calc.add_data(gca, index)
                calc.add_data(defense, index)
                calc.add_data(possession, index)
                calc.add_data(misc, index)

                full_match = calc.get_match()

                # Add total min and averages to raw data, then add array to Excel sheet
                full_match.append(int(total_min))
                full_match.extend(averages)
                index+=1
                ws.append(full_match)
        except:
            wb.save(excelFile)
            print()
            print("The program failed on "+player.name+" of "+team.name+". However, the Excel file "+excelFile+" is located in the program directory.")
            quit()

# Saves Excel file and prints finished message
wb.save(excelFile)
print()
print("Finished! The Excel file "+excelFile+" is located in the program directory.")
