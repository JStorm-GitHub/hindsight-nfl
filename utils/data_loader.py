from sqlalchemy import create_engine
import pandas as pd

NFL_DATA = "sqlite:///data/nfl_merged.db"

NFL_TRADE = "sqlite:///data/trade_data.db"


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


    return df


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


def get_yearly_player_stats(player_id):
    
    engine = create_engine(NFL_DATA)
    query = """
    SELECT season, recent_team as team, SUM(completions) as completions,SUM(attempts) as attempts,SUM(passing_yards) as passing_yards,SUM(passing_tds) as passing_tds,SUM(interceptions) as interceptions,SUM(sacks) as sacks,SUM(sack_yards) as sack_yards,SUM(sack_fumbles) as sack_fumbles,SUM(sack_fumbles_lost) as sack_fumbles_lost
    FROM nfl_data
    WHERE player_id = :_id 
    GROUP BY season, player_id
    ORDER BY player_display_name asc
"""
    data = {'_id':player_id}
    df = pd.read_sql_query(query, engine, params=data)

    return df


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


def get_player_trades(player_id):

    engine = create_engine(NFL_TRADE)
    query = """
    SELECT player_id, player_name, transaction_date, team, status, notes
    FROM transactions
    WHERE player_id = :_id
    """
    data = {'_id':player_id}
    df = pd.read_sql_query(query, engine, params=data)
    return df

def get_weekly_per_year_passing_player_stats(player_id,season):
    engine = create_engine(NFL_DATA)
    query = """
    SELECT season, week, gameday, recent_team as team, completions, attempts, passing_yards, passing_tds, interceptions, sacks, sack_yards, sack_fumbles, sack_fumbles_lost
    FROM nfl_data
    WHERE player_id = :_id AND season = :_season
    ORDER BY season asc, week asc
    """
    data = {'_id':player_id, '_season':season}
    df = pd.read_sql_query(query, engine, params=data)
    return df

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

def get_free_agency_trades(player_id):
    engine = create_engine(NFL_TRADE)
    query = """
    SELECT * FROM transactions 
WHERE (LOWER(notes) LIKE '%free agent%'
   OR LOWER(notes) LIKE '%contract expired%'
   OR LOWER(notes) LIKE '%opted out%')
   AND player_id = :_id;
    """
    data = {'_id':player_id, }
    df = pd.read_sql_query(query, engine, params=data)
    return df

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