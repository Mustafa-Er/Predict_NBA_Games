import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime


#Directory of html(score) files 
scores_dir = "data-nbagames/scores"

#Find the full directory of html(score) files
box_scores = os.listdir(scores_dir)
box_scores = [os.path.join(scores_dir, f) for f in box_scores if f.endswith(".html")]
print(f"Count of File is {len(box_scores)}")


def parse_html(box_score: str) -> BeautifulSoup:
    """
    This function reads the html file and deletes some tables in it


    Parameter: box_score: File which will read

    Return: BeatifulSoup object
    
    """
    with open(box_score, "r", encoding = "utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "lxml")
    [s.decompose() for s in soup.select("tr.over_header")]
    [s.decompose() for s in soup.select("tr.thead")]
    return soup


def read_scores(soup: BeautifulSoup) -> pd.DataFrame:
    """
    This function takes the BeatifulSoup object and reads the score of the match from it

    Parameter: BeatifulSoup object to extract score of match

    Return: pd.DataFrame object which cover score of match and teams of match
    
    """

    
   
    try:
        scorebox_soup = soup.find("div", class_ = "scorebox")
        scores_soup = scorebox_soup.find_all("div", class_ = "score")
        list_scores = []
        for score_soup in scores_soup:
            list_scores.append(int(score_soup.text.strip()))

        imgtags = scorebox_soup.find_all("img")
        list_teams = []
        for img_tag in imgtags:
            team = img_tag['src'].split("/")[-1].split("-")[0]
            list_teams.append(team)
        
        data = {
            "Team": list_teams,
            "Total": list_scores
            }
        
        scores = pd.DataFrame(data = data)
    except Exception as  e:
        print(f"Error: {str(e)}")
        print(f"Match which has error: {soup.h1}")
        data = {
            "Team": list_teams,
            "Totals": [0, 5000]
        }
        scores = pd.DataFrame(data = data)
        
    return scores


def read_season_info(soup: BeautifulSoup) -> int:
    """
    This function takes the BeatifulSoup object and extracts the season information from it

    Parameter: BeatifulSoup object to extract season of match

    Return: Season of match
    """

    nav = soup.select("#bottom_nav_container")[0]#The select function returns an array and we get the information in the first row.
    hrefs = [a["href"] for a in nav.find_all("a")] #we collected all href information
    season = os.path.basename(hrefs[1]).split("_")[0] #The os.path.basename function is there to get the filename and it gets the last extension in a place full of slashes("/"). 
                                                        #So we took the last line of information in the href and split it with "_"
    return season

# Basic Box Score Stats ile Advanced Box Score Stats isimli tablolardaki verileri pandasta tabloya dönüştürme fonksiyonudur.
def read_stats(soup: BeautifulSoup, team: str, stat: str) -> pd.DataFrame:
    """
    It is a function to convert the data in the tables named Basic Box Score Stats and Advanced Box Score Stats in the BeatifulSoup object to the pandas table.

    Parameters:
        soup: BeatifulSoup object to get dataftame object
        team: Name of team
        stat: It can be two string: Basic or Advanced. If basic, we get basic box score stats table and else, we get advanced box score stats table
    
    Return:
        pd.Dataframe object which converted
    
    """
    df = pd.read_html(str(soup), attrs = {'id': f'box-{team}-game-{stat}'}, index_col=0)[0]
    df["MP"] = df["MP"].str.split(":").str[0] #get minutes of players' time in a match
    df = df.apply(pd.to_numeric, errors = "coerce") #change data type of columns to numeric
    return df



base_cols_player, base_cols_team = None, None #Specify base columns for team an player stats
players, games = [], [] 
for box_score in box_scores:
    soup = parse_html(box_score)                                                                                #Get soup object from html file
    line_score = read_scores(soup)                                                                              #Get dataframe with score of match and team names
    teams = line_score["Team"]                                                                                  #Get team names
    summaries_player, summaries_team = [], []
    for team in teams:
        basic = read_stats(soup, team, "basic")                                                                 #Get dataframe with basic stats
        advanced = read_stats(soup, team, "advanced")                                                           #Get dataframe with advanced stats

        basic = basic.reset_index()                                                                             #Do reset_index to basic dataframe
        advanced = advanced.reset_index()                                                                       #Do reset index to advanced dataframe

        df_player = pd.merge(basic.iloc[:10,], advanced.iloc[:10,:], on = ["Starters", "MP"], how = "outer")    #Create dataframe with merging first 10 player stats in basic and advanced dataframes
        df_player.columns = df_player.columns.str.lower() + "_player"                                           #Change columns names of player dataframe
        df_player = df_player.rename(columns = {"starters_player": "player_name"})                              #Change column name called starters_player
    

        df_player["date"] = os.path.basename(box_score)[:8]                                                     #Get last 8 element of filename in directory with using basename function
        df_player["date"] = pd.to_datetime(df_player["date"], format="%Y%m%d")                                  #Change format of date type

        df_player["team"] = team                                                                                #Add team name

        df_player["season"] = read_season_info(soup)                                                            #Get season of match

        if not "bpm_player" in df_player.columns:
            df_player["bpm_player"] = 0
        
        #Determine base columns for player dataframe
        if base_cols_player is None:
            base_cols_player = [col for col in df_player.columns]
        
        df_player = df_player[base_cols_player]
        df_player = df_player.fillna(0)                                                                         #Fill Na values with 0
        summaries_player.append(df_player)                                                                      #Add player dataframe to array


        #----------------------------------------------------------------------------------Team Stats----------------------------------------------------------------------------------
        df_team = pd.concat([basic.iloc[-1, 1:].to_frame().T, advanced.iloc[-1, 1:].to_frame().T], axis = 1)    #Create team dataframw with using last row of basic and advanced dataframes 
        df_team = df_team.loc[:, ~df_team.columns.duplicated(keep='first')]                                     #Remove duplicated columns from team dataframe
        df_team.columns = df_team.columns.str.lower()                                                           #Convert column names to lower case

        #Add player names of team to team dataframe
        for i in range(10):
            df_team[f"player_{i+1}_name"] = basic["Starters"][i]
        
        df_team["team"] = team                                                                                  #Add team name to team dataframe

        #Determine base columns for team dataframe
        if base_cols_team is None:
            base_cols_team = [col for col in df_team.columns if not "bpm" in col]

        
        df_team = df_team[base_cols_team]                                                                       
        df_team = df_team.fillna(0)                                                                             #Fill Na values with 0
        summaries_team.append(df_team)                                                                          #Add team dataframe to array

    summary_player = pd.concat(summaries_player, axis = 0)                                                      #Concatenates the elements of the list named summaries_player, which contains two player dataframes separately
    players.append(summary_player)                                                                              #Add array concatenated to another array



    summary_team = pd.concat(summaries_team, axis = 0)                                                          #Concatenates the elements of the list named summaries_team, which contains two team dataframes separately
    summary_team = summary_team.reset_index(drop = True)                                                        #Add array concatenated to another array

    summary_team["total"] = line_score["Total"].values                                                          #Add score of each team in the match
    summary_team["home"] = [0, 1]                                                                               #Add whether team is home

    summary_team_opp = summary_team[::-1].reset_index(drop=True).copy()                                         #Reverse of summary_team dataframe to get statistics of the same match according to the opposing team
    summary_team_opp.columns += "_opp"                                                                          #Add "_opp" to column names of dataframe reversed 

    full_game = pd.concat([summary_team, summary_team_opp], axis = 1)                                           #Concatenate two dataframe from columns
    full_game["season"] = read_season_info(soup)                                                                #Add season of match 

    full_game["date"] = os.path.basename(box_score)[:8]                                                         #Get last 8 element of filename in directory with using basename function
    full_game["date"] = pd.to_datetime(full_game["date"], format="%Y%m%d")                                      #Change format of date type                                      

    full_game["won"] = full_game["total"] > full_game["total_opp"]                                              #Add whether team won the match
    #player_names = [col for col in full_game.columns if "player" in col]
    games.append(full_game)                                                                                     #Append dataframe to array
    
    #Let us know every 100 matches to see progress
    if len(games) % 100 == 0:
        print(f"{len(games)} / {len(box_scores)}")


today_date = datetime.today().strftime("%d%m%y_%H_%M")                                                          #Get date of today with format day-month-year hour-minute
games_df = pd.concat(games, ignore_index=True)                                                                  #Concatenate each element of array called games
games_df.to_csv(f"nba_games_V6_{today_date}.csv")                                                               #Save the array in csv file format

players_df = pd.concat(players, axis = 0).reset_index(drop = True)                                              #Concatenate each element of array called players
players_df.to_csv(f"nba_players_V6_{today_date}.csv")                                                           #Save the array in csv file format
