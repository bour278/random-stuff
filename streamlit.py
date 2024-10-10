import streamlit as st
import pandas as pd
import numpy as np

# Create a sample DataFrame
df = pd.DataFrame({
    'A': np.random.randn(10),
    'B': np.random.randn(10),
    'C': np.random.randn(10)
})

# Display the original DataFrame
st.write("Original DataFrame:")
st.dataframe(df)

# Create a dropdown list of column names
selected_column = st.selectbox("Select a column to display:", df.columns)

# Display the selected column with color coding based on absolute values
st.write(f"Selected column: {selected_column}")
st.dataframe(df[[selected_column]].style.background_gradient(cmap='YlOrRd', subset=[selected_column], vmin=0, vmax=df[selected_column].abs().max()))

# Explanation of the color coding
st.write("Color Legend: Yellow (low absolute values) to Orange to Red (high absolute values)")
