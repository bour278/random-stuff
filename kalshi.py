import streamlit as st
import pandas as pd

# Initialize session state for storing data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Name", "Type", "Value"])

# Title of the app
st.title("Market Maker App")

# Button to become a market maker
st.button("Become a Market Maker")

# Function to capture bid or ask
def capture_bid_ask(type_label):
    name = st.text_input(f"Enter your name for {type_label}:")
    if name:
        value = st.number_input(f"Enter {type_label} Value:", min_value=0.0)
        if value:
            # Append new data to the session state DataFrame
            new_entry = {"Name": name, "Type": type_label, "Value": value}
            st.session_state.data = st.session_state.data.append(new_entry, ignore_index=True)
            st.success(f"{type_label} captured successfully!")

# Display bid and ask buttons with input prompts
if st.button("Bid"):
    capture_bid_ask("Bid")

if st.button("Ask"):
    capture_bid_ask("Ask")

# Display the DataFrame
st.write(st.session_state.data)
