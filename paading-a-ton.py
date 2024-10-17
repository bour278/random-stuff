import pandas as pd
import numpy as np

# Create a sample DataFrame
df = pd.DataFrame(np.random.randn(10, 4), columns=['A', 'B', 'C', 'D'])

# Define a function to style the last row
def style_last_row(row):
    if row.name == df.index[-1]:
        return ['background-color: red'] * len(row)
    else:
        return [''] * len(row)

# Apply the styling
styled_df = df.style.apply(style_last_row, axis=1)

# Display the styled DataFrame
styled_df
