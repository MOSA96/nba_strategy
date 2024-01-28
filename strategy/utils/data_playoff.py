import pandas as pd
import numpy as np
import seasonal_playoff

games_data = seasonal_playoff.read_json("D:/Programacion/nba_strategy/data/2023-2022.json")
playoff_data = seasonal_playoff.filter_playoff(games_data)
playoff_games = seasonal_playoff.playoff_matches(playoff_data)
ids_dict = seasonal_playoff.create_dict_ids(playoff_games)
games_with_series = seasonal_playoff.games_by_series(playoff_data, ids_dict)

rows = []

for series_id, series_data in games_with_series.items():
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
result["date"] = pd.to_datetime(result["date"], format="%d %b %Y")
result["winner"] = np.where(result["local_points"]>result["visit_points"], result["local_team"], result["visit_team"])
result.sort_values(['series_id', 'date'], inplace=True)
result.reset_index(drop=True, inplace=True)


for series_id in result['series_id'].unique():
    series_df = result[result['series_id'] == series_id]
    
    first_three_wins_team = series_df.loc[series_df.index[:3], 'winner'].unique()
    if len(first_three_wins_team) == 1 and series_df['winner'].eq(first_three_wins_team[0]).rolling(window=3).sum().max() == 3:
        result.loc[result['series_id'] == series_id, 'strategy'] = 1
    


result[['series_id', 'date', 'team_1', 'team_2', 'local_team', 'local_points','visit_team', 'visit_points', 'winner', "strategy"]].to_csv("test_result.csv")


