import pandas as pd
import numpy as np
import seasonal_playoff


def create_dataframe(games:dict) -> pd.DataFrame:
    rows = []
    for series_id, series_data in games.items():
        for game in series_data['games']:
            row = {
                'series_id': series_id,
                'date': game["date"].split("-")[0].strip(),
                'team_1': list(series_data['teams'])[0],
                'team_2': list(series_data['teams'])[1],
                'local_team': game['local_team'],
                'local_points': int(game['local_points']),
                'visit_team': game['visit_team'],
                'visit_points':  int(game['visit_points']),
                '10x10bet': game['odds_by_house'].get('10x10bet'),
                '1xBet': game['odds_by_house'].get('1xBet'),
                'Alphabet': game['odds_by_house'].get('Alphabet'),
                'bet-at-home': game['odds_by_house'].get('bet-at-home'),
                'bet365': game['odds_by_house'].get('bet365'),
                'BetInAsia': game['odds_by_house'].get('BetInAsia'),
                'GGBET': game['odds_by_house'].get('GGBET'),
                'Marsbet': game['odds_by_house'].get('Marsbet'),
                'Pinnacle': game['odds_by_house'].get('Pinnacle'),
                'Unibet': game['odds_by_house'].get('Unibet'),
                'VOBET': game['odds_by_house'].get('VOBET'),
                'William Hill': game['odds_by_house'].get('William Hill')
            }
            rows.append(row)
    result = pd.DataFrame(rows)
    return result


def identify_winner(df:pd.DataFrame):

    df["date"] = pd.to_datetime(df["date"], format="%d %b %Y")
    df["winner"] = np.where(df["local_points"]>df["visit_points"], df["local_team"], df["visit_team"])
    df.sort_values(['series_id', 'date'], inplace=True)
    df.reset_index(drop=True, inplace=True)


def identify_series(df:pd.DataFrame):
    for series_id in df['series_id'].unique():
        series_df = df[df['series_id'] == series_id]
        
        first_three_wins_team = series_df.loc[series_df.index[:3], 'winner'].unique()

        if series_df['winner'].eq(series_df['winner'].iloc[0]).rolling(window=4).sum().max() == 3:
            df.loc[df['series_id'] == series_id, 'strategy'] = 2

        if len(first_three_wins_team) == 1 and series_df['winner'].eq(first_three_wins_team[0]).rolling(window=3).sum().max() == 3:
            df.loc[df['series_id'] == series_id, 'strategy'] = 1


def get_mean_lines(df:pd.DataFrame):
        houses = ["10x10bet","1xBet","Alphabet","bet-at-home","bet365","BetInAsia","GGBET","Marsbet","Pinnacle","Unibet","VOBET","William Hill"]
        three_series = df[(df["strategy"] == 1.0)]
        four_series = df[(df["strategy"] == 2.0)]
        local_means_three = []
        visit_means_three = []
        local_means_four = []
        visit_means_four = []
        for house in houses:
            local_means_three.append(three_series[house].str[0].astype("float").mean())
            visit_means_three.append(three_series[house].str[1].astype("float").mean())
        for house in houses:
            local_means_four.append(four_series[house].str[0].astype("float").mean())
            visit_means_four.append(four_series[house].str[1].astype("float").mean())
        local_mean_three = np.mean(local_means_three)
        visit_mean_three  = np.mean(visit_means_three)
        local_mean_four = np.mean(local_means_four)
        visit_mean_four  = np.mean(visit_means_four)
        four_seres = df[(df["strategy"] == 2.0)]
        print("gadg")
        



if __name__== "__main__":
    games_data = seasonal_playoff.read_json("D:/Programacion/nba_strategy/data/2023-2022.json")
    playoff_data = seasonal_playoff.filter_playoff(games_data)
    playoff_games = seasonal_playoff.playoff_matches(playoff_data)
    ids_dict = seasonal_playoff.create_dict_ids(playoff_games)
    games_with_series = seasonal_playoff.games_by_series(playoff_data, ids_dict)
    dataframe = create_dataframe(games_with_series)
    identify_winner(dataframe)
    identify_series(dataframe)
    get_mean_lines(dataframe)
    dataframe[['series_id', 'date', 'team_1', 'team_2', 'local_team', 'local_points','visit_team', 'visit_points', 'winner', "strategy"]].to_csv("test_result.csv")

