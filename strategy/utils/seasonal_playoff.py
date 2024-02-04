import json
import uuid
import pandas as pd

def read_json(filename: str) -> list:
    file = open(filename)
    return json.load(file)

def filter_playoff(data: list) -> list:
    return [i for i in data if "Play Offs" in i["date"] and "Promotion" not in i["date"]]

def playoff_matches(playoffs_list: list) -> set:
    series = list(set((match["local_team"], match["visit_team"]) for match in playoffs_list))
    return set(frozenset(t) for t in series)

def create_dict_ids(series: set) -> dict:
    return {str(uuid.uuid4())[:4]: {"teams": data, "games": []} for data in series}

def games_by_series(playoff_data: list, series: dict) -> dict:
    for match in playoff_data:
        local = match.get("local_team")
        visit = match.get("visit_team")
        teams = frozenset((local, visit))
        for key, value in series.items():
            if teams == value['teams']:
                value["games"].append(match)
    return series
