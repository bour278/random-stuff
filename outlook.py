import win32com.client
import pandas as pd
import io

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Access the 'Funding' folder in the inbox
funding_folder = outlook.Folders.Item(1).Folders['Inbox'].Folders['Funding']

# Get the email received on a specific date
for item in funding_folder.Items:
    if item.ReceivedTime.date() == datetime.date(2024, 10, 8):
        # Assume there's only one attachment and it's an Excel file
        attachment = item.Attachments.Item(1)
        
        # Save the attachment to a temporary location
        temp_file = 'temp.xlsx'
        attachment.SaveAsFile(temp_file)
        
        # Read the Excel file into a DataFrame
        df = pd.read_excel(temp_file)
        print
