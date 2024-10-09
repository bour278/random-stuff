import win32com.client
import pandas as pd
import io

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Access the 'Funding' folder in the inbox (usually index 6 is the inbox)
funding_folder = outlook.Folders.Item(1).Folders['Inbox'].Folders['Funding']

# Filter emails by date
for item in funding_folder.Items:
    if item.ReceivedTime.date() == datetime.date(2024, 10, 8):
        for attachment in item.Attachments:
            if attachment.FileName.endswith('.xlsx'):
                # Save the attachment to a temporary location
                temp_file = 'temp.xlsx'
                attachment.SaveAsFile(temp_file)
                
                # Read the Excel file into a DataFrame
                df = pd.read_excel(temp_file)
                print(df)
