import win32com.client
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime

def find_and_parse_email():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    
    # Access the "Prelim" folder
    prelim_folder = None
    for folder in outlook.Folders.Item(1).Folders:
        if folder.Name == "Prelim":
            prelim_folder = folder
            break
    
    if not prelim_folder:
        print("Prelim folder not found")
        return None

    # Search for emails with the subject pattern
    messages = prelim_folder.Items
    messages.Sort("[ReceivedTime]", True)
    
    for message in messages:
        if re.match(r"Prelim pl \d{1,2}/\d{1,2}", message.Subject):
            # Check this email and its replies
            current_message = message
            while current_message:
                if "PL by LHU" in current_message.HTMLBody:
                    # Extract table data
                    df = extract_table_data(current_message.HTMLBody)
                    if df is not None:
                        return df
                
                # Move to the next reply
                if current_message.ResponseStatus == 5:  # 5 means it has been replied to
                    current_message = current_message.GetAssociatedItem()
                else:
                    break
    
    print("No matching email found")
    return None

def extract_table_data(html_body):
    soup = BeautifulSoup(html_body, 'html.parser')
    
    # Find the paragraph containing "PL by LHU"
    pl_by_lhu_p = soup.find('p', string=lambda text: 'PL by LHU' in text if text else False)
    
    if pl_by_lhu_p:
        # Find the next table after this paragraph
        table = pl_by_lhu_p.find_next('table')
        
        if table:
            # Extract table data
            data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                data.append([ele.text.strip() for ele in cols])
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
    
    return None

if __name__ == "__main__":
    df = find_and_parse_email()
    if df is not None:
        print(df)
    else:
        print("No data found")
