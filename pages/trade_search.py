import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.team_list import (get_team_logos,
                            get_team_colors,
                            get_short_to_long_team_abbreviation_map
                            )
from utils.data_loader import (load_players,
                               load_trades,
                               get_career_seasons,
                               get_career_player_stats,
                               get_league_per_game_average,
                               get_player_full_career_average,
                               get_ranked_players_per_team
                               )
from app import find_valid_trades, calculate_trade_value
import urllib.parse

st.set_page_config(
    page_title="Hindsight Trade Search",
    page_icon="🏈",
    layout="wide"
)

players = load_players()
trades = load_trades()


def clickable_link(trade1, trade2, url, teamLogo1, teamLogo2, team1Value,
                   team2Value, team1, team2):
    """Creates a styled hyperlink that looks like a button."""
    st.markdown(
        f"""
        <a href="{url}" target="_self" class="custom-button">
            <div class="trade-container">
                <div class="button-line">
                    <img src="{teamLogo1}" class="button-image">
                    <h4>{team1}' trade score: <span style="background-color:
                    #3b3c51; color: black; padding: 3px 6px; border-radius:
                    # 5px; border: 1px solid #21233b;">{team1Value}</span></h4>
                    <span>{trade1}</span>
                </div>
                <div class="button-line">
                    <img src="{teamLogo2}" class="button-image">
                    <h4>{team2}' trade score: <span style="background-color:
                    #3b3c51; color: black; padding: 3px 6px; border-radius:
                    # 5px; border: 1px solid #21233b;">{team2Value}</span></h4>
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


def pull_trade_value(index, performance, filtered_trades, team1, team2):
    # pulls trade scores at a given index
    trade = filtered_trades.loc[int(index)]

    draft_match_list1 = trade["draft_names1"]
    draft_match_list2 = trade["draft_names2"]

    player_match_list1 = trade["player_matches1"]
    player_match_list2 = trade["player_matches2"]

    team1_list = player_match_list1 + draft_match_list1
    team2_list = player_match_list2 + draft_match_list2

    def avg_match_list(player_match_list, team_name):
        total_sum = 0
        count = len(player_match_list) if player_match_list else 1
        win_weighted_list = []

        for player_name in player_match_list:
            player_data = performance[(performance['name'] == player_name) &
                                      (performance['new_team'] == team_name)]
            if not player_data.empty:
                win_weighted = player_data["win_weighted"].sum()
                total_sum += win_weighted
            else:
                win_weighted = 0
                total_sum += win_weighted
            win_weighted_list.append((player_name, win_weighted))

        return total_sum / count, win_weighted_list

    # Compute per-team impact
    team1_value, trade_score_list1 = avg_match_list(team1_list, team1)
    team2_value, trade_score_list2 = avg_match_list(team2_list, team2)

    return team1_value, team2_value, trade_score_list1, trade_score_list2


def show_trade_comp_page(index, page, date):
    # gets called when trade query parameters are set. splits up trade into
    # rows for player_page

    if st.button("Back to search"):
        st.query_params.clear()
        st.query_params.pg = page

        st.rerun()

    st.subheader(date)

    filtered_trades = find_valid_trades(trades)

    trade = filtered_trades.loc[int(index)]

    team1 = trade["team1"]
    team2 = trade["team2"]

    performance = calculate_trade_value()

    team_name_map = get_short_to_long_team_abbreviation_map()

    performance["new_team"] = performance["new_team"].map(team_name_map)

    tscore1, tscore2, trade_score_list1, trade_score_list2 = pull_trade_value(
        index, performance, filtered_trades, team1, team2)

    trade_score_list1 = dict(trade_score_list1)
    trade_score_list2 = dict(trade_score_list2)

    draft_match_list1 = trade["draft_matches1"]
    draft_match_list2 = trade["draft_matches2"]

    player_match_list1 = trade["player_matches1"]
    player_match_list2 = trade["player_matches2"]

    def show_draft_list(draft_match_list, trade_score_list):
        for draft_number, player_name in draft_match_list:
            player_data = players[(players['draft_position'] ==
                                   int(draft_number)) & (players['name'] ==
                                                         player_name)]

            trade_score_value = int(float(trade_score_list.get(player_name)))

            if not player_data.empty:
                player_page(player_data.iloc[0],
                            trade_score_value=trade_score_value)
            else:
                with st.expander(f"No data given for {player_name}, Hindsight score: 0"):
                    st.write(f"No data given for {player_name}")

    def show_player_list(player_match_list, trade_score_list):
        for player_name in player_match_list:
            player_data = players[(players['name'] == player_name)]

            trade_score_value = int(float(trade_score_list.get(player_name)))

            if not player_data.empty:
                player_page(player_data.iloc[0],
                            trade_score_value=trade_score_value)
            else:
                with st.expander(f"No data given for {player_name}, Hindsight score: 0"):
                    st.write(f"No data given for {player_name}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        ### Trade score for the {team1}: <span style="background-color:#3b3c51; color: black; padding: 3px 6px; border-radius: 5px; border: 1px solid #21233b; display: inline-block;">{int(tscore1)}</span>
        """, unsafe_allow_html=True)
        st.divider()
        show_draft_list(draft_match_list1, trade_score_list1)
        show_player_list(player_match_list1, trade_score_list1)
    with col2:
        st.markdown(f"""
        ### Trade score for the {team2}: <span style="background-color:#3b3c51; color: black; padding: 3px 6px; border-radius: 5px; border: 1px solid #21233b; display: inline-block;">{int(tscore2)}</span>
        """, unsafe_allow_html=True)
        st.divider()
        show_draft_list(draft_match_list2, trade_score_list2)
        show_player_list(player_match_list2, trade_score_list2)


