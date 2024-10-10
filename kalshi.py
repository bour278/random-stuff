import streamlit as st
import pandas as pd

# Initialize an empty DataFrame to store user inputs
data = pd.DataFrame(columns=["Name", "Type", "Value"])

# Title of the app
st.title("Market Maker App")

# Button to become a market maker
st.button("Become a Market Maker")

# Display bid and ask buttons with input prompts
if st.button("Bid"):
    name = st.text_input("Enter your name for Bid:")
    if name:
        # Capture the bid value and store it in the DataFrame
        bid_value = st.number_input("Enter Bid Value:", min_value=0.0)
        if bid_value:
            data = data.append({"Name": name, "Type": "Bid", "Value": bid_value}, ignore_index=True)

if st.button("Ask"):
    name = st.text_input("Enter your name for Ask:")
    if name:
        # Capture the ask value and store it in the DataFrame
        ask_value = st.number_input("Enter Ask Value:", min_value=0.0)
        if ask_value:
            data = data.append({"Name": name, "Type": "Ask", "Value": ask_value}, ignore_index=True)

# Display the DataFrame
st.write(data)
