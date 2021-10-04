from pandas import DataFrame
from typing import List, Tuple, Dict
from models.team_stats import TeamSkeletonStats


def get_opponents_in_given_fixture_list(team_id: int, fixtures: DataFrame) -> List[int]:
    home_opponents = fixtures.loc[fixtures['team_a'] == team_id, 'team_h']
    away_opps = fixtures.loc[fixtures['team_h'] == team_id, 'team_a']

    return list(home_opponents.values) + list(away_opps.values)


def get_prev_and_next_opponents(
        team_id: int,
        number_of_opponents_to_get: int,
        fixtures: DataFrame
) -> Tuple[List[int], List[int]]:

    team_fixtures = fixtures[(fixtures['team_a'] == team_id) | (fixtures['team_h'] == team_id)]

    completed_fixtures = team_fixtures[team_fixtures['finished'] == True]
    upcoming_fixtures = team_fixtures[team_fixtures['finished'] == False]

    # all_previous_opponents = get_opponents_in_given_fixture_list(team_id, completed_fixtures)
    previous_x_opponents = get_opponents_in_given_fixture_list(team_id, completed_fixtures.tail(number_of_opponents_to_get))
    next_x_opponents = get_opponents_in_given_fixture_list(team_id, upcoming_fixtures.head(number_of_opponents_to_get))

    return previous_x_opponents, next_x_opponents


def get_current_team_stats(team: str, team_id: int, teams_data: Dict[str, DataFrame]) -> TeamSkeletonStats:
    relevant_team_data = teams_data[team]
    xg_total = relevant_team_data.xG.sum()
    xga_total = relevant_team_data.xGA.sum()
    npxg_total = relevant_team_data.npxG.sum()
    npxga_total = relevant_team_data.npxGA.sum()
    goals_scored_total = relevant_team_data.scored.sum()
    goals_conceded_total = relevant_team_data.missed.sum()
    games_played = len(relevant_team_data.index)

    xg_avg = xg_total / games_played
    xga_avg = xga_total / games_played
    goals_scored_avg = goals_scored_total / games_played
    goals_conceded_avg = goals_conceded_total / games_played

    return TeamSkeletonStats(
        xg_total=xg_total,
        xga_total=xga_total,
        npxg_total=npxg_total,
        npxga_total=npxga_total,
        g_total=goals_scored_total,
        ga_total=goals_conceded_total,
        games_played=games_played,
        xg_avg=xg_avg,
        xga_avg=xga_avg,
        goals_scored_avg=goals_scored_avg,
        goals_conceded_avg=goals_conceded_avg,
        name=team,
        team_id=team_id,
    )