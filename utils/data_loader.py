from sqlalchemy import create_engine
from data.all_position_stats import get_bulk_position_stats, get_simple_position_stats
from data.team_list import get_team_name_replacement_map
import pandas as pd

NFL_DATA = "sqlite:///data/nfl_merged.db"

NFL_TRADE = "sqlite:///data/trade_data.db"

# this loads all unique trades
def load_trades():
    engine = create_engine(NFL_TRADE)
    query = """
            WITH NumberedRows AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY transaction_date ASC) AS row_num
    FROM transactions
	WHERE (LOWER(notes) LIKE 'trade%')
),
MergedRows AS (
    SELECT 
        n1.transaction_date,
        n1.team AS team1, 
        n1.acquired AS acquired1, 
        n1.relinquished AS relinquished1, 
        n1.notes AS notes1,
        n2.team AS team2, 
        n2.acquired AS acquired2, 
        n2.relinquished AS relinquished2, 
        n2.notes AS notes2
    FROM NumberedRows n1
    LEFT JOIN NumberedRows n2
    ON n1.row_num = n2.row_num - 1
    WHERE n1.team < n2.team
    AND LOWER(n1.notes) LIKE '%' || LOWER(n2.team) || '%'
)
SELECT transaction_date AS date, team1,acquired1 AS acquired_team1,team2,acquired2 AS acquired_team2 FROM MergedRows
ORDER BY transaction_date;
"""
    df = pd.read_sql_query(query,engine)
    df = df.drop_duplicates().reset_index(drop=True)
    df['date'] = pd.to_datetime(df['date'])

    replacement_map = get_team_name_replacement_map()

    df["team1"] = df["team1"].replace(replacement_map)
    df["team2"] = df["team2"].replace(replacement_map)
    return df

# this loads essential player data
def load_players():
    engine = create_engine(NFL_DATA)
    query = """
    WITH data_table AS (
    SELECT 
        player_id,
        headshot_url, 
		player_display_name as name,
		birth_date as birthdate,
		college,
		CAST(entry_year AS INTEGER) as draft_year,
        season,
        position,
		CAST(draft_number AS INTEGER) as draft_position,
        ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY season DESC) AS rn
    FROM nfl_data
)
SELECT player_id, name, headshot_url, season, birthdate, college, draft_year, draft_position,position
FROM data_table
WHERE rn = 1
ORDER BY name ASC
"""

    df = pd.read_sql_query(query, engine)
    df['headshot_url'] = df['headshot_url'].fillna("https://static.www.nfl.com/image/private/f_auto,q_auto/league/tvzbhead7hjhqpcbilgc")

    return df

# this returns the 
def get_career_seasons(player_id):
    
    engine = create_engine(NFL_DATA)
    query = """
        SELECT season
    FROM nfl_data
    WHERE player_id = :_id
    GROUP BY season
    ORDER BY player_display_name asc
"""
    data = {'_id':player_id}
    df = pd.read_sql_query(query, engine, params=data)

    return df

