import streamlit as st
from utils.data_loader import load_players, load_trades
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from data.team_list import get_team_logos, get_team_colors, get_team_name_map
from utils.data_loader import load_players, load_trades, get_yearly_player_stats, get_career_player_stats, get_cut_trades, get_free_agency_trades, get_acquired_trades, get_injuries_trades, get_win_loss


players = load_players()
trades = load_trades()


### These functions are initialized on startup and cached
@st.cache_data
def find_valid_trades(trades_df):
    # formats trade database to filter out player names, draft position, etc.

    # Drop NaN draft positions early
    valid_draft_players = players.dropna(subset=['draft_position']).copy()

    # Ensure draft_position is properly formatted
    valid_draft_players['draft_position'] = valid_draft_players['draft_position'].astype(str).str.replace('.0$', '', regex=True)

    # Patterns for extraction
    draft_pattern = re.compile(r"#(\d+)-([\w\s'-]+)")
    player_pattern = re.compile(r"• (?:rights to )?([A-Za-z.'-]+(?: [A-Za-z.'-]+)*)")

    # Function to extract draft/player matches
    def extract_matches(text, pattern):
        if isinstance(text, list):
            text = " ".join(map(str, text))  # Convert list to string
        return pattern.findall(text) if isinstance(text, str) else []

    # Apply regex extraction to entire DataFrame
    trades_df["draft_matches1"] = trades_df["acquired_team1"].apply(lambda x: extract_matches(x, draft_pattern))
    trades_df["draft_matches2"] = trades_df["acquired_team2"].apply(lambda x: extract_matches(x, draft_pattern))

    trades_df["player_matches1"] = trades_df["acquired_team1"].apply(lambda x: extract_matches(x, player_pattern))
    trades_df["player_matches2"] = trades_df["acquired_team2"].apply(lambda x: extract_matches(x, player_pattern))

    # Function to check valid matches
    def check_valid_matches(draft_matches, player_matches):
        draft_df = pd.DataFrame(draft_matches, columns=["draft_position", "name"])
        player_df = pd.DataFrame(player_matches, columns=["name"])

        draft_valid = not draft_df.empty and not valid_draft_players.merge(draft_df, on=["draft_position", "name"], how="inner").empty
        player_valid = not player_df.empty and not players.merge(player_df, on=["name"], how="inner").empty

        return draft_valid or player_valid  # At least one valid match

    # Apply validation check across all rows
    trades_df["team1_valid"] = trades_df.apply(lambda row: check_valid_matches(row["draft_matches1"], row["player_matches1"]), axis=1)
    trades_df["team2_valid"] = trades_df.apply(lambda row: check_valid_matches(row["draft_matches2"], row["player_matches2"]), axis=1)

    # Filter only valid trades where both teams have valid assets
    valid_trades_df = trades_df[(trades_df["team1_valid"]) & (trades_df["team2_valid"])]

    # Drop temporary columns
    valid_trades_df = valid_trades_df.drop(columns=["team1_valid","team2_valid"])

    return valid_trades_df

@st.cache_data
def calculate_trade_value():
    # formulates trade score using weighing
    filtered_trades = find_valid_trades(trades)

    weekly_performance = get_win_loss()
    
    team_name_map = get_team_name_map()

    filtered_trades["team1"] = filtered_trades["team1"].map(team_name_map)
    filtered_trades["team2"] = filtered_trades["team2"].map(team_name_map)
    

    trades_team1 = filtered_trades.explode("player_matches1")[["team1", "player_matches1"]].rename(
        columns={"team1": "new_team", "player_matches1": "name"}
    )
    trades_team2 = filtered_trades.explode("player_matches2")[["team2", "player_matches2"]].rename(
        columns={"team2": "new_team", "player_matches2": "name"}
    )

    filtered_trades["draft_matches1"] = filtered_trades["draft_matches1"].apply(lambda x: [name for _, name in x] if isinstance(x, list) else [])

    # Explode into separate rows and rename columns
    draft_trades_team1 = filtered_trades.explode("draft_matches1")[["team1", "draft_matches1"]].rename(
        columns={"team1": "new_team", "draft_matches1": "name"}
    )

    # If you have draft_matches2 and need the same transformation:
    filtered_trades["draft_matches2"] = filtered_trades["draft_matches2"].apply(lambda x: [name for _, name in x] if isinstance(x, list) else [])

    draft_trades_team2 = filtered_trades.explode("draft_matches2")[["team2", "draft_matches2"]].rename(
        columns={"team2": "new_team", "draft_matches2": "name"}
    )

    trade_players = pd.concat([trades_team1, trades_team2,draft_trades_team1,draft_trades_team2]).dropna()

    performance_for_new_team = weekly_performance.merge(trade_players, on="name", how="inner")

    performance_for_new_team = performance_for_new_team[
        performance_for_new_team["team"] == performance_for_new_team["new_team"]
    ]

    # Assign weights to wins
    def assign_weight(week):
        if week < 18:  # Regular season
            return 1
        elif week < 20:  # Wild Card / Divisional
            return 3
        elif week == 20:  # Conference Championship
            return 5
        else:  # Super Bowl
            return 10

    performance_for_new_team["win_weighted"] = performance_for_new_team["win"] * performance_for_new_team["week"].apply(assign_weight)

    position_weights = {
        "QB": 1.5,  # Most impact
        "RB": 1.2,
        "WR": 1.2,
        "TE": 1.2,
        "OL": 1.0,  # Baseline
        "DL": 1.0,
        "LB": 1.0,
        "DB": 1.0,
        "K": 0.7,  # Less impact
        "P": 0.7,
    }
    
    performance_for_new_team["position_weight"] = performance_for_new_team["position"].map(position_weights).fillna(1.0)
    
    performance_for_new_team["win_weighted"] *= performance_for_new_team["position_weight"]

    performance_value_scores = performance_for_new_team.groupby(["name", "new_team"], as_index=False)["win_weighted"].sum()

    return performance_value_scores


st.set_page_config(
    page_title="NFL Trade Analysis",
    page_icon="🏈",
    layout="wide"
)

def main(): 
    filtered_trades = find_valid_trades(trades)
    trade_dates = filtered_trades['date']


    
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.page_link('app.py', label='Home')
    st.sidebar.page_link('pages/trade_search.py', label='Trade Search')
    st.sidebar.page_link('pages/player_search.py', label='Player Search')
    st.sidebar.page_link('pages/about.py', label='About')

    st.title("NFL Trade Analysis")
    st.write("Welcome to the NFL Trade Analysis platform!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Players", len(players))
    with col2:
        st.metric("Total Trades", len(filtered_trades))
    with col3:
        earliest_trade = pd.to_datetime(trade_dates).min().year if len(trades) > 0 else "No trades"
        st.metric("Earliest Trade", str(earliest_trade))


if __name__ == "__main__":
    main()