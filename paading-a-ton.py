def style_df(df):
    return df.style.set_table_styles([
        {'selector': 'th, td', 'props': [
            ('padding', '2px 5px'),
            ('white-space', 'normal'),
            ('max-width', 'none'),
            ('width', 'auto'),
            ('height', 'auto'),
            ('line-height', '1.2')
        ]},
        {'selector': 'table', 'props': [
            ('border-collapse', 'collapse'),
            ('width', '100%')
        ]}
    ])

# Apply the style to your DataFrame
styled_df = style_df(your_dataframe)

# To render the styled DataFrame as HTML
html_output = styled_df.to_html()
