def predict_number_of_goals_team_will_score(prev_x_opp_stats, next_x_opp_stats, teams_data, team, number_of_opps):
    sum_of_avg_goals_let_in_by_prev_opps = sum(opp.goals_conceded_avg for opp in prev_x_opp_stats)
    goals_scored_by_team_in_prev_x_matches = teams_data[team].tail(number_of_opps).scored.sum()
    sum_of_avg_goals_let_in_by_next_opps = sum(opp.goals_conceded_avg for opp in next_x_opp_stats)
    goals_team_will_score_in_next_x_matches = (
        goals_scored_by_team_in_prev_x_matches / sum_of_avg_goals_let_in_by_prev_opps
    ) * sum_of_avg_goals_let_in_by_next_opps

    return round(goals_team_will_score_in_next_x_matches, 2)


def predict_number_of_goals_team_will_concede(prev_x_opp_stats, next_x_opp_stats, teams_data, team, number_of_opps):
    sum_of_avg_goals_scored_by_prev_opps = sum(opp.goals_scored_avg for opp in prev_x_opp_stats)
    goals_conceded_by_team_in_prev_x_matches = teams_data[team].tail(number_of_opps).missed.sum()
    sum_of_goals_scored_by_next_opps = sum(opp.goals_scored_avg for opp in next_x_opp_stats)

    goals_team_will_concede_in_next_x_matches = (
        goals_conceded_by_team_in_prev_x_matches / sum_of_avg_goals_scored_by_prev_opps
    ) * sum_of_goals_scored_by_next_opps

    return round(goals_team_will_concede_in_next_x_matches, 2)


def get_result_by_goal_frequency(teams_by_goals, number_of_opponents_to_get):
    interim = {}
    for k, v in teams_by_goals.items():
        if v < 0.5 * number_of_opponents_to_get:
            interim[k] = "Less than 0.5 goals per game"
        elif v < number_of_opponents_to_get:
            interim[k] = "0.5-1 goal per game"
        elif v < 1.5 * number_of_opponents_to_get:
            interim[k] = "1-1.5 goals per game"
        elif v < 2 * number_of_opponents_to_get:
            interim[k] = "1.5-2 goals per game"
        else:
            interim[k] = "More than 2 goals per game"

    reindexed = {}
    for v in interim.values():
        reindexed[v] = [key for key in interim.keys() if interim[key] == v]
        # reindexed[v] = ', '.join(reindexed[v])  # use this for string result

    return reindexed