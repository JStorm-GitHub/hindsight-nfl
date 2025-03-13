def get_bulk_position_stats(position):
    if position == "QB":
        return ("""AVG(completions) AS avg_completions, AVG(attempts) AS avg_attempts, AVG(passing_yards) AS avg_passing_yards, 
AVG(passing_tds) AS avg_passing_tds, AVG(interceptions) AS avg_interceptions, AVG(sacks) AS avg_sacks, 
AVG(sack_yards) AS avg_sack_yards, AVG(sack_fumbles) AS avg_sack_fumbles, AVG(sack_fumbles_lost) AS avg_sack_fumbles_lost, 
AVG(passing_air_yards) AS avg_passing_air_yards, AVG(passing_yards_after_catch) AS avg_passing_yards_after_catch, 
AVG(passing_first_downs) AS avg_passing_first_downs, AVG(passing_epa) AS avg_passing_epa, 
AVG(passing_2pt_conversions) AS avg_passing_2pt_conversions, AVG(pacr) AS avg_pacr, AVG(dakota) AS avg_dakota, 
AVG(carries) AS avg_carries, AVG(rushing_yards) AS avg_rushing_yards, AVG(rushing_tds) AS avg_rushing_tds, 
AVG(rushing_fumbles) AS avg_rushing_fumbles, AVG(rushing_fumbles_lost) AS avg_rushing_fumbles_lost, 
AVG(rushing_first_downs) AS avg_rushing_first_downs, AVG(rushing_epa) AS avg_rushing_epa, 
AVG(rushing_2pt_conversions) AS avg_rushing_2pt_conversions, AVG(fantasy_points) AS avg_fantasy_points, 
AVG(fantasy_points_ppr) AS avg_fantasy_points_ppr, AVG(age) AS avg_age""")
    elif position == "RB":
        return ("""AVG(carries) AS avg_carries, AVG(rushing_yards) AS avg_rushing_yards, AVG(rushing_tds) AS avg_rushing_tds, 
AVG(rushing_fumbles) AS avg_rushing_fumbles, AVG(rushing_fumbles_lost) AS avg_rushing_fumbles_lost, 
AVG(rushing_first_downs) AS avg_rushing_first_downs, AVG(rushing_epa) AS avg_rushing_epa, 
AVG(rushing_2pt_conversions) AS avg_rushing_2pt_conversions, AVG(receptions) AS avg_receptions, 
AVG(targets) AS avg_targets, AVG(receiving_yards) AS avg_receiving_yards, AVG(receiving_tds) AS avg_receiving_tds, 
AVG(receiving_fumbles) AS avg_receiving_fumbles, AVG(receiving_fumbles_lost) AS avg_receiving_fumbles_lost, 
AVG(receiving_air_yards) AS avg_receiving_air_yards, AVG(receiving_yards_after_catch) AS avg_receiving_yards_after_catch, 
AVG(receiving_first_downs) AS avg_receiving_first_downs, AVG(receiving_epa) AS avg_receiving_epa, 
AVG(receiving_2pt_conversions) AS avg_receiving_2pt_conversions, AVG(racr) AS avg_racr, 
AVG(target_share) AS avg_target_share, AVG(air_yards_share) AS avg_air_yards_share, 
AVG(wopr) AS avg_wopr, AVG(fantasy_points) AS avg_fantasy_points, 
AVG(fantasy_points_ppr) AS avg_fantasy_points_ppr, AVG(age) AS avg_age""")
    elif position == "WR" or "TE":
        return("""AVG(receptions) AS avg_receptions, AVG(targets) AS avg_targets, AVG(receiving_yards) AS avg_receiving_yards, 
AVG(receiving_tds) AS avg_receiving_tds, AVG(receiving_fumbles) AS avg_receiving_fumbles, 
AVG(receiving_fumbles_lost) AS avg_receiving_fumbles_lost, AVG(receiving_air_yards) AS avg_receiving_air_yards, 
AVG(receiving_yards_after_catch) AS avg_receiving_yards_after_catch, AVG(receiving_first_downs) AS avg_receiving_first_downs, 
AVG(receiving_epa) AS avg_receiving_epa, AVG(receiving_2pt_conversions) AS avg_receiving_2pt_conversions, 
AVG(racr) AS avg_racr, AVG(target_share) AS avg_target_share, AVG(air_yards_share) AS avg_air_yards_share, 
AVG(wopr) AS avg_wopr, AVG(carries) AS avg_carries, AVG(rushing_yards) AS avg_rushing_yards, 
AVG(rushing_tds) AS avg_rushing_tds, AVG(rushing_fumbles) AS avg_rushing_fumbles, 
AVG(rushing_fumbles_lost) AS avg_rushing_fumbles_lost, AVG(rushing_first_downs) AS avg_rushing_first_downs, 
AVG(rushing_epa) AS avg_rushing_epa, AVG(rushing_2pt_conversions) AS avg_rushing_2pt_conversions, 
AVG(fantasy_points) AS avg_fantasy_points, AVG(fantasy_points_ppr) AS avg_fantasy_points_ppr, AVG(age) AS avg_age""")
    elif position == "K" or "P":
        return("""AVG(special_team_tds) AS avg_special_team_tds, AVG(fantasy_points) AS avg_fantasy_points, AVG(fantasy_points_ppr) AS avg_fantasy_points_ppr, AVG(age) AS avg_age""")
    else:
        return ""
    
def get_simple_position_stats(position):
    if position == "QB":
        return ("""SUM(passing_yards) AS sum_passing_yards,
        PERCENT_RANK() OVER (ORDER BY SUM(passing_yards) ASC) AS percent_rank""")
    elif position == "RB":
        return ("""SUM(rushing_yards) AS sum_rushing_yards,
        PERCENT_RANK() OVER (ORDER BY SUM(rushing_yards) ASC) AS percent_rank""")
    elif position == "WR" or "TE":
        return("""SUM(receiving_yards) AS sum_receiving_yards,
        PERCENT_RANK() OVER (ORDER BY SUM(receiving_yards) ASC) AS percent_rank""")
    elif position == "K" or "P":
        return("""SUM(special_team_tds) AS sum_special_team_tds,
        PERCENT_RANK() OVER (ORDER BY SUM(special_team_tds) ASC) AS percent_rank""")
    else:
        return ""