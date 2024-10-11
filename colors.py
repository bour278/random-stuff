import pandas as pd
import numpy as np

# Create sample data
data = {
    'Q1 2024': np.random.rand(5),
    'Q2 2024': np.random.rand(5),
    'Aug-24': np.random.rand(5),
    'Current': np.random.rand(5)
}

df = pd.DataFrame(data)

# Define a function to color the headers
def color_headers(col_name):
    if col_name.startswith('Q'):
        return 'background-color: blue; color: white'
    else:
        return 'background-color: brown; color: white'

# Apply the styles
styled_df = df.style.set_table_styles([
    {'selector': 'th.index_name', 'props': 'background-color: yellow;'},
    {'selector': 'th.col_heading', 'props': 'text-align: center;'}
]).set_properties(**{
    'text-align': 'center',
    'border': '1px solid black'
}).set_table_styles([
    {'selector': 'th', 'props': [('font-size', '11pt')]},
    {'selector': 'td', 'props': [('font-size', '10pt')]}
]).set_table_styles([
    {'selector': f'th.col{i}', 'props': color_headers(col)}
    for i, col in enumerate(df.columns)
], overwrite=False)

# Display the styled DataFrame
styled_df
