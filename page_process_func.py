import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def home_page(match_data, ball_data):
    editions = np.sort(match_data['Season'].unique().astype('int'))
    total_editions = len(editions)
    first_edition = editions[0]
    last_edition = editions[-1]

    title_won = match_data[match_data['MatchNumber'] == 'Final']['WinningTeam'].value_counts()
    plt.figure(0)
    plt.xticks(rotation=90)
    sns.barplot(x=title_won.index, y=title_won.values)
    plt.xlabel('Teams')
    plt.ylabel('Trophies Won')
    plt.savefig(os.path.join('graphs','Title_won.png'),edgecolor='b',bbox_inches='tight')

    top_scorer_IPL = ball_data.groupby('batter').sum()['batsman_run'].sort_values(ascending=False)[:10]
    plt.figure(1)
    plt.xticks(rotation=90)
    sns.barplot(x=top_scorer_IPL.index, y=top_scorer_IPL.values)
    plt.xlabel('Batsman')
    plt.ylabel('Total Run')
    plt.savefig(os.path.join('graphs','Top_run_scorer_IPL.png'),edgecolor='b',bbox_inches='tight')

    bowlers_wicket_kind = ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw']
    top_wicket_taker_IPL = ball_data[ball_data['kind'].isin(bowlers_wicket_kind)].groupby('bowler').sum()['isWicketDelivery'].sort_values(ascending=False)[:10]
    plt.figure(2)
    plt.xticks(rotation=90)
    sns.barplot(x=top_wicket_taker_IPL.index, y=top_wicket_taker_IPL.values)
    plt.xlabel('Bowler')
    plt.ylabel('Total Wickets')
    plt.savefig(os.path.join('graphs','top_wicket_taker_IPL.png'),edgecolor='b',bbox_inches='tight')

    home_page_data = {}
    home_page_data['total_editions'] = total_editions
    home_page_data['first_edition'] = first_edition
    home_page_data['last_edition'] = last_edition    

    return home_page_data

def team_analysis_page(match_data, ball_data, team_name):

    team_editions = match_data[(match_data['Team1'] == team_name) | (match_data['Team2'] == team_name)]['Season'].unique()
    team_editions = team_editions.astype(np.int16)
    team_editions.sort()
    first_edition, last_edition = team_editions[0], team_editions[-1]

    ## Old Logic
    # match_played = match_data[(match_data['Team1'] == team_name) | (match_data['Team2'] == team_name)].shape[0]
    # match_won = match_data[match_data['WinningTeam'] == team_name].shape[0]
    # win_percentage = round(match_won / match_played * 100,2)
    # trophy_won = match_data[(match_data['WinningTeam'] == team_name) & (match_data['MatchNumber'] == 'Final')].shape[0]

    ## New logic
    team_match_played_data = match_data[((match_data['Team1'] == team_name) | (match_data['Team2'] == team_name))]
    team_match_won_data = team_match_played_data[team_match_played_data['WinningTeam'] == team_name].groupby('Season').size()
    team_season_won_data = team_match_played_data[(team_match_played_data['WinningTeam'] == team_name) & (team_match_played_data['MatchNumber'] == 'Final')].groupby('Season').size()

    match_played = team_match_played_data.shape[0]
    match_won = team_match_won_data.sum()
    win_percentage = round(match_won / match_played * 100,2)
    trophy_won = team_season_won_data.sum()

    temp_season_won_data = team_match_won_data[team_season_won_data.index]
    plt.figure(0,figsize=(8,6))
    if team_match_won_data.shape[0] == 1:
        plt.scatter(team_match_won_data.index, team_match_won_data.values, label='Match Won',color='red',marker='o',s = 100)
    else:
        plt.plot(team_match_won_data,label='Match Won',color='red')
    plt.scatter(temp_season_won_data.index,temp_season_won_data.values,label='Title Won',color='b',marker='*',s=200)
    plt.xlabel('Season')
    plt.ylabel('Matches Won')
    plt.legend()
    plt.savefig(os.path.join('graphs','matches_won_team.png'),edgecolor='w',bbox_inches='tight')

    top_run_scorer = ball_data[ball_data['BattingTeam'] == team_name].groupby('batter').sum()['batsman_run'].sort_values(ascending=False)[:10]
    plt.figure(1)
    plt.xticks(rotation=90)
    sns.barplot(x=top_run_scorer.index, y=top_run_scorer.values)
    plt.xlabel('Batsman')
    plt.ylabel('Total Runs')
    plt.savefig(os.path.join('graphs','Top_run_scorer_team.png'),edgecolor='w',bbox_inches='tight')

    bowlers_wicket_kind = ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw']
    match_id_team_played = match_data[(match_data['Team1'] == team_name) | (match_data['Team2'] == team_name)]['ID']
    team_wicket_data = ball_data[ball_data['ID'].isin(match_id_team_played) & (ball_data['BattingTeam'] != team_name) & (ball_data['kind'].isin(bowlers_wicket_kind))]
    top_wicket_taker = team_wicket_data.groupby('bowler').sum()['isWicketDelivery'].sort_values(ascending=False)[:10]
    plt.figure(2)
    plt.xticks(rotation=90)
    sns.barplot(x=top_wicket_taker.index, y=top_wicket_taker.values)
    plt.xlabel('Bowler')
    plt.ylabel('Total Wickets')
    plt.savefig(os.path.join('graphs','Top_wicket_taker_team.png'),edgecolor='w',bbox_inches='tight')

    team_analysis_data = {}
    team_analysis_data['first_edition'] = first_edition
    team_analysis_data['last_edition'] = last_edition
    team_analysis_data['match_played'] = match_played
    team_analysis_data['match_won'] = match_won
    team_analysis_data['win_percentage'] = win_percentage
    team_analysis_data['tropy_won'] = trophy_won

    return team_analysis_data

