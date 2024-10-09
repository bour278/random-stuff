import win32com.client
import pandas as pd
import os
from datetime import date

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Access the 'Funding' folder in the inbox
funding_folder = outlook.Folders.Item(1).Folders['Inbox'].Folders['Funding']

# Specify a directory to save the attachment temporarily
save_dir = os.path.join(os.getcwd(), "temp_files")
os.makedirs(save_dir, exist_ok=True)

# Get the email received on a specific date
for item in funding_folder.Items:
    if item.ReceivedTime.date() == date(2024, 10, 8):
        # Assume there's only one attachment and it's an Excel file
        attachment = item.Attachments.Item(1)
        
        # Save the attachment to a full path
        temp_file_path = os.path.join(save_dir, 'temp.xlsx')
        attachment.SaveAsFile(temp_file_path)
        
        # Read the Excel file into a DataFrame
        df = pd.read_excel(temp_file_path)
        print(df)
