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
        .title {color: #FF6B35;font-size: 3em;font-weight: bold;margin-bottom: 1em;}
        .stButton>button {background-color: #FF6B35;color: white;}
        .stButton>button:hover {background-color: #FF8C61;}
        div[data-testid="stSelectbox"] label {color: #FF6B35;}
        .section-header {color: #FF6B35;font-size: 1.5em;font-weight: bold;margin-top: 1em;}
    </style>
    <div class="title">RateHub 🍦</div>
""", unsafe_allow_html=True)

BML_COL = "BML 👨‍🚀"
J_COL = "Q Monkey 🐵"
VB_COL = "Rich Vish 💂‍♂️"
DISPLAY_COLUMNS = [BML_COL, J_COL, VB_COL]
STORAGE_COLUMNS = ['BML', 'J', 'VB']
RATINGS_FILE = 'ratings.pkl'

def init_session_state():
    if 'daily_votes' not in st.session_state:
        st.session_state['daily_votes'] = {}
    if 'historical_data' not in st.session_state:
        st.session_state['historical_data'] = pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS)
        st.session_state['historical_data'].set_index('Date', inplace=True)

def load_data():
    try:
        if os.path.exists(RATINGS_FILE):
            with open(RATINGS_FILE, 'rb') as f:
                data = pickle.load(f)
                if not isinstance(data, pd.DataFrame):
                    return pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS).set_index('Date')
                if 'Date' not in data.index.name:
                    data.set_index('Date', inplace=True)
                return data
        return pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS).set_index('Date')
    except Exception:
        return pd.DataFrame(columns=['Date'] + STORAGE_COLUMNS).set_index('Date')

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

def calculate_daily_rating():
    votes = st.session_state['daily_votes'].get(current_date, [])
    if not votes:
        return {'BML': 0, 'J': 0, 'VB': 0}
    
    ratings = {}
    for person in ['BML', 'J', 'VB']:
        person_votes = [vote[person] for vote in votes]
        avg = sum(person_votes) / len(person_votes)
        ratings[person] = min(2, max(0, round(avg)))
    return ratings

init_session_state()
current_date = datetime.now().date().strftime('%Y-%m-%d')
st.session_state['historical_data'] = load_data()

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
    if current_date not in st.session_state['daily_votes']:
        st.session_state['daily_votes'][current_date] = []
    
    vote = {'BML': bml_vote, 'J': j_vote, 'VB': vb_vote}
    st.session_state['daily_votes'][current_date].append(vote)
    
    current_ratings = calculate_daily_rating()
    st.session_state['historical_data'].loc[current_date] = [
        current_ratings['BML'],
        current_ratings['J'],
        current_ratings['VB']
    ]
    
    save_data(st.session_state['historical_data'])
    st.success('Vote submitted successfully!')
    st.rerun()

st.markdown('<div class="section-header">Today\'s Current Ratings</div>', unsafe_allow_html=True)
current_ratings = calculate_daily_rating()
current_df = pd.DataFrame([{
    BML_COL: current_ratings['BML'],
    J_COL: current_ratings['J'],
    VB_COL: current_ratings['VB']
}])

styled_current = current_df.style.applymap(get_color, subset=DISPLAY_COLUMNS)
st.dataframe(styled_current)

daily_votes = st.session_state['daily_votes'].get(current_date, [])
st.write(f"Total votes today: {len(daily_votes)}")

if not daily_votes:
    st.info("No votes submitted yet today")

st.markdown('<div class="section-header">Voting Trends (Last 10 Days)</div>', unsafe_allow_html=True)

if not st.session_state['historical_data'].empty:
    df = st.session_state['historical_data'].copy()
    df = df.sort_index(ascending=True).tail(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['BML'],
        mode='lines+markers+text',
        name='BML',
        text=['👨‍🚀'] * len(df),
        textposition="middle center",
        textfont=dict(size=20),
        line=dict(color='#1f77b4'),
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['J'],
        mode='lines+markers+text',
        name='Q Monkey',
        text=['🐵'] * len(df),
        textposition="middle center",
        textfont=dict(size=20),
        line=dict(color='#ff7f0e'),
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['VB'],
        mode='lines+markers+text',
        name='Rich Vish',
        text=['💂‍♂️'] * len(df),
        textposition="middle center",
        textfont=dict(size=20),
        line=dict(color='#2ca02c'),
        showlegend=True
    ))
    
    fig.update_layout(
        title='Last 10 Days Rating History',
        xaxis_title="Date",
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

if not st.session_state['historical_data'].empty:
    df_display = st.session_state['historical_data'].copy()
    df_display.index.name = 'Date'
    df_display = df_display.rename(columns=dict(zip(STORAGE_COLUMNS, DISPLAY_COLUMNS)))
    styled_df = df_display.style.applymap(get_color, subset=DISPLAY_COLUMNS)
    st.dataframe(styled_df)
else:
    st.write("No historical data available yet.")

st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 60000);
    </script>
    """, unsafe_allow_html=True)