def team_vs_team_page(match_data, ball_data, team1, team2):
    id_match_played = match_data[((match_data['Team1'] == team1) & (match_data['Team2'] == team2)) | 
                              ((match_data['Team1'] == team2) & (match_data['Team2'] == team1))]['ID']

    if id_match_played.shape[0]:

        match_played = id_match_played.shape[0]
        match_won_team1 = match_data[(match_data['ID'].isin(id_match_played)) & (match_data['WinningTeam'] == team1)].shape[0]
        match_won_team2 = match_data[(match_data['ID'].isin(id_match_played)) & (match_data['WinningTeam'] == team2)].shape[0]

        team_1_scores = ball_data[(ball_data['ID'].isin(id_match_played)) & (ball_data['BattingTeam'] == team1)].groupby('ID')['total_run'].sum().sort_values()
        team1_low = team_1_scores.iloc[0]
        team1_high = team_1_scores.iloc[-1]

        team_2_scores = ball_data[(ball_data['ID'].isin(id_match_played)) & (ball_data['BattingTeam'] == team2)].groupby('ID')['total_run'].sum().sort_values()
        team2_low = team_2_scores.iloc[0]
        team2_high = team_2_scores.iloc[-1]

        plt.figure(0)
        plt.pie([match_won_team1, match_won_team2], labels=[team1, team2], autopct='%1.1f%%')
        plt.savefig(os.path.join('graphs','TeamVsTeam_won.png'))

        plt.figure(1)
        x_axis = np.arange(2)
        plt.bar(x_axis -0.2, [team1_high, team2_high], width=0.4, label = 'Highest score')
        plt.bar(x_axis +0.2, [team1_low, team2_low], width=0.4, label = 'Lowest score')

        # Xticks
        plt.xticks(x_axis, [team1, team2])
        plt.yticks(np.arange(0, max([team1_high, team2_high]), 20))
        
        # Add legend
        plt.legend()

        plt.savefig(os.path.join('graphs','TeamVsTeam_HighLow.png'))

        return match_played
    else:
        return 0

