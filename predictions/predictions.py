# common functions

import pickle
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder, boxscoreadvancedv2

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

team_id_mapper = {'ATL': 1610612737, 'BOS': 1610612738, 'CLE': 1610612739, 'NOP': 1610612740, 'CHI': 1610612741,
                  'DAL': 1610612742, 'DEN': 1610612743, 'GSW': 1610612744, 'HOU': 1610612745, 'LAC': 1610612746,
                  'LAL': 1610612747, 'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'BKN': 1610612751,
                  'NYK': 1610612752, 'ORL': 1610612753, 'IND': 1610612754, 'PHI': 1610612755, 'PHX': 1610612756,
                  'POR': 1610612757, 'SAC': 1610612758, 'SAS': 1610612759, 'OKC': 1610612760, 'TOR': 1610612761,
                  'UTA': 1610612762, 'MEM': 1610612763, 'WAS': 1610612764, 'DET': 1610612765, 'CHA': 1610612766}

team_names = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI',
              'DAL', 'DEN', 'GSW', 'HOU', 'LAC',
              'LAL', 'MIA', 'MIL', 'MIN', 'BKN',
              'NYK', 'ORL', 'IND', 'PHI', 'PHX',
              'POR', 'SAC', 'SAS', 'OKC', 'TOR',
              'UTA', 'MEM', 'WAS', 'DET', 'CHA']


class GamePredict:
    # I want this to be more flexible than it was in NFL2

    def __init__(self, home, away, model='ridge_1'):
        self.home = home
        self.away = away
        self.model = model
        try:
            self.HOME_TEAM_ID = team_id_mapper[self.home]
        except KeyError:
            print(f'{home} is not a valid team abbreviation.')
            print('Valid abbreviations are:')
            print(team_names)
        try:
            self.VISITOR_TEAM_ID = team_id_mapper[self.away]
        except KeyError:
            print(f'{away} is not a valid team abbreviation.')
            print('Valid abbreviations are:')
            print(team_names)
        self.inputs = self.generate_inputs()

    def generate_inputs(self):
        home_games = leaguegamefinder.LeagueGameFinder(team_id_nullable=self.HOME_TEAM_ID,
                                                       headers=headers).get_data_frames()[0]

        # In[117]:

        home_games.GAME_DATE = pd.to_datetime(home_games.GAME_DATE)
        last5_home = home_games.sort_values(by='GAME_DATE', ascending=False).loc[:5, :]

        away_games = leaguegamefinder.LeagueGameFinder(team_id_nullable=self.VISITOR_TEAM_ID,
                                                       headers=headers).get_data_frames()[0]

        # In[119]:

        away_games.GAME_DATE = pd.to_datetime(away_games.GAME_DATE)
        last5_away = away_games.sort_values(by='GAME_DATE', ascending=False).loc[:5, :]

        # In[120]:

        games_unused = ['season_id', 'team_abbreviation', 'team_name', 'wl', 'min', 'pts', 'fgm', 'fga', 'fg3m', 'fg3a',
                        'ftm', 'fta']

        # In[125]:

        games_unused = [i.upper() for i in games_unused]

        # In[126]:

        last5_home2 = last5_home.drop(games_unused, axis=1)
        last5_away2 = last5_away.drop(games_unused, axis=1)

        home_box = pd.DataFrame()

        for game in last5_home2.GAME_ID:
            box = boxscoreadvancedv2.BoxScoreAdvancedV2(game,
                                                        headers=headers).get_data_frames()[1]
            home_box = pd.concat([home_box, box])

        box_unused = ['team_name', 'team_abbreviation', 'team_city', 'min', 'off_rating', 'def_rating',
                      'net_rating', 'usg_pct', 'pace_per40', 'poss', 'pie']

        box_unused.extend([i for i in home_box.columns if i.startswith('E_')])
        box_unused = [i.upper() for i in box_unused]

        home_box2 = home_box.drop(box_unused, axis=1)

        away_box = pd.DataFrame()

        for game in last5_away2.GAME_ID:
            box = boxscoreadvancedv2.BoxScoreAdvancedV2(game,
                                                        headers=headers).get_data_frames()[1]
            away_box = pd.concat([away_box, box])

        away_box2 = away_box.drop(box_unused, axis=1)

        # THIS IS BAD, A POTENTIAL BUG

        home_box2 = home_box2.loc[home_box2.TEAM_ID == self.HOME_TEAM_ID]
        away_box2 = away_box2.loc[away_box2.TEAM_ID == self.VISITOR_TEAM_ID]
        #print(home_box2.shape, away_box2.shape)

        last5_home2 = last5_home2.loc[last5_home2.TEAM_ID == self.HOME_TEAM_ID]
        last5_away2 = last5_away2.loc[last5_away2.TEAM_ID == self.VISITOR_TEAM_ID]
        #print(last5_home2.shape, last5_away2.shape)

        home_data = home_box2.merge(last5_home2, how='left', on=['GAME_ID',
                                                                 'TEAM_ID'])
        away_data = away_box2.merge(last5_away2, how='left', on=['GAME_ID',
                                                                 'TEAM_ID'])

        #print(home_data.shape, away_data.shape)
        non_pred = ['game_id', 'team_id', 'game_date', 'matchup', 'plus_minus']
        non_pred = [i.upper() for i in non_pred]

        home_data2 = home_data.drop(non_pred, axis=1)
        away_data2 = away_data.drop(non_pred, axis=1)

        #print(home_data2.shape, away_data2.shape)

        test = pd.concat([home_data2, away_data2], axis=1)

        test_values = test.mean().values

        return test_values.reshape(1, -1)

    def predict_spread(self):
        """
        Predict spread for GamePredict object
        :return (int): Spread for home team
        """
        with open(f'models/{self.model}.pickle', mode='rb') as pred:
            predictor = pickle.load(pred)
            return predictor.predict(self.inputs)

