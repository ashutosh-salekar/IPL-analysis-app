import streamlit as st
import pickle
import page_process_func
import os


match_data = pickle.load(open('match_data.pkl','rb'))
ball_data = pickle.load(open('ball_data.pkl','rb'))
all_player_names = pickle.load(open('all_player_names.pkl','rb'))
all_team_names = pickle.load(open('all_team_names.pkl','rb'))

st.set_page_config(layout='wide', page_title='IPL Analysis')

st.sidebar.title('IPL Analysis')
st.sidebar.image('IPL_logo.png')

action = st.sidebar.radio('Select',
['Home', 'Team Analysis', 'Player Analysis', 'Team Vs Team', 'Insights'])

if action == 'Home':
    st.title('Home')
    response = page_process_func.home_page(match_data, ball_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title('Total Editions')
        st.header(response['total_editions'])

    with col2:
        st.title('First Edition')
        st.header(response['first_edition'])

    with col3:
        st.title('Last Edition')
        st.header(response['last_edition'])
    
    st.header('Trophies Won By Teams')
    st.image(os.path.join('graphs','Title_won.png'))
    
    st.header('Top Run Scorer')
    st.image(os.path.join('graphs','Top_run_scorer_IPL.png'))

    st.header('Top Wicket Taker')
    st.image(os.path.join('graphs','top_wicket_taker_IPL.png'))

if action == 'Team Analysis':
    st.title('Team Analysis')

    col1, col2 = st.columns(2)
    with col1:
        team_name = st.selectbox('Select Team', all_team_names)

    response = page_process_func.team_analysis_page(match_data, ball_data, team_name)
    col3, col4, col5 = st.columns(3)
    with col3:
        st.header('First Edition')
        st.subheader(response['first_edition'])

    with col4:
        st.header('Last Edition')
        st.subheader(response['last_edition'])

    with col5:
        st.header('Title won')
        st.subheader(response['tropy_won'])

    col5, col6, col7 = st.columns(3)

    with col5:
        st.header('Match Played')
        st.subheader(response['match_played'])

    with col6:
        st.header('Match Won')
        st.subheader(response['match_won'])

    with col7:
        st.header('Winning Percentage')
        st.subheader(str(response['win_percentage']) + '%')

    st.header('Season Wise Team Performance')
    st.image(os.path.join('graphs','matches_won_team.png'))

    st.header('Top Run scorer')
    st.image(os.path.join('graphs','Top_run_scorer_team.png'))

    st.header('Top Wicket Taker')
    st.image(os.path.join('graphs','Top_wicket_taker_team.png'))

if action == 'Player Analysis':
    st.title('Player Analysis')

    col8, col9 = st.columns(2)
    with col8:
        player_name = st.selectbox('Select Player', all_player_names)

    response = page_process_func.player_analysis_page(match_data, ball_data, player_name)
    
    col10, col11 = st.columns(2)
    with col10:
        st.title(player_name)
    with col11:
        st.markdown('### Man of the Match')
        st.markdown('#### '+str(response['MoM']))

    st.markdown('## Batting Statistics')
    batting_stats = response['batting_stats']

    col12, col13, col14, col15 = st.columns(4)
    with col12:
        st.markdown('### Innings')
        st.markdown('#### '+str(batting_stats['Innings']))

    with col13:
        st.markdown('### Not Out')
        st.markdown('#### '+str(batting_stats['Not Out']))

    with col14:
        st.markdown('### Runs')
        st.markdown('#### '+str(batting_stats['Runs']))

    with col15:
        st.markdown('### Highest Score')
        st.markdown('#### '+str(batting_stats['Highest Score']))


    st.write('')

    col16, col17, col18, col19 = st.columns(4)
    with col16:
        st.markdown('### Average')
        st.markdown('#### '+str(batting_stats['Average']))

    with col17:
        st.markdown('### Strike Rate')
        st.markdown('#### '+str(batting_stats['Strike Rate']))

    with col18:
        st.markdown('### 100s')
        st.markdown('#### '+str(batting_stats['100s']))

    with col19:
        st.markdown('### 50s')
        st.markdown('#### '+str(batting_stats['50s']))

    st.write('')

    col20, col21, col22, col23 = st.columns(4)
    with col20:
        st.markdown('### 6s')
        st.markdown('#### '+str(batting_stats['6s']))

    with col21:
        st.markdown('### 4s')
        st.markdown('#### '+str(batting_stats['4s']))

    st.write('')
    st.write('')

    st.markdown('## Bowling Statistics')
    bowling_stats = response['bowling_stats']

    col24, col25, col26, col27 = st.columns(4)
    with col24:
        st.markdown('### Innings')
        st.markdown('#### '+str(bowling_stats['Innings']))

    with col25:
        st.markdown('### Balls')
        st.markdown('#### '+str(bowling_stats['Balls']))

    with col26:
        st.markdown('### Wickets')
        st.markdown('#### '+str(bowling_stats['Wickets']))

    with col27:
        st.markdown('### Runs')
        st.markdown('#### '+str(bowling_stats['Runs']))

    st.write('')

    col28, col29, col30, col31 = st.columns(4)
    with col28:
        st.markdown('### Economy')
        st.markdown('#### '+str(bowling_stats['Economy']))

    with col29:
        st.markdown('### Average')
        st.markdown('#### '+str(bowling_stats['Average']))

    with col30:
        st.markdown('### Strike rate')
        st.markdown('#### '+str(bowling_stats['Strike rate']))

    with col31:
        st.markdown('### 5 wicket haul')
        st.markdown('#### '+str(bowling_stats['5 wicket haul']))

if action == 'Team Vs Team':
    st.title('Team Vs Team')

    col10, col11 = st.columns(2)
    with col10:
        team1 = st.selectbox('Select Team1', all_team_names)
    with col11:
        team2 = st.selectbox('Select Team2', all_team_names)

    process = st.button('Get Analysis')
    if process:
        response = page_process_func.team_vs_team_page(match_data, ball_data, team1, team2)

        if response:
            st.header('Matches Played Between Two Teams')
            st.subheader(response) 
            
            st.header('Match Won By Teams')
            st.image(os.path.join('graphs','TeamVsTeam_won.png'))

            st.header('Highest/Lowest Scores')
            st.image(os.path.join('graphs','TeamVsTeam_HighLow.png'))

        else:
            st.error('No records found')

if action == 'Insights':
    st.title('Insights')

    response = page_process_func.insight_page(match_data)

    st.image(os.path.join('graphs','toss_effect_on_match_winning.png'))
    conclude_state = 'Conclusion : ' + str(response['toss_match_relation']) + '% Toss winners were able to won the match. The toss result does not have much impact on the match result.'
    st.markdown('### ' + conclude_state)


    


