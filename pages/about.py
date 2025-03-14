import streamlit as st

def about_page():
    st.set_page_config(
    page_title="About Hindsight",
    page_icon="🏈",
    layout="wide"
    )
    st.title("📊 About")
    st.sidebar.page_link('app.py', label='Home')
    st.sidebar.page_link('pages/trade_search.py', label='Trade Search')
    st.sidebar.page_link('pages/player_search.py', label='Player Search')
    st.sidebar.page_link('pages/about.py', label='About')
    # Introduction
    st.markdown(
        """
        Welcome to **Hindsight**, a historical NFL trade analyzer! This tool 
        provides a straightforward way to evaluate the success of NFL trades. 
        ### Here's how it works:
        For each NFL trade in the range (2002 to 2025), 2 trade scores are assigned, one for each team. 
        This trade score is an average of each traded player's individual trade score. 

        For example: the April 19th, [2005 Broncos-Commanders/Redskins](https://hindsight-nfl.streamlit.app/trade_search?index=89&date=April%2019,%202005&team1=Broncos&team2=Commanders&tscore1=32&tscore2=73) 
        trade of Brandon Marshall, Jason Campbell, Karl Paymah, and Manny Lawrence, received an average 32-73 for all players traded to the Broncos and Commanders respectively (0 being the value assigned to players with no data).

        A player's trade score is calculated from their total performance while at the team they were traded to. 
        There are several factors involved in this score:\n
        - the win/loss percentage of the team during their tenure\n
        - the position they play (higher value for key players)\n
        - the player's league-wide ranking in position-specific stats during their time on the team\n

        While the methodology is simple, it provides context for controversial trades like the Chargers' 
        [2004 NFL Draft Eli Manning trade](https://hindsight-nfl.streamlit.app/~/+/trade_search?index=56&date=April%2024,%202004&team1=Chargers&team2=Giants&tscore1=61&tscore2=81) and may help fantasy football managers avoid similar mistakes.
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
