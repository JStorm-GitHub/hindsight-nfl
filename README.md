# 📊 Hindsight - NFL Trade Analyzer

🚀 **[View Live Demo](https://hindsight-nfl.streamlit.app/)**

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
