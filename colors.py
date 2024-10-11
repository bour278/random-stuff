import pandas as pd

def style_dataframe(df):
    def color_headers(s):
        if s.name == df.index.name or s.name == '':
            return ['background-color: yellow'] * len(s)
        elif s.name.startswith('Q'):
            return ['color: blue'] * len(s)
        else:
            return ['color: brown'] * len(s)
    
    return (df.style
              .apply(color_headers)
              .set_properties(**{'text-align': 'left', 'border': '1px solid black', 'padding': '8px'})
              .set_table_styles([
                  {'selector': 'th', 'props': [('font-weight', 'bold'), ('border', '1px solid black'), ('padding', '8px')]},
                  {'selector': 'td', 'props': [('border', '1px solid black'), ('padding', '8px')]},
                  {'selector': 'th:first-child', 'props': [('width', '100px')]},  # Adjust the width as needed
              ])
              .hide(axis="index")  # This hides the index numbers
           )

def send_email(recipient, subject):
    outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    
    # Apply styling to the dataframe
    styled_df = style_dataframe(summary_df)
    
    # Convert styled dataframe to HTML
    html_table = styled_df.to_html()
    
    mail.HTMLBody = f"<html><body>{html_table}</body></html>"
    mail.Send()

send_email("vish.bordia@rbccm.com", "Funding Balance")
