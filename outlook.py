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


#####################################

import plotly.graph_objects as go
import pandas as pd

# Sample data dictionary
data_dict = {datetime_obj: value, ...}

# Convert to DataFrame
df = pd.DataFrame(list(data_dict.items()), columns=['Date', 'Value'])

# Plot
fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Value']))
fig.show()

######################################

import datetime as dt

# Most recent date
recent_date_avg = df[df['Date'] == df['Date'].max()]['Value'].mean()

# Recent week
one_week_ago = df['Date'].max() - pd.Timedelta(weeks=1)
recent_week_avg = df[df['Date'] >= one_week_ago]['Value'].mean()

# Recent month
one_month_ago = df['Date'].max() - pd.DateOffset(months=1)
recent_month_avg = df[df['Date'] >= one_month_ago]['Value'].mean()

# Current year quarters
current_year = df['Date'].dt.year.max()
df['Quarter'] = df['Date'].dt.to_period('Q')
quarter_avg = df[df['Date'].dt.year == current_year].groupby('Quarter')['Value'].mean()

# Create summary DataFrame
summary_df = pd.DataFrame({
    'Period': ['Recent Date', 'Recent Week', 'Recent Month'] + quarter_avg.index.tolist(),
    'Average': [recent_date_avg, recent_week_avg, recent_month_avg] + quarter_avg.tolist()
})
