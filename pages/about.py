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
        **Hindsight** is a historical NFL trade analysis tool that evaluates the impact of trades from 2002 to 2025. Each trade is assigned two scores—one per team—based on the performance of the players involved.
        
        #### How Trade Scores Work
        - Each player in a trade receives an individual score reflecting their contributions while on the team.
        - A team’s trade score is the average of all its acquired players’ scores.
        
        **Example:**
        The [April 19, 2005 Broncos-Commanders trade](https://hindsight-nfl.streamlit.app/trade_search?index=89&date=April%2019,%202005&team1=Broncos&team2=Commanders&tscore1=32&tscore2=73) involved Brandon Marshall, Jason Campbell, Karl Paymah, and Manny Lawrence. The Broncos received a trade score of **32**, while the Commanders scored **73**.
        
        #### Factors Affecting Player Scores
        - **Team performance** (win/loss record during their tenure)
        - **Positional value** (key positions have higher impact)
        - **Individual performance** (league-wide ranking in position-specific stats)
        
        While simple, this method provides context for trades like the [2004 Eli Manning trade](https://hindsight-nfl.streamlit.app/trade_search?index=56&date=April%2024,%202004&team1=Chargers&team2=Giants&tscore1=61&tscore2=81) and can offer insights for fantasy football managers.
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
