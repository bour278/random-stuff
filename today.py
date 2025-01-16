import streamlit as st
import pandas as pd
import datetime
import time
import pickle
from datetime import datetime, time as dt_time
import os

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

if 'ratings_df' not in st.session_state:
    st.session_state['ratings_df'] = pd.DataFrame(columns=['Date', 'BML', 'J', 'VB'])

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
        return pd.DataFrame(columns=['Date', 'BML', 'J', 'VB'])
    except Exception:
        return pd.DataFrame(columns=['Date', 'BML', 'J', 'VB'])

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
    bml_vote = st.selectbox('BML 👨‍🚀', options=[0, 1, 2], key='bml_vote')
with col2:
    j_vote = st.selectbox('Q Monkey 🐵', options=[0, 1, 2], key='j_vote')
with col3:
    vb_vote = st.selectbox('Rich Vish 💂‍♂️', options=[0, 1, 2], key='vb_vote')

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
    'BML 👨‍🚀': current_ratings['BML'],
    'Q Monkey 🐵': current_ratings['J'],
    'Rich Vish 💂‍♂️': current_ratings['VB']
}])

styled_current = current_df.style.applymap(get_color, subset=['BML 👨‍🚀', 'Q Monkey 🐵', 'Rich Vish 💂‍♂️'])
st.dataframe(styled_current)

st.write(f"Total votes today: {len(st.session_state['votes'])}")

if not st.session_state['votes']:
    st.info("No votes submitted yet today")

st.markdown('<div class="section-header">Rating History</div>', unsafe_allow_html=True)

historical_df = load_data()

if len(st.session_state['votes']) > 0:
    historical_df = historical_df[historical_df['Date'] != current_date]
    if not historical_df.empty:
        historical_df = historical_df.rename(columns={
            'BML': 'BML 👨‍🚀',
            'J': 'Q Monkey 🐵',
            'VB': 'Rich Vish 💂‍♂️'
        })
    historical_df = pd.concat([current_df, historical_df], ignore_index=True)
    save_df = historical_df.rename(columns={
        'BML 👨‍🚀': 'BML',
        'Q Monkey 🐵': 'J',
        'Rich Vish 💂‍♂️': 'VB'
    })
    save_data(save_df)

if not historical_df.empty:
    styled_df = historical_df.style.applymap(get_color, subset=['BML 👨‍🚀', 'Q Monkey 🐵', 'Rich Vish 💂‍♂️'])
    st.dataframe(styled_df)
else:
    st.write("No historical data available yet.")

if st.session_state['last_vote_time']:
    last_vote_date = st.session_state['last_vote_time'].date()
    if last_vote_date < datetime.now().date():
        st.session_state['votes'] = []

st.session_state['last_vote_time'] = datetime.now()

# Add auto-refresh using JavaScript
st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 60000);
    </script>
    """, unsafe_allow_html=True)
