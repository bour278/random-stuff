import streamlit as st
import pandas as pd
import datetime
import time
import schedule
import json
from datetime import datetime, time as dt_time
import os

# Initialize session state variables if they don't exist
if 'ratings_df' not in st.session_state:
    if os.path.exists('ratings.json'):
        # Load existing data
        with open('ratings.json', 'r') as f:
            data = json.load(f)
            st.session_state.ratings_df = pd.DataFrame(data)
    else:
        # Create empty DataFrame with required columns
        st.session_state.ratings_df = pd.DataFrame(columns=['Date', 'BML', 'J', 'VB'])

if 'last_submission_date' not in st.session_state:
    st.session_state.last_submission_date = None

def is_submission_time():
    """Check if current time is around 5:00 PM (allowing 30 minutes before and after)"""
    current_time = datetime.now().time()
    target_time = dt_time(17, 0)  # 5:00 PM
    
    # Allow submissions between 4:30 PM and 5:30 PM
    start_time = dt_time(16, 30)
    end_time = dt_time(17, 30)
    
    return start_time <= current_time <= end_time

def are_ratings_valid(bml_rating, j_rating, vb_rating):
    """Check if ratings are valid (all different and between 0-2)"""
    ratings = [bml_rating, j_rating, vb_rating]
    return len(set(ratings)) == 3 and all(0 <= r <= 2 for r in ratings)

def save_ratings():
    """Save ratings to JSON file"""
    with open('ratings.json', 'w') as f:
        json.dump(st.session_state.ratings_df.to_dict('records'), f)

def get_color(val):
    """Return color based on rating value"""
    colors = {0: 'background-color: green',
              1: 'background-color: yellow',
              2: 'background-color: red'}
    return colors.get(val, '')

def add_default_ratings():
    """Add default ratings (all 0) for today if no submission was made"""
    current_date = datetime.now().date()
    if (st.session_state.last_submission_date != current_date and 
        current_date.strftime('%Y-%m-%d') not in st.session_state.ratings_df['Date'].values):
        new_row = {
            'Date': current_date.strftime('%Y-%m-%d'),
            'BML': 0,
            'J': 0,
            'VB': 0
        }
        st.session_state.ratings_df = pd.concat([st.session_state.ratings_df, 
                                               pd.DataFrame([new_row])], 
                                               ignore_index=True)
        save_ratings()

# App title
st.title('Daily Team Rating System')

# Check if it's submission time and if ratings haven't been submitted today
current_date = datetime.now().date()
can_submit = (is_submission_time() and 
             (st.session_state.last_submission_date is None or 
              st.session_state.last_submission_date != current_date))

if can_submit:
    st.write("Please submit today's ratings (0 = Green, 1 = Yellow, 2 = Red)")
    
    # Create three columns for input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bml_rating = st.selectbox('BML Rating', options=[0, 1, 2], key='bml')
    with col2:
        j_rating = st.selectbox('J Rating', options=[0, 1, 2], key='j')
    with col3:
        vb_rating = st.selectbox('VB Rating', options=[0, 1, 2], key='vb')
    
    if st.button('Submit Ratings'):
        if are_ratings_valid(bml_rating, j_rating, vb_rating):
            # Add new ratings to DataFrame
            new_row = {
                'Date': current_date.strftime('%Y-%m-%d'),
                'BML': bml_rating,
                'J': j_rating,
                'VB': vb_rating
            }
            st.session_state.ratings_df = pd.concat([st.session_state.ratings_df, 
                                                   pd.DataFrame([new_row])], 
                                                   ignore_index=True)
            
            # Update last submission date
            st.session_state.last_submission_date = current_date
            
            # Save to file
            save_ratings()
            
            st.success('Ratings submitted successfully!')
        else:
            st.error('Invalid ratings. Each person must have a different rating (0, 1, or 2).')
else:
    if not is_submission_time():
        st.info('Ratings can only be submitted around 5:00 PM.')
        # Check if we need to add default ratings for today
        if datetime.now().time() > dt_time(17, 30):  # After 5:30 PM
            add_default_ratings()
    elif st.session_state.last_submission_date == current_date:
        st.info('Ratings have already been submitted for today.')

# Display ratings table with colored cells
if not st.session_state.ratings_df.empty:
    st.write("### Rating History")
    
    # Sort DataFrame by date in descending order
    df_display = st.session_state.ratings_df.sort_values('Date', ascending=False)
    
    # Apply color styling
    styled_df = df_display.style.applymap(get_color, subset=['BML', 'J', 'VB'])
    
    st.dataframe(styled_df)
else:
    st.write("No ratings have been submitted yet.")
