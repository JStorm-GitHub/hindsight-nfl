import streamlit as st
import pandas as pd
from utils.data_loader import load_players, load_trades,get_yearly_player_stats,get_career_player_stats,get_cut_trades,get_free_agency_trades,get_acquired_trades,get_injuries_trades
import plotly.express as px
import plotly.graph_objects as go
from data.team_list import get_team_colors


players = load_players()
trades = load_trades()


def clickable_link(label, url,image_url):
    """Creates a styled hyperlink that looks like a button."""
    st.markdown(
        f"""
        <a href="{url}" target="_self" class="custom-button">
        <img src="{image_url}" class="button-image">
        <span>{label}</span>
        </a>
        <style>
        .custom-button {{
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            text-align: left;
            text-decoration: none;
            background-color: #2d425d;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
            margin-bottom: 10px;
        }}
        .custom-button:hover {{
            background-color: #005f73;
        }}
        .button-image {{
            width:100px;
            height:100px;
            border-radius: 50%;
            object-fit: cover;
            background-color: #d9ceca;
            margin-right:20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def show_player_page(player_id,player_name):
    st.set_page_config(
        page_title=f"{player_name} Profile",
        page_icon="🏈",
        layout="wide"
    )

    if st.button("Back to search"):
        st.query_params.clear()
        st.rerun()

    player_data = players[players['player_id'] == player_id].iloc[0]

    col1, col2, col3= st.columns([1,3,3], gap="small")
    with col1:
        st.image(player_data['headshot_url'],use_container_width=False,width=200)
    with col2:
        st.subheader("Player profile:")
        st.title(f"{player_name}")
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
        default="Career"
    )

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

    if player_data['position']== "QB":
        selected_stat = st.selectbox(
            "Choose a QB stat to observe",
            ("completions", "attempts", "passing_yards", "passing_tds", "interceptions", "sacks", "sack_yards", "sack_fumbles", "sack_fumbles_lost",
             "passing_air_yards", "passing_yards_after_catch", "passing_first_downs", "passing_epa", "passing_2pt_conversions", "pacr", "dakota", 
             "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions",
             "fantasy_points", "fantasy_points_ppr","age")
        )
    elif player_data['position'] == "RB":
        selected_stat = st.selectbox(
            "Choose a RB stat to observe",
            ("carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", 
             "receptions","targets", "receiving_yards", "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", 
             "receiving_air_yards", "receiving_yards_after_catch", "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", 
             "racr", "target_share", "air_yards_share", "wopr", 
             "fantasy_points", "fantasy_points_ppr","age")
        )
    elif player_data['position'] == "WR" or player_data['position'] == "TE":
        selected_stat = st.selectbox(
            "Choose a WR/TE stat to observe",
            ("receptions", "targets", "receiving_yards", "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", 
             "receiving_air_yards", "receiving_yards_after_catch", "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", 
             "racr", "target_share", "air_yards_share", "wopr", 
             "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", 
             "fantasy_points", "fantasy_points_ppr","age")
    )
    elif player_data['position'] == "K" or player_data['position'] == "P":
        selected_stat = st.selectbox(
            "Choose a K/P stat to observe",
            ("special_teams_tds", 
             "fantasy_points", "fantasy_points_ppr","age")
    )
    else:
        st.write("No stats available for this position. Defensive statistics coming soon!")
        show_stats = False
    
    if show_stats: 

        team_colors = get_team_colors()

        plot_stats[f"Average_{selected_stat}"] = plot_stats[selected_stat].rolling(window=5, min_periods=1).mean()

        fig = px.line(plot_stats, x="gameday", y=f"Average_{selected_stat}", title=f"{selected_stat} Over Time")
        
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
        fig.update_layout(showlegend=True)

        st.plotly_chart(fig)


def show_search_page():
    st.set_page_config(
        page_title="NFL Player Search",
        page_icon="🏈",
        layout="centered"
    )

    # Load data
    st.sidebar.page_link('app.py', label='Trades')
    st.sidebar.page_link('pages/player_search.py', label='Player Search')
    st.sidebar.page_link('pages/about.py', label='About')
    st.title("Player Search")

    if "page" not in st.session_state:
        st.session_state.page = 1

    ITEMS_PER_PAGE = 9

    # Query parameters handling
    query_params = st.query_params
    selected_search = query_params.get("search_name", "")
    selected_category = query_params.get("draft_year", "All")


    search_name = st.text_input("Search by name:", value=selected_search)
    category_options = ["All"] + list(players["draft_year"].unique())
    draft_year_filter = st.selectbox("Filter by draft year:", category_options, index=category_options.index(selected_category))

    if search_name != selected_search:
        st.query_params["search_name"] = search_name  

    if draft_year_filter != selected_category:
        st.query_params["draft_year"] = draft_year_filter

    # Filter data
    filtered_players = players.copy()

    
    if search_name:
        filtered_players = filtered_players[
            filtered_players['name'].str.contains(search_name, case=False, na=False)
        ]

    if draft_year_filter != "All":
        filtered_players = filtered_players[filtered_players["draft_year"] == draft_year_filter]

    # Pagination logic
    total_pages = (len(filtered_players) - 1) // ITEMS_PER_PAGE + 1
    start_idx = (st.session_state.page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_data = filtered_players.iloc[start_idx:end_idx]

    # Display results
    st.write(f"Showing {len(paginated_data)} of {len(filtered_players)} results")

    if len(filtered_players)>0:
        for _, row in paginated_data.iterrows():
            clickable_link(f"{row["name"]} ({row['position']}) - Drafted {row["draft_year"]}", f"?selected_id={row["player_id"]}&selected_name={row["name"]}&search={search_name}&category={draft_year_filter}",row['headshot_url'])
    else:
        st.write("No players found matching your criteria.")

    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.session_state.page > 1:
            if st.button("Prev"):
                st.session_state.page -= 1
                st.rerun()
    with col3:
        if st.session_state.page < total_pages:
            if st.button("Next"):
                st.session_state.page += 1
                st.rerun()
    

params = st.query_params
selected_id = params.get("selected_id")
selected_name = params.get("selected_name")
search_query = params.get("search", "")
category = params.get("category", "")

if selected_id:
    show_player_page(selected_id,selected_name)
else:
    show_search_page()
