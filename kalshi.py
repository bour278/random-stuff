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
    # Use a form to ensure inputs are captured together
    with st.form(key=f"{type_label}_form"):
        name = st.text_input(f"Enter your name for {type_label}:")
        value = st.number_input(f"Enter {type_label} Value:", min_value=0.0)
        submit_button = st.form_submit_button(label=f"Submit {type_label}")

        if submit_button and name:
            # Append new data to the session state DataFrame
            new_entry = {"Name": name, "Type": type_label, "Value": value}
            st.session_state.data = st.session_state.data.append(new_entry, ignore_index=True)
            st.success(f"{type_label} captured successfully!")

# Display bid and ask buttons with input prompts
st.subheader("Place Your Bid or Ask")
capture_bid_ask("Bid")
capture_bid_ask("Ask")

# Display the DataFrame
st.write(st.session_state.data)
