import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Q1': [1, 2],
    'A2': [3, 4],
    'Q3': [5, 6]
})

# Function to apply styles to column headers
def style_headers(s):
    return ['background-color: blue' if col.startswith('Q') else 'background-color: brown' for col in s]

# Apply styles to the DataFrame
styled_df = df.style.set_table_styles(
    {
        # Style for column headers
        'columns': [{'selector': 'th.col_heading', 'props': [('background-color', 'brown')]}],
        # Style for index header
        'index_name': [{'selector': 'th.row_heading', 'props': [('background-color', 'yellow')]}]
    }
)

# Update specific column headers based on condition
for col in df.columns:
    if col.startswith('Q'):
        styled_df = styled_df.set_table_styles(
            {col: [{'selector': f'th.col_heading.level0.{df.columns.get_loc(col)}', 'props': [('background-color', 'blue')]}]},
            overwrite=False
        )

styled_df