def player_page(player_data, trade_score_value):
    # Gets called per player in drafted and normal player list.
    player_name = player_data["name"]

    player_id = player_data["player_id"]

    player_position = player_data["position"]

    player_full_career_avg_stats = get_player_full_career_average(player_id, player_position)

    encoded_player_name = urllib.parse.quote(player_name)

    url = f"https://hindsight-nfl.streamlit.app/~/+/player_search?selected_id={player_id}&selected_name={encoded_player_name}"

    with st.expander(f"{player_name} ({player_position}), Hindsight score: {trade_score_value}", expanded=True):
        col1, col2, col3 = st.columns([1, 3, 3], gap="small")
        with col1:
            st.image(player_data['headshot_url'], use_container_width=False,
                     width=200)
        with col2:
            st.markdown(f"""
                <div style="line-height: 1.2;">
                    <a href="{url}" style="font-size: 24px; font-weight: bold; 
                    color: white;">
                        {player_name} ({player_position})
                    </a>
                    <div style="
                        margin-left:10px;
                        background-color: #3b3c51;
                        color: black;
                        padding: 3px 6px;
                        border-radius: 5px;
                        border: 1px solid #21233b;
                        display: inline-block;
                        margin-top: 5px;">
                        {trade_score_value}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.subheader("Player Information")
            st.write(f"Born: {player_data['birthdate']}")
            st.write(f"College: {player_data['college']}")
            st.write(f"Draft: Round {player_data['draft_position']} ({player_data['draft_year']})")

        stats = get_career_seasons(player_id)

        years = stats['season'].tolist()

        options = ["Career"] + years

        selected_year = st.segmented_control(
            "Select Year",
            options=options,
            format_func=lambda x: str(x),
            selection_mode="single",
            default="Career",
            key=f"{player_name}"
        )

        player_start_date = player_full_career_avg_stats['start_date'].iloc[0]
        player_end_date = player_full_career_avg_stats['end_date'].iloc[0]

        # Set up trade data
        plot_stats = get_career_player_stats(player_id)
        plot_stats["gameday"] = pd.to_datetime(plot_stats["gameday"])

        avg_plot_stats = get_league_per_game_average(player_position,
                                                     player_start_date,
                                                     player_end_date)
        avg_plot_stats["gameday"] = pd.to_datetime(avg_plot_stats["gameday"])

        # Date ranges are shifted to follow the NFL season
        if selected_year in years:
            start_date = pd.Timestamp(f"{selected_year}-09-01")
            end_date = pd.Timestamp(f"{selected_year + 1}-09-01")
            plot_stats = plot_stats[plot_stats['season'] == selected_year]
            avg_plot_stats = avg_plot_stats[
                (avg_plot_stats['gameday'] >= start_date) &
                (avg_plot_stats['gameday'] < end_date)]
            st.subheader(f"{selected_year} Statistics")
        elif selected_year == "Career":
            st.subheader("Career Statistics")

        show_stats = True

        # to avoid overloading output more position-specific stats are used
        if player_position == "QB":
            selected_stat = st.selectbox(
                f"Choose one of {player_name}'s QB stat to observe",
                (
                    "completions", "attempts", "passing_yards",
                    "passing_tds", "interceptions", "sacks", "sack_yards",
                    "sack_fumbles", "sack_fumbles_lost",
                    "passing_air_yards", "passing_yards_after_catch",
                    "passing_first_downs",
                    "passing_epa", "passing_2pt_conversions", "pacr", "dakota",
                    "carries", "rushing_yards", "rushing_tds",
                    "rushing_fumbles",
                    "rushing_fumbles_lost", "rushing_first_downs",
                    "rushing_epa",
                    "rushing_2pt_conversions",
                    "fantasy_points", "fantasy_points_ppr", "age"
                    )
            )
        elif player_position == "RB":
            selected_stat = st.selectbox(
                f"Choose one of {player_name}'s RB stat to observe",
                (
                    "carries", "rushing_yards", "rushing_tds",
                    "rushing_fumbles",
                    "rushing_fumbles_lost", "rushing_first_downs",
                    "rushing_epa", "rushing_2pt_conversions",
                    "receptions", "targets", "receiving_yards",
                    "receiving_tds",
                    "receiving_fumbles", "receiving_fumbles_lost",
                    "receiving_air_yards", "receiving_yards_after_catch",
                    "receiving_first_downs", "receiving_epa",
                    "receiving_2pt_conversions",
                    "racr", "target_share", "air_yards_share", "wopr",
                    "fantasy_points", "fantasy_points_ppr", "age"
                )
            )
        elif player_position == "WR" or player_position == "TE":
            selected_stat = st.selectbox(
                f"Choose one of {player_name}'s WR/TE stat to observe",
                (
                    "receptions", "targets", "receiving_yards", "receiving_tds",
                    "receiving_fumbles", "receiving_fumbles_lost",
                    "receiving_air_yards", "receiving_yards_after_catch",
                    "receiving_first_downs", "receiving_epa",
                    "receiving_2pt_conversions",
                    "racr", "target_share", "air_yards_share", "wopr",
                    "carries", "rushing_yards", "rushing_tds",
                    "rushing_fumbles",
                    "rushing_fumbles_lost", "rushing_first_downs",
                    "rushing_epa", "rushing_2pt_conversions",
                    "fantasy_points", "fantasy_points_ppr", "age"
                )
            )
        elif player_position == "K" or player_position == "P":
            selected_stat = st.selectbox(
                f"Choose one of {player_name}'s K/P stat to observe",
                (
                    "special_teams_tds",
                    "fantasy_points", "fantasy_points_ppr", "age"
                )
            )
        else:
            st.write("No stats available for this position. Defensive statistics coming soon!")
            show_stats = False

        if show_stats:
            team_colors = get_team_colors()

            fig = go.Figure()

            plot_stats[f"Average_{selected_stat}"] = plot_stats[selected_stat].rolling(window=5, min_periods=1).mean()

            fig.add_trace(go.Scatter(x=plot_stats["gameday"], y=plot_stats[f"Average_{selected_stat}"],
                         mode='lines', name=f"{player_name}'s Average {selected_stat}"))

            avg_plot_stats[f"avg_{selected_stat}"] = avg_plot_stats[f"avg_{selected_stat}"].rolling(window=5, min_periods=1).mean()

            fig.add_trace(go.Scatter(
                x=avg_plot_stats["gameday"],
                y=avg_plot_stats[f"avg_{selected_stat}"],
                mode="lines",
                line=dict(color='#95238b'),
                name="League Average",
                opacity=0.65
            ))
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
                    showlegend=False,
                    opacity=0.75
                ))

            fig.update_layout(showlegend=True, legend={'traceorder': 'normal'},
                              legend_title="Legend")

            st.plotly_chart(fig)

            st.subheader(f"Ranked {player_position} Performance per Team")
            player_rank = get_ranked_players_per_team(player_position)
            st.dataframe(player_rank[player_rank["player_id"] == player_id])


def trade_main(page):

    st.sidebar.page_link('app.py', label='Home')
    st.sidebar.page_link('pages/trade_search.py', label='Trade Search')
    st.sidebar.page_link('pages/player_search.py', label='Player Search')
    st.sidebar.page_link('pages/about.py', label='About')

    # copies formatted valid trade
    filtered_trades = find_valid_trades(trades)

    performance_value = calculate_trade_value()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Hindsight Trade Search")
    with col2:
        if st.button("Clear"):
            st.query_params.clear()
            st.rerun()

    trade_dates = filtered_trades['date']

    ITEMS_PER_PAGE = 5

    query_params = st.query_params
    selected_search = query_params.get("search_name", "")
    selected_category = query_params.get("trade_date", "All")
    page_number = int(query_params.get("pg", 1))

    search_name = st.text_input("Search by name:", value=selected_search)
    category_options = ["All"] + list(trade_dates.dt.year.unique())
    trade_year_filter = st.selectbox("Filter by trade year:",
                                     category_options,
                                     index=category_options.index(selected_category))

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

    team_name_map = get_short_to_long_team_abbreviation_map()

    performance_value["new_team"] = performance_value["new_team"].map(team_name_map)

    if len(filtered_trades) > 0:
        for index, row in paginated_data.iterrows():
            date = row["date"].strftime("%B %-d, %Y")
            team_logos = get_team_logos()
            team1 = row["team1"]
            team2 = row["team2"]
            team1Logo = team_logos.get(team1, "images/default.png")
            team2Logo = team_logos.get(team2, "images/default.png")
            team1Value, team2Value, _, _ = pull_trade_value(index,
                                                            performance_value,
                                                            filtered_trades,
                                                            team1,
                                                            team2)
            team1Value = int(team1Value)
            team2Value = int(team2Value)

            clickable_link(
                           f"{team1} acquire {row["acquired_team1"]}",
                           f"{team2} acquire {row["acquired_team2"]}",
                           f"?pg={page}&index={index}&date={date}",
                           team1Logo, team2Logo,
                           team1Value, team2Value,
                           team1, team2)
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
page = params.get("pg", 1)
index = params.get("index")
transaction_date = params.get("date")

if index:
    show_trade_comp_page(index, page, transaction_date)
else:
    trade_main(page)
