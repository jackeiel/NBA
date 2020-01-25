from time import sleep

import pandas as pd

from predictions.predictions import GamePredict
from utilities import find_games, get_lines

pd.set_option('display.width', 1500)
pd.set_option('display.max_columns', 100)

def todays_bets(book='Caesars', threshold=4, display=True, save=True):
    """
    Generates potential value bets for todays games.
    :param book (str, optional): The sports book to use
    :param threshold (int, optional): The value threshold for making a bet
    :param display (bool, optional): Print resulting DataFrame to screen
    :param save (bool, optional): Save csv file to DATA/Predictions folder
    :return: DataFrame of games and bets
    """
    lines = get_lines(sportsbook=book)
    games = find_games()

    #TODO filter down games
    full = games.merge(lines, how='left', left_on=['HOME_TEAM_ID', 'VISITOR_TEAM_ID'],
                       right_on=['home_team', 'away_team'])

    def internal_predict(row):
        sleep(10)
        return GamePredict(row.home_team, row.away_team).predict_spread()

    full['predicted_spread'] = full.apply(internal_predict, axis=1)

    #TODO write bet algo
    def place_bet(row, threshold=4):
        if max(row.vegas_line_home, row.predicted_spread) - min(row.vegas_line_home, row.predicted_spread) > threshold:
            if row.vegas_line_home - row.predicted_spread > row.predicted_spread - row.vegas_line_home:
                return row.home_team
            else:
                return row.away_team
        else:
            return '---'

    full['bet'] = full.apply(place_bet, threshold=threshold, axis=1)

    # full = full.drop('GAME_DATE_EST', axis=1)

    if display:
        print(full)

    if save:
        # TODO simple date
        date = pd.Timestamp('today').date()
        full.to_csv(f'DATA/Predictions/{date}.csv')

    return full