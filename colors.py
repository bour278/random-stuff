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
        th:first-child {background-color: yellow;}  /* Index header */
        th[data-column^="Q"] {color: blue;}  /* Headers starting with Q */
        th:not([data-column^="Q"]):not(:first-child) {color: brown;}  /* Other headers */
    </style>
    """
    
    # Convert dataframe to HTML with custom header attributes
    html_table = summary_df.to_html(classes='dataframe', escape=False)
    html_table = html_table.replace('<th>', '<th data-column="')
    html_table = html_table.replace('</th>', '">')
    
    mail.HTMLBody = f"<html><head>{styles}</head><body>{html_table}</body></html>"
    mail.Send()

send_email("vish.bordia@rbccm.com", "Funding Balance")
