import win32com.client
import datetime

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the Inbox

# Define date range
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2023, 12, 31)

# Filter emails by date range
messages = inbox.Items
messages = messages.Restrict("[ReceivedTime] >= '{}' AND [ReceivedTime] <= '{}'".format(start_date.strftime("%m/%d/%Y"), end_date.strftime("%m/%d/%Y")))

# Iterate through filtered emails
for message in messages:
    print(f"Subject: {message.Subject}, Received: {message.ReceivedTime}")
