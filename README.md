# 📊 Hindsight - NFL Trade Analyzer

🚀 **[View Live Demo](https://hindsight-nfl.streamlit.app/)**

# **Hindsight – NFL Trade Analyzer**  

Hindsight is a historical NFL trade analysis tool that evaluates the success of trades from **2002 to 2025**. By assigning **trade scores** to each team involved, it provides an easy way to assess past transactions.

## **How It Works**  

Each trade is scored based on the **average trade score** of the players exchanged.  

For example, the [April 19, 2005 Broncos-Commanders trade](https://hindsight-nfl.streamlit.app/trade_search?index=89&date=April%2019,%202005&team1=Broncos&team2=Commanders&tscore1=32&tscore2=73) involving **Brandon Marshall, Jason Campbell, Karl Paymah, and Manny Lawrence** resulted in a **32-73 split**—with 0 assigned to players lacking data.  

A **player’s trade score** is calculated based on:  
- **Team success** (win/loss percentage during their tenure)  
- **Position value** (higher impact for key positions)  
- **Performance** (league-wide ranking in position-specific stats)  

This simple methodology adds context to trades like the [2004 Eli Manning draft trade](https://hindsight-nfl.streamlit.app/~/+/trade_search?index=56&date=April%2024,%202004&team1=Chargers&team2=Giants&tscore1=61&tscore2=81) and can help fantasy football managers avoid similar mistakes.  

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
