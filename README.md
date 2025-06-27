# Predict_NBA_Games

📂 Project Structure
.
├── data-nbagames/                    # Scraped raw game data (2010–Oct 2024)
├── NBA_Data_Science_Works.ipynb     # Main analysis, modeling, and feature engineering notebook
├── Parse_NBA_Games.py               # Parser to structure scraped data
├── Scraping_NBA_Games.py            # Web scraper using BeautifulSoup
├── nba_games_V6_081123_02_04.csv    # Processed game-level features
├── nba_players_V6_081123_02_04.csv  # Processed player-level features



🌐 Data Collection
Data was scraped from: https://www.basketball-reference.com/

Tools: BeautifulSoup for HTML parsing

Files:

Scraping_NBA_Games.py: Collects data for each match

Parse_NBA_Games.py: Transforms raw scraped data into structured CSVs

🏀 Collected data includes all NBA games from 2010 to October 2024

🧼 Data Cleaning and Feature Engineering
Fixed inconsistent player names using a custom character translation dictionary

Added team-level features, such as:

Total number of All-Star players in each team (based on recent All-Star games)

Win streak for both home and away teams

Difference features (e.g., home_feature - away_feature)

Removed highly correlated features based on EDA

📊 Key Features & Metrics
Collected both team statistics and player statistics, including but not limited to:

| **Feature**         | **Description**                     |
|---------------------|--------------------------------------|
| 3P, 3PA, 3P%         | Three-point shooting                 |
| AST, AST%            | Assists and assist rate             |
| BLK, BLK%            | Blocks and block rate               |
| DRB, DRB%            | Defensive rebounds                  |
| eFG%                | Effective Field Goal %              |
| TS%                 | True Shooting %                     |
| ORB, TRB            | Offensive/Total rebounds            |
| STL%, TOV%          | Steal & Turnover percentages        |
| BPM, ORtg, DRtg     | Box plus/minus, Off/Def ratings     |
| Usg%                | Usage Rate                          |


See Basketball Reference's official glossary for exact formulas and definitions.

🔍 Dimensionality Reduction
PCA and LDA were used for reducing feature dimensions

Feature scaling done with StandardScaler

Dimensionality reduction is configurable via a Config class

🧠 Modeling
Used XGBoost Classifier to predict the match winner:

### 🕒 Model Performance

| **Metric**  | **Value**       |
|-------------|-----------------|
| Accuracy    | 0.637           |
| F1 Score    | 0.637           |
| Runtime     | ~40 seconds     |




