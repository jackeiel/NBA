
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

from nba_api.stats.endpoints import scoreboardv2

city_to_abrv = {'Atlanta': 'ATL', 'Boston': 'BOS', 'Cleveland': 'CLE', 'New Orleans': 'NOP',
                'Chicago': 'CHI', 'Dallas': 'DAL', 'Denver': 'DEN', 'Golden State': 'GSW',
                'Houston': 'HOU', 'Los Angeles': 'LAL', 'Miami': 'MIA', 'Milwaukee': 'MIL',
                'Minnesota': 'MIN', 'Brooklyn': 'BKN', 'New York': 'NYK', 'Orlando': 'ORL',
                'Indiana': 'IND', 'Philadelphia': 'PHI', 'Phoenix': 'PHX', 'Portland': 'POR',
                'Sacramento': 'SAC', 'San Antonio': 'SAS', 'Oklahoma City': 'OKC',
                'Toronto': 'TOR', 'Utah': 'UTA', 'Memphis': 'MEM', 'Washington': 'WAS',
                'Detroit': 'DET', 'Charlotte': 'CHA'}

id_to_abrv = {1610612737: 'ATL', 1610612738: 'BOS', 1610612739: 'CLE', 1610612740: 'NOP',
              1610612741: 'CHI', 1610612742: 'DAL', 1610612743: 'DEN', 1610612744: 'GSW',
              1610612745: 'HOU', 1610612746: 'LAC', 1610612747: 'LAL', 1610612748: 'MIA',
              1610612749: 'MIL', 1610612750: 'MIN', 1610612751: 'BKN', 1610612752: 'NYK',
              1610612753: 'ORL', 1610612754: 'IND', 1610612755: 'PHI', 1610612756: 'PHX',
              1610612757: 'POR', 1610612758: 'SAC', 1610612759: 'SAS', 1610612760: 'OKC',
              1610612761: 'TOR', 1610612762: 'UTA', 1610612763: 'MEM', 1610612764: 'WAS',
              1610612765: 'DET', 1610612766: 'CHA'}

espn_to_api = {'SA': 'SAS', 'NO': 'NOP', 'NY': 'NYK', 'GS': 'GSW', 'UTAH': 'UTA', 'WSH': 'WAS'}

def get_lines(sportsbook='Caesars', display=False):
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

    table = soup.find('table', attrs={'class': 'tablehead'})
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

    #TODO how to just get simple date 2020-01-22 ?
    df = pd.DataFrame(data={'Date_Scraped' : pd.Timestamp('today').date(), 'vegas_line_home' : home_spread, 'home_odds' : home_odds,
                            'vegas_line_away' : away_spread, 'away_odds' : away_odds,
                            'home_team' : home_team, 'away_team' : away_team})
    df.home_team.replace(city_to_abrv, inplace=True)
    df.away_team.replace(city_to_abrv, inplace=True)
    df.replace(espn_to_api, inplace=True)

    if display:
        print(df)

    return df

def find_games(days_ahead=0):
    """
    Pull today's upcoming games

    :param days_ahead (int, optional): number of days ahead from which to pull games
    :return: DataFrame
    """
    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }
    board = scoreboardv2.ScoreboardV2(day_offset=days_ahead, headers=headers).get_data_frames()[0]
    board.replace(id_to_abrv, inplace=True)
    return board[['GAME_DATE_EST', 'GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID']]