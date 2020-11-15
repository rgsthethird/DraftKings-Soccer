# DraftKings-Soccer
 Web Scraper for Draftkings Soccer Data Aggregation

<strong>Soccer-scraper</strong> takes a league as input and outputs all data stored on fbref.com for each player - and each statistic for each match of the player's current season - in an Excel file, along with a separate tab with each player's statistical averages.

I created this scraper to get quick access to data to inform my daily fantasy picks in DraftKings.

Currently, the English Premier League, the Spanish La Liga, the Italian Serie A, the German Bundesliga, and the French Ligue 1 are all supported.

<strong>Lineup.py</strong> and <strong>values.txt</strong> are an attempt to optimize a Draftkings lineup using a greedy knapsack algorithm. It's not operational. I'm open to collaboration if you have a possible solution to this problem (maximizing expected points given associated cost for each player and a maximum total possible cost).

I've included example Excel outputs from the 2020-2021 season. This program requires BeautifulSoup4.
