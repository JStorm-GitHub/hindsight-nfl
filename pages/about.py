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
        Welcome to **NFL Trade Analyzer**. This is a straight-forward attempt to analyze the success of NFL trades.
        The success of a trade is evaluated using the team's win/loss record after the player is acquired. The score is weighed
        so that postseason victories mean more. It also gives more weight to core positions like QB and
        RB. While the methodology is simple, it gives context to contentious decisions like the Chargers' 
        [2004 NFL Draft Eli Manning trade](http://localhost:5000/?index=56&date=2004&team1=Chargers&team2=Giants&tscore1=9&tscore2=199)
        and it may offer insights on how to avoid making similar mistakes on your fantasy team.
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
