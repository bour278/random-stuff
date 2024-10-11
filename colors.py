def send_email(recipient, subject):
    outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    
    # Custom styling for the dataframe
    styles = """
    <style>
        table {border-collapse: collapse; width: 100%;}
        th, td {border: 1px solid black; padding: 8px; text-align: left;}
        th {font-weight: bold;}
        th:first-child {background-color: yellow !important;}  /* Index header */
        th[data-column^="Q"] {color: blue !important;}  /* Headers starting with Q */
        th:not([data-column^="Q"]):not(:first-child) {color: brown !important;}  /* Other headers */
    </style>
    """
    
    # Convert dataframe to HTML
    html_table = summary_df.to_html(classes='dataframe', escape=False)
    
    # Modify the HTML to add data-column attributes to headers
    import re
    def add_data_column(match):
        return f'<th data-column="{match.group(1)}">{match.group(1)}'
    
    html_table = re.sub(r'<th.*?>(.+?)</th>', add_data_column, html_table)
    
    mail.HTMLBody = f"<html><head>{styles}</head><body>{html_table}</body></html>"
    mail.Send()

send_email("vish.bordia@rbccm.com", "Funding Balance")
