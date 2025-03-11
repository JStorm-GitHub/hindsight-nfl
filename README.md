# 📊 NFL Trade Analyzer

🚀 **[View Live Demo](https://nfl-trade-analyzer-dxgzbjijmzh9t9xrgpdzri.streamlit.app/)**

Welcome to **NFL Trade Analyzer**! This tool provides a straightforward way to evaluate the success of NFL trades. It assesses a trade's impact based on the team's win/loss record after acquiring a player, giving extra weight to postseason victories and key positions like **Quarterback (QB)** and **Running Back (RB)**.

While the methodology is simple, it provides context for controversial trades like the Chargers' [2004 NFL Draft Eli Manning trade](https://nfl-trade-analyzer-dxgzbjijmzh9t9xrgpdzri.streamlit.app/~/+/trade_search?index=56&date=2004&team1=Chargers&team2=Giants&tscore1=9&tscore2=199) and may help fantasy football managers avoid similar mistakes.

---

## ⚡ Key Features

- 📅 **Historical Data** – Weekly player stats from **2002 to today**  
- 🔄 **Player Transactions** – Track **trades, injuries, and releases**  
- 🔍 **Interactive Search** – Find players by **name, team, or position**  
- 📈 **Stat Visualization** – View **charts and tables** for analysis  

---

## 📚 Data Sources

The data is sourced from publicly available NFL records and updated periodically. Major sources include:

- [nflverse](https://github.com/nflverse)  
- [Pro Sports Transactions](https://www.prosportstransactions.com/)  

While efforts are made to ensure accuracy, users should cross-check insights with official league sources.

---

## 🚀 Get Started



This application is built using **Streamlit**. To run it locally:

```bash
pip install -r requirements.txt
streamlit run app.py