# this returns all stats for any given player
def get_career_player_stats(player_id):

    engine = create_engine(NFL_DATA)
    query = """
    SELECT 
        season, week, gameday, recent_team as team, 
        completions, attempts, passing_yards, passing_tds, 
        interceptions, sacks, sack_yards, sack_fumbles, sack_fumbles_lost, 
        age,
        passing_air_yards, passing_yards_after_catch, passing_first_downs, passing_epa, passing_2pt_conversions, 
        pacr, dakota,
        carries, rushing_yards, rushing_tds, rushing_fumbles, rushing_fumbles_lost, rushing_first_downs, rushing_epa, rushing_2pt_conversions,
        fantasy_points, fantasy_points_ppr, special_teams_tds, 
        receptions, targets, receiving_yards, receiving_tds, 
        receiving_fumbles, receiving_fumbles_lost, receiving_air_yards, receiving_yards_after_catch, receiving_first_downs, receiving_epa,receiving_2pt_conversions,
        racr, wopr
    FROM nfl_data
    WHERE player_id = :_id
    ORDER BY season asc, week asc
    """
    data = {'_id':player_id}
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this gets all "fired" like reports for a player
def get_cut_trades(player_id):
    engine = create_engine(NFL_TRADE)
    query = """
    SELECT * FROM transactions 
WHERE (LOWER(notes) LIKE '%released%'
   OR LOWER(notes) LIKE '%waived%'
   OR LOWER(notes) LIKE '%traded%'
   OR LOWER(notes) LIKE '%terminated%'
   OR LOWER(notes) LIKE '%cut%'
   )
   AND player_id = :_id;
    """
    data = {'_id':player_id, }
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this gets all "free agency" like reports for a player
def get_free_agency_trades(player_id):
    engine = create_engine(NFL_TRADE)
    query = """
    SELECT * FROM transactions 
WHERE (LOWER(notes) LIKE '%free agent%')
   AND player_id = :_id;
    """
    data = {'_id':player_id, }
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this gets all "draft" like reports for a player
def get_acquired_trades(player_id):
    engine = create_engine(NFL_TRADE)
    query = """
    SELECT * FROM transactions 
WHERE (LOWER(notes) LIKE '%draft%')
   AND player_id = :_id;
    """
    data = {'_id':player_id, }
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this gets all "injury" like reports for a player
def get_injuries_trades(player_id):
    engine = create_engine(NFL_TRADE)
    query = """
    SELECT * FROM transactions 
WHERE (LOWER(notes) LIKE '%injury%'
   OR LOWER(notes) LIKE '% IR %'
   OR LOWER(notes) LIKE '%out indefinitely%'
   OR LOWER(notes) LIKE '%returned to lineup%')
   AND player_id = :_id;
    """
    data = {'_id':player_id, }
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this gets the win/loss ratio of all players
def get_win_loss():
    engine = create_engine(NFL_DATA)
    query = """
    SELECT 
        season, week, gameday, recent_team AS team, player_display_name AS name, player_id, 
        result, CAST(draft_number AS INTEGER) as draft_position, position,
		CASE
			WHEN result > 0 THEN 1
			ELSE 0
		END AS win
    FROM nfl_data
    ORDER BY season asc, week asc
    """
    df = pd.read_sql_query(query, engine)
    return df

### hindsight data

# this returns a player's average full stats for their entire career
def get_player_full_career_average(player_id,position):
    position_stats = get_bulk_position_stats(position)
    engine = create_engine(NFL_DATA)
    query = f"""
    SELECT 
        player_id,
        {position_stats},
        MIN(gameday) AS start_date, 
        MAX(gameday) AS end_date,
        MIN(season) AS start_season,
		MAX(season) AS end_season
    FROM nfl_data
    WHERE player_id = :_player_id
    GROUP BY player_id
    """
    data = {'_player_id':player_id}
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this returns the average stats for a given position entire career
def get_league_per_game_average(position, start_date, end_date):
    position_stats = get_bulk_position_stats(position)
    engine = create_engine(NFL_DATA)
    query = f"""
    SELECT 
        position,
	    gameday,
        {position_stats}
    FROM nfl_data
    WHERE position = :_position AND gameday BETWEEN :_start_date AND :_end_date
    GROUP BY position, gameday
    ORDER BY gameday ASC
    """
    data = {'_position':position, '_start_date':start_date, '_end_date':end_date}
    df = pd.read_sql_query(query, engine, params=data)
    return df

# this gets the ranked performance of a player during their tenure at all teams they played on.
def get_ranked_players_per_team(position):
    position_stats = get_simple_position_stats(position)
    engine = create_engine(NFL_DATA)
    query = f"""
    WITH qb_ranks AS (
        SELECT 
            player_id,
            gameday,
            player_display_name AS name,
            recent_team AS team,
            {position_stats}
        FROM nfl_data
        WHERE position = :_position
        GROUP BY player_id, player_display_name, recent_team
    )
    SELECT 
        p.player_id,
        p.name,
        p.team,
        q.percent_rank
    FROM (
        SELECT DISTINCT player_id, player_display_name AS name, recent_team AS team
        FROM nfl_data
    ) p
    LEFT JOIN qb_ranks q 
        ON p.player_id = q.player_id 
        AND p.team = q.team
    ORDER BY q.gameday ASC;
    """
    data = {'_position':position}
    df = pd.read_sql_query(query, engine, params=data)
    df = df.dropna()
    return df