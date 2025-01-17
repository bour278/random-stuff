import streamlit as st
import pandas as pd
import datetime
import time
import pickle
from datetime import datetime, time as dt_time
import os
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="RateHub 🍦")

st.markdown("""
    <style>
        .title {
            color: #FF6B35;
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 1em;
        }
        .stButton>button {
            background-color: #FF6B35;
            color: white;
        }
        .stButton>button:hover {
            background-color: #FF8C61;
        }
        div[data-testid="stSelectbox"] label {
            color: #FF6B35;
        }
        .section-header {
            color: #FF6B35;
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 1em;
        }
    </style>
    <div class="title">RateHub 🍦</div>
""", unsafe_allow_html=True)

BML_COL = "BML 👨‍🚀"
J_COL = "Q Monkey 🐵"
VB_COL = "Rich Vish 💂‍♂️"
DISPLAY_COLUMNS = [BML_COL, J_COL, VB_COL]
STORAGE_COLUMNS = ['BML', 'J', 'VB']

if 'ratings_df' not in st.session_state:
    st.session_state['ratings_df'] = pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS)

if 'votes' not in st.session_state:
    st.session_state['votes'] = []

if 'last_vote_time' not in st.session_state:
    st.session_state['last_vote_time'] = None

RATINGS_FILE = 'ratings.pkl'

def load_data():
    try:
        if os.path.exists(RATINGS_FILE):
            with open(RATINGS_FILE, 'rb') as f:
                return pickle.load(f)
        return pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS)

def save_data(df):
    try:
        with open(RATINGS_FILE, 'wb') as f:
            pickle.dump(df, f)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def get_color(val):
    colors = {0: 'background-color: green',
              1: 'background-color: yellow',
              2: 'background-color: red'}
    return colors.get(val, '')

def calculate_ratings():
    if len(st.session_state['votes']) == 0:
        return {'BML': 0, 'J': 0, 'VB': 0}
    
    vote_counts = {'BML': [], 'J': [], 'VB': []}
    for vote in st.session_state['votes']:
        for person in ['BML', 'J', 'VB']:
            vote_counts[person].append(vote[person])
    
    ratings = {}
    for person in vote_counts:
        if vote_counts[person]:
            avg = sum(vote_counts[person]) / len(vote_counts[person])
            ratings[person] = min(2, max(0, round(avg)))
        else:
            ratings[person] = 0
    
    return ratings

current_date = datetime.now().date().strftime('%Y-%m-%d')

st.markdown('<div class="section-header">Submit Your Vote</div>', unsafe_allow_html=True)
st.write("Rate each person (0 = Green, 1 = Yellow, 2 = Red)")

col1, col2, col3 = st.columns(3)

with col1:
    bml_vote = st.selectbox(BML_COL, options=[0, 1, 2], key='bml_vote')
with col2:
    j_vote = st.selectbox(J_COL, options=[0, 1, 2], key='j_vote')
with col3:
    vb_vote = st.selectbox(VB_COL, options=[0, 1, 2], key='vb_vote')

if st.button('Submit Vote'):
    vote = {
        'BML': bml_vote,
        'J': j_vote,
        'VB': vb_vote,
        'timestamp': datetime.now()
    }
    st.session_state['votes'].append(vote)
    st.success('Vote submitted successfully!')
    st.rerun()

st.markdown('<div class="section-header">Today\'s Current Ratings</div>', unsafe_allow_html=True)

current_ratings = calculate_ratings()

current_df = pd.DataFrame([{
    'Date': current_date,
    BML_COL: current_ratings['BML'],
    J_COL: current_ratings['J'],
    VB_COL: current_ratings['VB']
}])

styled_current = current_df.style.applymap(get_color, subset=DISPLAY_COLUMNS)
st.dataframe(styled_current)

st.write(f"Total votes today: {len(st.session_state['votes'])}")

if not st.session_state['votes']:
    st.info("No votes submitted yet today")

st.markdown('<div class="section-header">Voting Trends</div>', unsafe_allow_html=True)

if len(st.session_state['votes']) > 0:
    vote_numbers = list(range(1, len(st.session_state['votes']) + 1))
    x = vote_numbers if len(vote_numbers) < 10 else np.log10(vote_numbers)
    x_title = "Number of Votes" if len(vote_numbers) < 10 else "Number of Votes (log scale)"
    
    fig = go.Figure()
    
    bml_votes = [vote['BML'] for vote in st.session_state['votes']]
    fig.add_trace(go.Scatter(
        x=x,
        y=bml_votes,
        mode='lines+markers+text',
        name='BML',
        text=['👨‍🚀'] * len(bml_votes),
        textposition="middle center",
        textfont=dict(size=20),
        line=dict(color='#1f77b4'),
        showlegend=True
    ))
    
    j_votes = [vote['J'] for vote in st.session_state['votes']]
    fig.add_trace(go.Scatter(
        x=x,
        y=j_votes,
        mode='lines+markers+text',
        name='Q Monkey',
        text=['🐵'] * len(j_votes),
        textposition="middle center",
        textfont=dict(size=20),
        line=dict(color='#ff7f0e'),
        showlegend=True
    ))
    
    vb_votes = [vote['VB'] for vote in st.session_state['votes']]
    fig.add_trace(go.Scatter(
        x=x,
        y=vb_votes,
        mode='lines+markers+text',
        name='Rich Vish',
        text=['💂‍♂️'] * len(vb_votes),
        textposition="middle center",
        textfont=dict(size=20),
        line=dict(color='#2ca02c'),
        showlegend=True
    ))
    
    fig.update_layout(
        title='Voting Trends Over Time',
        xaxis_title=x_title,
        yaxis_title='Rating',
        yaxis=dict(
            tickmode='array',
            ticktext=['Green 🟩', 'Yellow 🟨', 'Red 🟥'],
            tickvals=[0, 1, 2],
            range=[-0.5, 2.5]
        ),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#FF6B35'),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.8)'
        )
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">Rating History</div>', unsafe_allow_html=True)

historical_df = load_data()

if len(st.session_state['votes']) > 0:
    historical_df = historical_df[historical_df['Date'] != current_date]
    
    if not historical_df.empty:
        name_mapping = dict(zip(STORAGE_COLUMNS, DISPLAY_COLUMNS))
        historical_df = historical_df.rename(columns=name_mapping)
    
    historical_df = pd.concat([current_df, historical_df], ignore_index=True)
    historical_df = historical_df.sort_values('Date', ascending=False).drop_duplicates(subset=['Date']).reset_index(drop=True)
    
    save_df = historical_df.copy()
    reverse_mapping = dict(zip(DISPLAY_COLUMNS, STORAGE_COLUMNS))
    save_df = save_df.rename(columns=reverse_mapping)
    save_data(save_df)

if not historical_df.empty:
    styled_df = historical_df.style.applymap(get_color, subset=DISPLAY_COLUMNS)
    st.dataframe(styled_df)
else:
    st.write("No historical data available yet.")

if st.session_state['last_vote_time']:
    last_vote_date = st.session_state['last_vote_time'].date()
    if last_vote_date < datetime.now().date():
        st.session_state['votes'] = []

st.session_state['last_vote_time'] = datetime.now()

st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 60000);
    </script>
    """, unsafe_allow_html=True)
