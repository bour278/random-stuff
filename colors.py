import pandas as pd

def style_dataframe(df):
    def color_headers(col):
        if col.name == df.index.name or col.name == '':
            return ['background-color: yellow'] * len(col)
        elif str(col.name).startswith('Q'):
            return ['background-color: lightblue'] * len(col)
        else:
            return ['background-color: #D2B48C'] * len(col)  # Light brown
    
    return (df.style
              .apply(lambda _: pd.DataFrame(color_headers(_), index=_.index, columns=[_.name]))
              .set_properties(**{'text-align': 'left', 'border': '1px solid black', 'padding': '8px'})
              .set_table_styles([
                  {'selector': 'th', 'props': [('font-weight', 'bold'), ('border', '1px solid black'), ('padding', '8px')]},
                  {'selector': 'td', 'props': [('border', '1px solid black'), ('padding', '8px')]},
                  {'selector': 'th:first-child', 'props': [('width', '150px')]},  # Adjust width as needed
              ])
           )

def send_email(recipient, subject):
    outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    
    # Apply styling to the dataframe
    styled_df = style_dataframe(summary_df)
    
    # Convert styled dataframe to HTML
    html_table = styled_df.to_html(index=True)  # Ensure index is included
    
    mail.HTMLBody = f"<html><body>{html_table}</body></html>"
    mail.Send()

send_email("vish.bordia@rbccm.com", "Funding Balance")