def player_analysis_page(match_data, ball_data, player_name):

    ## MoM
    MoM = match_data[match_data['Player_of_Match'] == player_name].shape[0]

    ## ------------------ Batting Statistics --------------------

    batting_stats = {}

    # Number of innings played by a batsman
    batting_innings = ball_data[ball_data['batter'] == player_name]['ID'].unique().shape[0]
    batting_stats['Innings'] = batting_innings

    if batting_innings != 0:

        # Total run scored by a batsaman
        scored_runs = ball_data[ball_data['batter'] == player_name]['batsman_run'].sum()
        batting_stats['Runs'] = scored_runs

        # Highest score of a batsman 
        highest_score = ball_data[ball_data['batter'] == player_name].groupby('ID').sum()['batsman_run'].max()
        batting_stats['Highest Score'] = highest_score
        
        # Number of times batsman remains not out 
        out_number = ball_data[ball_data['player_out'] == player_name].shape[0]
        not_out = batting_innings - out_number
        batting_stats['Not Out'] = not_out

        # Batting average of a batsman
        if out_number != 0:
            bat_average = round(scored_runs / out_number,2)
        else:
            bat_average = 'NA'
        batting_stats['Average'] = bat_average
        
        # Stike rate of a btasman
        ball_played = ball_data[ball_data['batter'] == player_name].shape[0]
        bat_strike_rate = round(scored_runs / ball_played * 100,2)
        batting_stats['Strike Rate'] = bat_strike_rate

        # 100s and 50s
        runs_per_inning = ball_data[ball_data['batter'] == player_name].groupby('ID').sum()['batsman_run']
        number_100 = runs_per_inning[runs_per_inning >= 100].shape[0]
        batting_stats['100s'] = number_100
        
        number_50 = runs_per_inning[(runs_per_inning >= 50) & (runs_per_inning < 100)].shape[0]
        batting_stats['50s'] = number_50

        # 6s
        sixes_data = ball_data[ball_data['batter'] == player_name]['batsman_run'] == 6
        number_6s = sixes_data.sum()
        batting_stats['6s'] = number_6s

        # 4s
        fours_data = ball_data[ball_data['batter'] == player_name]['batsman_run'] == 4
        number_4s = fours_data.sum()
        batting_stats['4s'] = number_4s
        
    else:
        batting_stats['Innings'] = 0
        batting_stats['Runs'] = 0
        batting_stats['Highest Score'] = 0
        batting_stats['Not Out'] = 0
        batting_stats['Average'] = 0
        batting_stats['Strike Rate'] = 0
        batting_stats['100s'] = 0
        batting_stats['50s'] = 0
        batting_stats['6s'] = 0
        batting_stats['4s'] = 0


    ## ------------------ Bowling Statistics --------------------

    bowling_stats = {}

    # Number of innings played by bowler
    bowling_innings = ball_data[ball_data['bowler'] == player_name]['ID'].unique().shape[0]
    bowling_stats['Innings'] = bowling_innings

    if bowling_innings != 0:
        # Number of balls bowl
        not_legitimate_delivery = ['wides', 'noballs']
        balls_bowl = ball_data[(ball_data['bowler'] == player_name) & (~ball_data['extra_type'].isin(not_legitimate_delivery))].shape[0]
        bowling_stats['Balls'] = balls_bowl
        
        # Total wickets taken by bowler
        bowlers_wicket_kind = ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw']
        total_wickets_taken = ball_data[(ball_data['bowler'] == player_name) & (ball_data['kind'].isin(bowlers_wicket_kind))].shape[0]
        bowling_stats['Wickets'] = total_wickets_taken
        
        # Run given by bowler
        extras_not_count_against_bowler = ['legbyes', 'byes']
        runs_given = ball_data[(ball_data['bowler'] == player_name) & (~ball_data['extra_type'].isin(extras_not_count_against_bowler))][['batsman_run','extras_run']].sum().sum()
        bowling_stats['Runs'] = runs_given
        
        # Bowler economy (average run given per over)
        bowler_economy = round(runs_given / (balls_bowl / 6),2)
        bowling_stats['Economy'] = bowler_economy
        
        # Bowler average (average runs given per wicket)
        if total_wickets_taken != 0:
            bowler_average = round(runs_given / total_wickets_taken, 2)
        else:
            bowler_average = 'NA'
            
        bowling_stats['Average'] = bowler_average
        
        # Bowler strike rate (average balls bowl per wicket)
        if total_wickets_taken != 0:
            bowler_strike_rate = round(balls_bowl / total_wickets_taken, 2)
        else:
            bowler_strike_rate = 'NA'
            
        bowling_stats['Strike rate'] = bowler_strike_rate

        # 5 wicket haul 
        wickets_per_match = ball_data[ball_data['bowler'] == player_name].groupby('ID').sum()['isWicketDelivery']
        wickets_5 = wickets_per_match[wickets_per_match >= 5].shape[0]
        bowling_stats['5 wicket haul'] = wickets_5
        
    else:
        bowling_stats['Innings'] = 0
        bowling_stats['Balls'] = 0
        bowling_stats['Wickets'] = 0
        bowling_stats['Runs'] = 0
        bowling_stats['Economy'] = 0
        bowling_stats['Average'] = 0
        bowling_stats['Strike rate'] = 0
        bowling_stats['5 wicket haul'] = 0


    player_analysis_data = {}
    player_analysis_data['MoM'] = MoM
    player_analysis_data['batting_stats'] = batting_stats
    player_analysis_data['bowling_stats'] = bowling_stats

    return player_analysis_data

def insight_page(match_data):
    total_matches = match_data.shape[0]
    toss_win_match_win = match_data[match_data['TossWinner'] == match_data['WinningTeam']].shape[0]
    toss_win_match_lose = total_matches - toss_win_match_win

    plt.pie([toss_win_match_win, toss_win_match_lose], labels=['Toss Win, Match Win', 'Toss Win, Match Lose'], autopct='%1.1f%%')
    plt.savefig(os.path.join('graphs','toss_effect_on_match_winning.png'))

    insight_data = {}
    insight_data['toss_match_relation'] = round(toss_win_match_win / total_matches * 100, 2)

    return insight_data