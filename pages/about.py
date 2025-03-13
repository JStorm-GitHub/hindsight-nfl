import streamlit as st

def about_page():
    st.title("📊 About")
    st.sidebar.page_link('app.py', label='Home')
    st.sidebar.page_link('pages/trade_search.py', label='Trade Search')
    st.sidebar.page_link('pages/player_search.py', label='Player Search')
    st.sidebar.page_link('pages/about.py', label='About')
    # Introduction
    st.markdown(
        """
        Welcome to **Hindsight**, a historical NFL trade analyzer! This tool 
        provides a straightforward way to evaluate the success of NFL trades. It assesses a 
        trade's impact based on the team's win/loss record after acquiring a player, giving extra weight 
        to postseason victories and key positions like **Quarterback (QB)** and **Running Back (RB)**. 

        It also weighs a player's league-wide rank in stats like **total passing yards** and 
        **total rushing yards**, depending on the position.

        Because these trades are historical, all Hindsight Trade Scores use 
        data from after the player is traded but during the time they're playing for the acquiring team.

        While the methodology is simple, it provides context for controversial trades like the Chargers' 
        [2004 NFL Draft Eli Manning trade](https://nfl-trade-analyzer-dxgzbjijmzh9t9xrgpdzri.streamlit.app/~/+/trade_search?index=56&date=2004&team1=Chargers&team2=Giants&tscore1=9&tscore2=199) and may help fantasy football managers avoid similar mistakes.
        """
    )

    # Features Section
    st.subheader("⚡ Key Features")
    features = [
        "📅 **Historical Data** – Weekly stats from 2002 to today",
        "🔄 **Player Transactions** – Trades, injuries, and releases",
        "🔍 **Interactive Search** – Find players by name, team, or position",
        "📈 **Stat Visualization** – Charts and tables for easy analysis"
    ]
    for feature in features:
        st.markdown(f"- {feature}")

    # Data Sources Section
    st.subheader("📚 Data Sources")
    st.markdown(
        """
        The data is sourced from publicly available NFL records and updated periodically, specifically [nflverse](https://github.com/nflverse) 
        and [prosportstransactions](https://www.prosportstransactions.com/). While efforts are made to ensure accuracy, users should cross-check important insights 
        with official league sources.
        """
    )

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io/)")

# Run the about page function
if __name__ == "__main__":
    about_page()
