def send_email(recipient, subject):
    outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    
    # Convert dataframe to HTML
    html_table = summary_df.to_html(classes='dataframe', escape=False)
    
    # Apply inline styles to headers
    import re
    
    def style_header(match):
        header_text = match.group(1)
        if header_text == summary_df.index.name or header_text == '':  # Index header
            return f'<th style="background-color: yellow; border: 1px solid black; padding: 8px; text-align: left;">{header_text}</th>'
        elif header_text.startswith('Q'):  # Headers starting with Q
            return f'<th style="color: blue; border: 1px solid black; padding: 8px; text-align: left;">{header_text}</th>'
        else:  # Other headers
            return f'<th style="color: brown; border: 1px solid black; padding: 8px; text-align: left;">{header_text}</th>'
    
    html_table = re.sub(r'<th.*?>(.+?)</th>', style_header, html_table)
    
    # Style for the table and cells
    table_style = 'style="border-collapse: collapse; width: 100%;"'
    cell_style = 'style="border: 1px solid black; padding: 8px; text-align: left;"'
    
    html_table = html_table.replace('<table', f'<table {table_style}')
    html_table = html_table.replace('<td', f'<td {cell_style}')
    
    mail.HTMLBody = f"<html><body>{html_table}</body></html>"
    mail.Send()

send_email("vish.bordia@rbccm.com", "Funding Balance")
