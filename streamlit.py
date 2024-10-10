import streamlit as st
import pandas as pd
import numpy as np

# Create a sample DataFrame
df = pd.DataFrame({
    'A': np.random.rand(10),
    'B': np.random.rand(10),
    'C': np.random.rand(10)
})

# Display the DataFrame
st.write("Original DataFrame:")
st.dataframe(df)

# Create a dropdown list of column names
selected_column = st.selectbox("Select a column to display:", df.columns)

# Display the selected column
st.write(f"Selected column: {selected_column}")
st.dataframe(df[[selected_column]])
