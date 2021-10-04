from typing import Tuple, Dict
from data import get_all_team_data, get_fixtures_data
from methods.opponent_info import get_prev_and_next_opponents, get_current_team_stats
from methods.computations import predict_number_of_goals_team_will_concede, predict_number_of_goals_team_will_score, get_result_by_goal_frequency
from methods.utility import save_to_file

TEAM_INDEX = {
    1: 'Arsenal',
    2: 'Aston_Villa',
    3: 'Brentford',
    4: 'Brighton',
    5: 'Burnley',
    6: 'Chelsea',
    7: 'Crystal_Palace',
    8: 'Everton',
    9: 'Leicester',
    10: 'Leeds',
    11: 'Liverpool',
    12: 'Manchester_City',
    13: 'Manchester_United',
    14: 'Newcastle_United',
    15: 'Norwich',
    16: 'Southampton',
    17: 'Tottenham',
    18: 'Watford',
    19: 'West_Ham',
    20: 'Wolverhampton_Wanderers',
}
TEAM_ID_INDEX = dict(zip(TEAM_INDEX.values(), TEAM_INDEX.keys()))
NUMBER_OF_OPPONENTS_TO_GET = 6


def get_major_predictions(
        fixtures, teams_data, all_teams_base_stats
) -> Tuple[Dict[str, float], Dict[str, float]]:
    teams_by_goals_they_will_score = {}
    teams_by_goals_they_will_concede = {}

    for team, team_id in TEAM_ID_INDEX.items():
        previous_x_opponents, next_x_opponents = get_prev_and_next_opponents(team_id, NUMBER_OF_OPPONENTS_TO_GET, fixtures)

        get_base_stats_for_given_opps = lambda opponent_list: [all_teams_base_stats[TEAM_INDEX.get(opponent)] for opponent in opponent_list]
        # the below 2 are each lists of team stats - one TeamSkeletonStats for each opponent
        prev_x_opp_stats = get_base_stats_for_given_opps(previous_x_opponents)
        next_x_opp_stats = get_base_stats_for_given_opps(next_x_opponents)

        # main calc
        teams_by_goals_they_will_score[team] = predict_number_of_goals_team_will_score(
            prev_x_opp_stats,
            next_x_opp_stats,
            teams_data,
            team,
            NUMBER_OF_OPPONENTS_TO_GET,
        )
        teams_by_goals_they_will_score = dict(sorted(teams_by_goals_they_will_score.items(), key=lambda item: item[1], reverse=True))

        teams_by_goals_they_will_concede[team] = predict_number_of_goals_team_will_concede(
            prev_x_opp_stats,
            next_x_opp_stats,
            teams_data,
            team,
            NUMBER_OF_OPPONENTS_TO_GET,
        )
        teams_by_goals_they_will_concede = dict(sorted(teams_by_goals_they_will_concede.items(), key=lambda item: item[1]))
    return teams_by_goals_they_will_score, teams_by_goals_they_will_concede


if __name__ == "__main__":
    fixtures = get_fixtures_data()
    teams_data = get_all_team_data()

    # compute and store stats for each team
    all_teams_base_stats = {team: get_current_team_stats(team, team_id, teams_data) for team, team_id in TEAM_ID_INDEX.items()}

    # print this for exact numbers of goals that will be scored/conceded
    high_scoring, high_clean_sheet = get_major_predictions(fixtures, teams_data, all_teams_base_stats)

    top_scoring_by_frequency = get_result_by_goal_frequency(high_scoring, NUMBER_OF_OPPONENTS_TO_GET)
    best_defense_by_frequency = get_result_by_goal_frequency(high_clean_sheet, NUMBER_OF_OPPONENTS_TO_GET)
    data_to_save = {
        "Top scoring by goal frequency": top_scoring_by_frequency,
        "Top scoring by team name (sorted)": high_scoring,
        "Best defense by goals allowed frequency": best_defense_by_frequency,
        "Best defense by team name (sorted)": high_clean_sheet,
    }
    save_to_file(data_to_save)

    # print(f"\nHigh scoring teams for next 6 games: {json.dumps(top_scoring_by_frequency, indent=4)}\n\n")
    # print(f"Best for cleansheets for next 6 games: {json.dumps(best_defense_by_frequency, indent=4)}")

