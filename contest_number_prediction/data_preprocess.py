import pandas as pd
from datetime import datetime

df = pd.read_csv('all_contest.csv')
df_filtered = df[df['Name'].str.match(r'^Codeforces (Beta )?Round \d+.*')].copy()
df_filtered['Round'] = df_filtered['Name'].str.extract(r'^Codeforces (Beta )?Round (\d+)', expand=False)[1].astype(int)
df_filtered['Month'] = pd.to_datetime(df_filtered['Month'], format='%B').dt.month
df_filtered['Day'] = df_filtered['Date'].astype(int)
df_filtered['Year'] = df_filtered['Year'].astype(int)
df_filtered['ContestDate'] = pd.to_datetime(df_filtered[['Year', 'Month', 'Day']])
start_date = datetime(2016, 1, 1)
df_filtered['Days'] = (df_filtered['ContestDate'] - start_date).dt.days
df_result = df_filtered[['Round', 'Days']]
df_result.to_csv('output.csv', index=False)