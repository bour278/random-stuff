import pandas as pd

def style_dataframe(df):
    def color_headers(col):
        # Style for headers
        if str(col.name).startswith('Q'):
            return ['background-color: lightblue'] * len(col)
        else:
            return ['background-color: #D2B48C'] * len(col)  # Light brown

    def color_index(idx):
        # Style for index
        return ['background-color: yellow'] * len(idx)

    return (df.style
              .apply(color_headers, axis=0)  # Apply to headers
              .apply(color_index, axis=1)    # Apply to index
              .set_properties(**{'text-align': 'left', 'border': '1px solid black', 'padding': '8px'})
              .set_table_styles([
                  {'selector': 'th', 'props': [('font-weight', 'bold'), ('border', '1px solid black'), ('padding', '8px')]},
                  {'selector': 'td', 'props': [('border', '1px solid black'), ('padding', '8px')]},
                  {'selector': 'th:first-child', 'props': [('width', '150px')]},  # Adjust width as needed
              ])
           )

def send_email(recipient, subject, summary_df):
    import win32com.client as win32
    import pythoncom
    
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

# Example usage:
# summary_df = pd.DataFrame(...)  # Your DataFrame here
# send_email("vish.bordia@rbccm.com", "Funding Balance", summary_df)
