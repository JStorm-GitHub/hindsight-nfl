import streamlit as st
from utils.data_loader import load_players, load_trades
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from data.team_list import get_team_logos, get_team_colors, get_team_name_map
from utils.data_loader import load_players, load_trades, get_yearly_player_stats, get_career_player_stats, get_cut_trades, get_free_agency_trades, get_acquired_trades, get_injuries_trades, get_win_loss
from app import find_valid_trades,calculate_trade_value

players = load_players()
trades = load_trades()

st.set_page_config(
    page_title="NFL Trade Search",
    page_icon="🏈",
    layout="wide"
)
            # <div class="date">{date}</div>
            # <div class="button-line">
            #     <img src="{teamLogo1}" class="button-image">
            #     <h4>{team1}' trade score: {team1Value}</h4>
            #     <span>{trade1}</span>
            # </div>
            # <div class="button-line">
            #     <img src="{teamLogo2}" class="button-image">
            #     <h4>{team2}' trade score: {team2Value}</h4>
            #     <span>{trade2}</span>
            # </div>

def clickable_link(date, trade1, trade2, url, teamLogo1, teamLogo2, team1Value, team2Value,team1,team2):
    """Creates a styled hyperlink that looks like a button."""
    st.markdown(
        f"""
        <a href="{url}" target="_self" class="custom-button">
            <div class="trade-container">
                <div class="button-line">
                    <img src="{teamLogo1}" class="button-image">
                    <h4>{team1}' trade score: {team1Value}</h4>
                    <span>{trade1}</span>
                </div>
                <div class="button-line">
                    <img src="{teamLogo2}" class="button-image">
                    <h4>{team2}' trade score: {team2Value}</h4>
                    <span>{trade2}</span>
                </div>
            </div>
        </a>
        <style>
        .custom-button {{
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            text-align: left;
            text-decoration: none !important;
            background-color: #1E1E1E;
            color: #cdcdcd !important;
            border-radius: 5px;
            border: 2px solid #444444;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
            margin-bottom: 10px;
        }}
        .custom-button:hover {{
            background-color: #3A3A3A;
        }}
        .trade-container {{
            display: flex;
            flex-direction: column;
            align-items: stretch; 
            gap: 10px; 
            max-width: 100%; 
        }}
        .button-image {{
            width:40px;
            height:40px;
            object-fit: cover;
            margin-right:20px;
        }}
        .button-line {{
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }}
        .date {{
            font-size: 22px;
            font-weight: bold;
            color: #cdcdcd;
            margin-bottom: 10px;
        }}
        h4 {{
            margin: 0;
            font-size: 16px;
            flex: 1; 
            text-align: center;
        }}
        span {{
            flex: 1; 
            text-align: right;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
def pull_trade_value(index, performance, filtered_trades):
    # pulls trade scores at a given index
    trade = filtered_trades.loc[int(index)]

    player_match_list1 = trade["player_matches1"]
    player_match_list2 = trade["player_matches2"]

    draft_match_list1 = trade["draft_matches1"]
    draft_match_list2 = trade["draft_matches2"]

    team1_list = player_match_list1 + draft_match_list1
    team2_list = player_match_list2 + draft_match_list2

    def avg_match_list(player_match_list):
        total_sum = 0  
        count = len(player_match_list) if player_match_list else 1  
        for player_name in player_match_list:
            player_data = performance[performance['name'] == player_name]
            if not player_data.empty:
                total_sum += player_data["win_weighted"].sum()
        return total_sum / count  
    
    # Compute per-team impact
    team1_value = avg_match_list(team1_list)  
    team2_value = avg_match_list(team2_list)  

    return team1_value, team2_value  


def show_trade_comp_page(index,date,team1,team2,tscore1,tscore2):
    # gets called when trade query parameters are set. splits up trade into rows for player_page
    
    if st.button("Back to search"):
        st.query_params.clear()
        st.rerun()
    
    st.subheader(date)

    filtered_trades = find_valid_trades(trades)

    trade = filtered_trades.loc[int(index)]

    draft_match_list1 = trade["draft_matches1"]
    draft_match_list2 = trade["draft_matches2"]

    player_match_list1 = trade["player_matches1"]
    player_match_list2 = trade["player_matches2"]

    def show_draft_list(draft_match_list):
        for draft_number,player_name in draft_match_list:
            player_data = players[(players['name'] == player_name) & (players['draft_position'] == int(draft_number))]
            if not player_data.empty:
                player_page(player_data.iloc[0])

    def show_player_list(player_match_list):
        for player_name in player_match_list:
            player_data = players[(players['name'] == player_name)]
            if not player_data.empty:
                player_page(player_data.iloc[0])
                
    col1,col2 = st.columns(2)
    with col1:
        st.subheader(f"Trade score for the {team1}: {tscore1}")
        st.divider()
        show_draft_list(draft_match_list1)
        show_player_list(player_match_list1)
    with col2:
        st.subheader(f"Trade score for the {team2}: {tscore2}")
        st.divider()
        show_draft_list(draft_match_list2)
        show_player_list(player_match_list2)


def player_page(player_data):
    ### Gets called per player in drafted and normal player list. 
    player_name = player_data["name"]
    player_id = player_data["player_id"]
        

    col1, col2, col3= st.columns([1,3,3], gap="small")
    with col1:
        st.image(player_data['headshot_url'],use_container_width=False,width=200)
    with col2:
        st.subheader("Player profile:")
        st.title(f"{player_name} ({player_data['position']})")
    with col3:
        st.subheader("Player Information")
        st.write(f"Born: {player_data['birthdate']}")
        st.write(f"College: {player_data['college']}")
        st.write(f"Draft: Round {player_data['draft_position']} ({player_data['draft_year']})")
    
    stats = get_yearly_player_stats(player_id)

    years = stats['season'].tolist()

    options = ["Career"] + years + ["Custom"]

    selected_year = st.segmented_control(
        "Select Year",
        options=options,
        format_func=lambda x: str(x),
        selection_mode="single",
        default="Career",
        key = f"{player_name}"
    )

    # Set up trade data
    plot_stats = get_career_player_stats(player_id)
    plot_stats["gameday"] = pd.to_datetime(plot_stats["gameday"])

    cut_trades = get_cut_trades(player_id)
    cut_trades['transaction_date'] = pd.to_datetime(cut_trades["transaction_date"])

    free_agency = get_free_agency_trades(player_id)
    free_agency['transaction_date'] = pd.to_datetime(free_agency["transaction_date"])

    acquired_trades = get_acquired_trades(player_id)
    acquired_trades['transaction_date'] = pd.to_datetime(acquired_trades["transaction_date"])

    injuries = get_injuries_trades(player_id)
    injuries['transaction_date'] = pd.to_datetime(injuries["transaction_date"])

    # Date ranges are shifted to follow the NFL season
    if selected_year in years:
        start_date = pd.Timestamp(f"{selected_year}-09-01")
        end_date = pd.Timestamp(f"{selected_year + 1}-09-01")
        plot_stats = plot_stats[plot_stats['season'] == selected_year]
        cut_trades = cut_trades[(cut_trades['transaction_date'] >= start_date) & (cut_trades['transaction_date'] < end_date)]
        free_agency = free_agency[(free_agency['transaction_date'] >= start_date) & (free_agency['transaction_date'] < end_date)]
        acquired_trades = acquired_trades[(acquired_trades['transaction_date'] >= start_date) & (acquired_trades['transaction_date'] < end_date)]
        injuries = injuries[(injuries['transaction_date'] >= start_date) & (injuries['transaction_date'] < end_date)]
        st.subheader(f"{selected_year} Statistics")
    elif selected_year == "Career":
        st.subheader(f"Career Statistics")
    elif selected_year == "Custom":
        st.subheader(f"Custom Statistics")  

    show_stats = True

    # to avoid overloading output more position-specific stats are used
    if player_data['position']== "QB":
        selected_stat = st.selectbox(
            f"Choose one of {player_name}'s QB stat to observe",
            ("completions", "attempts", "passing_yards", "passing_tds", "interceptions", "sacks", "sack_yards", "sack_fumbles", "sack_fumbles_lost",
             "passing_air_yards", "passing_yards_after_catch", "passing_first_downs", "passing_epa", "passing_2pt_conversions", "pacr", "dakota", 
             "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions",
             "fantasy_points", "fantasy_points_ppr","age")
        )
    elif player_data['position'] == "RB":
        selected_stat = st.selectbox(
            f"Choose one of {player_name}'s RB stat to observe",
            ("carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", 
             "receptions","targets", "receiving_yards", "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", 
             "receiving_air_yards", "receiving_yards_after_catch", "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", 
             "racr", "target_share", "air_yards_share", "wopr", 
             "fantasy_points", "fantasy_points_ppr","age")
        )
    elif player_data['position'] == "WR" or player_data['position'] == "TE":
        selected_stat = st.selectbox(
            f"Choose one of {player_name}'s WR/TE stat to observe",
            ("receptions", "targets", "receiving_yards", "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", 
             "receiving_air_yards", "receiving_yards_after_catch", "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", 
             "racr", "target_share", "air_yards_share", "wopr", 
             "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", 
             "fantasy_points", "fantasy_points_ppr","age")
    )
    elif player_data['position'] == "K" or player_data['position'] == "P":
        selected_stat = st.selectbox(
            f"Choose one of {player_name}'s K/P stat to observe",
            ("special_teams_tds", 
             "fantasy_points", "fantasy_points_ppr","age")
    )
    else:
        st.write("No stats available for this position. Defensive statistics coming soon!")
        show_stats = False
    
    if show_stats: 
        team_colors = get_team_colors()
        
        plot_stats[f"Average_{selected_stat}"] = plot_stats[selected_stat].rolling(window=5, min_periods=1).mean()
        fig = px.line(plot_stats, x="gameday", y=f"{selected_stat}", title=f"{selected_stat} Over Time")
        
        # uses the color map to add a scatterplot of raw, per-game statistics
        for team in plot_stats['team'].unique():
            team_data = plot_stats[plot_stats['team'] == team]
            fig.add_trace(go.Scatter(
                x=team_data["gameday"],
                y=team_data[f"{selected_stat}"],
                mode='markers',
                marker=dict(size=8, color=team_colors.get(team, '#000000')),
                text=team_data['team'],
                hoverinfo="text+x+y",
                showlegend=False  
            ))
        # dates of major career shifts, injuries, free agency, etc
        for _, row in cut_trades.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["transaction_date"], row["transaction_date"]],
                y=[0], 
                mode="markers+text",
                marker=dict(size = 10, color="red", symbol="circle"),
                name = f"CUT from {row["team"]} - {row['transaction_date'].strftime('%Y-%m-%d')}",
                opacity = 0.75
            ))
        for _, row in free_agency.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["transaction_date"], row["transaction_date"]],
                y=[0], 
                mode="markers",
                marker=dict(size = 10, color="blue", symbol="circle"),
                name=f"FREE AGENT - {row['transaction_date'].strftime('%Y-%m-%d')}",  
                opacity=0.75
            ))
        for _, row in acquired_trades.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["transaction_date"], row["transaction_date"]],
                y=[0],  
                mode="markers",
                marker=dict(size = 10, color="green", symbol="circle"),
                name=f"ACQUIRED by {row["team"]} - {row['transaction_date'].strftime('%Y-%m-%d')}",  
                opacity=0.75
            ))
        for _, row in injuries.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["transaction_date"], row["transaction_date"]],
                y=[0], 
                mode="markers",
                marker=dict(size = 10, color="black", symbol="circle"),
                name=f"INJURED - {row['transaction_date'].strftime('%Y-%m-%d')}",  
                opacity=0.75
            ))
            
        fig.update_layout(showlegend=True, legend = {'traceorder':'normal'})
        
        st.plotly_chart(fig)



def trade_main():


    # copies formatted valid trade
    filtered_trades = find_valid_trades(trades)
    #### fix this
    filtered_trades["draft_matches1"] = filtered_trades["draft_matches1"].apply(lambda x: [name for _, name in x] if isinstance(x, list) else [])
    filtered_trades["draft_matches2"] = filtered_trades["draft_matches2"].apply(lambda x: [name for _, name in x] if isinstance(x, list) else [])

    performance_value = calculate_trade_value()

    st.sidebar.page_link('app.py', label='Home')
    st.sidebar.page_link('pages/trade_search.py', label='Trade Search')
    st.sidebar.page_link('pages/player_search.py', label='Player Search')
    st.sidebar.page_link('pages/about.py', label='About')

    st.title("NFL Trade Search")

    trade_dates = filtered_trades['date']

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.metric("Total Players", len(players))
    # with col2:
    #     st.metric("Total Trades", len(filtered_trades))
    # with col3:
    #     earliest_trade = pd.to_datetime(trade_dates).min().year if len(trades) > 0 else "No trades"
    #     st.metric("Earliest Trade", str(earliest_trade))

    ITEMS_PER_PAGE = 5

    query_params = st.query_params
    selected_search = query_params.get("search_name", "")
    selected_category = query_params.get("trade_date", "All")
    page_number = int(query_params.get("pg",1))

    search_name = st.text_input("Search by name:", value=selected_search)
    category_options = ["All"] + list(trade_dates.dt.year.unique())
    trade_year_filter = st.selectbox("Filter by draft year:", category_options, index=category_options.index(selected_category))

    if search_name != selected_search:
        query_params["search_name"] = search_name  

    if trade_year_filter != selected_category:
        query_params["date"] = trade_year_filter
    
    if search_name:
        filtered_trades = filtered_trades[
            filtered_trades['acquired_team1'].str.contains(search_name, case=False, na=False) |
            filtered_trades['acquired_team2'].str.contains(search_name, case=False, na=False) |
            filtered_trades['team1'].str.contains(search_name, case=False, na=False) |
            filtered_trades['team2'].str.contains(search_name, case=False, na=False) 
        ]

    if trade_year_filter != "All":
        filtered_trades = filtered_trades[trade_dates.dt.year == trade_year_filter]

    total_pages = (len(filtered_trades) - 1) // ITEMS_PER_PAGE + 1
    start_idx = (page_number - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_data = filtered_trades.iloc[start_idx:end_idx]

    if len(filtered_trades)>0:
        for index, row in paginated_data.iterrows():
            date = row["date"].strftime("%B %-d, %Y")
            team_logos = get_team_logos()
            team1 = row["team1"]
            team2 = row["team2"]
            team1Logo = team_logos.get(team1, "images/default.png")
            team2Logo = team_logos.get(team2, "images/default.png")
            team1Value, team2Value = pull_trade_value(index,performance_value,filtered_trades)
            team1Value = int(team1Value)
            team2Value = int(team2Value)
            
            clickable_link(f"{date}",
                           f"{team1} acquire {row["acquired_team1"]}", 
                           f"{team2} acquire {row["acquired_team2"]}", 
                           f"?index={index}&date={row["date"].year}&team1={row["team1"]}&team2={row["team2"]}&tscore1={team1Value}&tscore2={team2Value}", 
                           team1Logo,team2Logo,team1Value,team2Value,team1,team2)
    else:
        st.write("No players found matching your criteria.")

    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if page_number > 1:
            if st.button("Prev"):
                query_params["pg"] = page_number - 1
                st.rerun()
    with col3:
        if page_number < total_pages:
            if st.button("Next"):
                query_params["pg"] = page_number + 1
                st.rerun()

    st.divider()

params = st.query_params
index = params.get("index")
transaction_date = params.get("date")
team1 = params.get("team1")
team2 = params.get("team2")
tscore1 = params.get("tscore1")
tscore2 = params.get("tscore2")

if index:
    show_trade_comp_page(index,transaction_date,team1,team2,tscore1,tscore2)
else:
    trade_main()