
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

city_to_abrv = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Cleveland': 'CLE', 'New Orleans': 'NOP',
                'Chicago': 'CHI', 'Dallas': 'DAL', 'Denver': 'DEN', 'Golden State': 'GSW',
                'Houston': 'HOU', 'Los Angeles': 'LAL', 'Miami': 'MIA', 'Milwaukee': 'MIL',
                'Minnesota': 'MIN', 'Brooklyn': 'BKN', 'New York': 'NYK', 'Orlando': 'ORL',
                'Indiana': 'IND', 'Philadelphia': 'PHI', 'Phoenix': 'PHX', 'Portland': 'POR',
                'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Oklahoma City': 'OKC',
                'Toronto': 'TOR', 'Utah': 'UTA', 'Memphis': 'MEM', 'Washington': 'WAS',
                'Detroit': 'DET', 'Charlotte': 'CHA'}


def get_lines(sportsbook='Caesars'):
    '''
    Scrape current available NBA lines from http://www.espn.com/nba/lines.
    Typically only *today's* games

    :param sportsbook (str, optional): any sportsbook listed on the webpage. Default to Caesars.
    :return: DataFrame
    '''
    driver = webdriver.Safari()
    driver.get('http://www.espn.com/nba/lines')
    driver.find_element_by_tag_name('tbody').text

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find('table', attrs={'class':'tablehead'})
    rows = table.find_all('tr')
    book = [row for row in rows if row.find('td').text==sportsbook]

    def home_internal_spread(game):
        try:
            return float(game.find('table').find_all('br')[0].next_sibling)
        except:
            return float(0.0)

    def home_internal_odds(game):
        try:
            return game.find('table').find_all('br')[1].next_sibling
        except:
            return float(0.0)

    def home_internal_team(team):
        try:
            return team.split(':')[0]
        except:
            return 'NA'

    home_spread = [home_internal_spread(game) for game in book]
    home_odds = [home_internal_odds(game) for game in book]
    home_team = [home_internal_team(team) for team in home_odds]

    def away_internal_spread(game):
        try:
            return float(game.find('table').find_all('br')[0].previous_sibling)
        except:
            return float(0.0)

    def away_interal_odds(game):
        try:
            return game.find('table').find_all('br')[1].previous_sibling
        except:
            return float(0.0)

    def away_internal_team(team):
        try:
            return team.split(':')[0]
        except:
            return 'NA'

    away_spread = [away_internal_spread(game) for game in book]
    away_odds = [away_interal_odds(game) for game in book]
    away_team = [away_internal_team(team) for team in away_odds]

    df = pd.DataFrame(data={'GAME_DATE' : pd.to_datetime('today'), 'vegas_line_home' : home_spread, 'home_odds' : home_odds,
                            'vegas_line_away' : away_spread, 'away_odds' : away_odds,
                            'home_team' : home_team, 'away_team' : away_team})
    df.home_team.replace(city_to_abrv, inplace=True)
    df.away_team.replace(city_to_abrv, inplace=True)

    return df