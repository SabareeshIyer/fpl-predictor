from pydantic import BaseModel

class TeamSkeletonStats(BaseModel):
    name: str
    team_id: int

    xg_total: float
    xga_total: float
    g_total: int
    ga_total: int
    npxg_total: float
    npxga_total: float
    games_played: int

    xg_avg: float
    xga_avg: float
    goals_scored_avg: float
    goals_conceded_avg: float

