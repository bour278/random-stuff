import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Q1': [1, 2],
    'A2': [3, 4],
    'Q3': [5, 6]
})

# Function to apply styles to headers
def style_headers(s):
    return ['background-color: blue' if v.startswith('Q') else 'background-color: brown' for v in s]

# Apply styles to the DataFrame
styled_df = df.style.apply_index(style_headers, axis='columns')
styled_df.set_table_styles({'index_name': {'selector': 'th.row_heading', 'props': [('background-color', 'yellow')]}})

styled_df
