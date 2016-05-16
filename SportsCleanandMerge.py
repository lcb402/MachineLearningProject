
import pandas as pd
import numpy as np


# load USDC + weather
df_USDC_WEATHER = pd.read_table(merged)


# load district lookup tables
df_MLB_lookup = pd.read_csv("MLB_lookup.csv",index_col=False)
df_NBA_lookup = pd.read_csv("NBA_lookup.csv",index_col=False)
df_NFL_lookup = pd.read_csv("NFL_lookup.csv",index_col=False)
df_NHL_lookup = pd.read_csv("NHL_lookup.csv",index_col=False)
df_CFB_lookup = pd.read_csv("CFB_lookup.csv",index_col=False)


# clean lookup data
df_MLB_lookup['Team'] = df_MLB_lookup['MLB'].replace({' ':''},regex=True)
df_NBA_lookup['Team'] = df_NBA_lookup['NBA'].replace({' ':''},regex=True)
df_NFL_lookup['Team'] = df_NFL_lookup['NFL'].replace({' ':''},regex=True)
df_NHL_lookup['Team'] = df_NHL_lookup['NHL'].replace({' ':''},regex=True)
df_MLB_lookup = df_MLB_lookup.drop('MLB', 1)
df_NBA_lookup = df_NBA_lookup.drop('NBA', 1)
df_NFL_lookup = df_NFL_lookup.drop('NFL', 1)
df_NHL_lookup = df_NHL_lookup.drop('NHL', 1)


# load professional sports data
df_MLB = pd.read_csv("MLB.csv",index_col=False)
df_NBA = pd.read_csv("NBA.csv",index_col=False)
df_NFL = pd.read_csv("NFL.csv",index_col=False)
df_NHL = pd.read_csv("NHL.csv",index_col=False)


# Clean NFL Date
df_NFL['Date'] = df_NFL['Date'].str.lstrip('Monday ')
df_NFL['Date'] = df_NFL['Date'].str.lstrip('Thursday ')
df_NFL['Date'] = df_NFL['Date'].str.lstrip('Friday ')
df_NFL['Date'] = df_NFL['Date'].str.lstrip('Saturday ')
df_NFL['Date'] = df_NFL['Date'].str.lstrip('Sunday ')
df_NFL['Date'] = df_NFL['Date'].str.lstrip('turday ')
df_NFL['Date'] = df_NFL['Date'].str.lstrip('Night ')
fmt = '%Y-%m-%d'


# load college football data
df_CFB = pd.read_csv("CFB/cfb1990.csv",index_col=False)
CFB_years = range(1991,2013)
for i in CFB_years:
    filename = "CFB/cfb"+ str(i) + ".csv"
    df_tmp = pd.read_csv(filename,index_col=False)
    df_CFB = pd.concat([df_CFB,df_tmp])
df_CFB.head()


# clean and merge MLB Day-Of data
df = df_MLB
df_lookup = df_MLB_lookup

df['Team'] = df['Team'].replace({' ':''},regex=True)

# Day-Of DataFrame
df_Day_Of = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','MLB_Field','MLB_Game'])
df_Day_Of['Team'] = df['Team']
df_Day_Of['Date'] = pd.to_datetime(df['Date'])
df_Day_Of['MLB_Field'] = df['FIELD'].replace({'HOME':1,'AWAY':0},regex=True)
df_Day_Of['MLB_Game'] = 1
df_Day_Of = df_Day_Of.merge(df_lookup,how='left',on='Team')
df_Day_Of = df_Day_Of.drop('Team', 1)

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_Of,how='left',on=['Date','DISTRICT'])


# clean and merge MLB Day-After data
df_Day_After = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','Field','Game','MLB_Scored','MLB_Allowed','MLB_Margin','MLB_Result'])
df_Day_After['Team'] = df['Team']
df_Day_After['Date'] = pd.to_datetime(df['Date'])
df_Day_After['Date'] = pd.DatetimeIndex(df_Day_After['Date']) + pd.DateOffset(1)
df_Day_After['MLB_Next_Day_Field'] = df['FIELD'].replace({'HOME':1,'AWAY':0},regex=True)
df_Day_After['MLA_Next_Day_Game'] = 1
df_Day_After['MLB_Scored'] = df['Runs Scr']
df_Day_After['MLB_Allowed'] = df['Runs Alw']
df_Day_After['MLB_Margin'] = df['Margin']
df_Day_After['MLB_Result'] = df['Game Result'].replace({'W':1,'L':0},regex=True)

df_Day_After.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_After,how='left',on=['Date','DISTRICT'])


# clean and merge NBA Day-Of data
df = df_NBA
df_lookup = df_NBA_lookup



df['Team'] = df['Team'].replace({' ':''},regex=True)

# Day-Of DataFrame
df_Day_Of = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','NBA_Field','NBA_Game'])
df_Day_Of['Team'] = df['Team']
df_Day_Of['Date'] = pd.to_datetime(df['Date'])
df_Day_Of['NBA_Field'] = df['FIELD'].replace({'HOME':1,'ROAD':0},regex=True)
df_Day_Of['NBA_Game'] = 1
df_Day_Of = df_Day_Of.merge(df_lookup,how='left',on='Team')
df_Day_Of = df_Day_Of.drop('Team', 1)

df_Day_Of.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_Of,how='left',on=['Date','DISTRICT'])


# clean and merge MLB Day-After data
df_Day_After = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','Field','Game','NBA_Scored','NBA_Allowed','NBA_Margin','NBA_Result'])
df_Day_After['Team'] = df['Team']
df_Day_After['Date'] = pd.to_datetime(df['Date'])
df_Day_After['Date'] = pd.DatetimeIndex(df_Day_After['Date']) + pd.DateOffset(1)
df_Day_After['NBA_Next_Day_Field'] = df['FIELD'].replace({'HOME':1,'ROAD':0},regex=True)
df_Day_After['NBA_Next_Day_Game'] = 1
df_Day_After['NBA_Scored'] = df['Pts Scr']
df_Day_After['NBA_Allowed'] = df['Pts Alw']
df_Day_After['NBA_Margin'] = df['Pts Scr'] - df['Pts Alw']
df_Day_After['NBA_Result'] = df['Game Result'].replace({'W':1,'L':0},regex=True)

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_After,how='left',on=['Date','DISTRICT'])


# clean and merge NBA Day-Of data
df = df_NFL
df_lookup = df_NFL_lookup

df['Team'] = df['Team'].replace({' ':''},regex=True)

# Day-Of DataFrame
df_Day_Of = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','NFL_Field','NFL_Game'])
df_Day_Of['Team'] = df['Team']
df_Day_Of['Date'] = pd.to_datetime(df['Date'])
df_Day_Of['NFL_Field'] = df['FIELD'].replace({'HOME':1,'AWAY':0},regex=True)
df_Day_Of['NFL_Game'] = 1
df_Day_Of = df_Day_Of.merge(df_lookup,how='left',on='Team')
df_Day_Of = df_Day_Of.drop('Team', 1)

df_Day_Of.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_Of,how='left',on=['Date','DISTRICT'])


# clean and merge NFL Day-After data
df_Day_After = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','NFL_Next_Day_Field','NFL_Next_Day_Game','NFL_Scored','NFL_Allowed','NFL_Margin','NFL_Result'])
df_Day_After['Team'] = df['Team']
df_Day_After['Date'] = pd.to_datetime(df['Date'])
#df_Day_After['Date'] = pd.DatetimeIndex(df_Day_After['Date']) + pd.DateOffset(1)
df_Day_After['NFL_Next_Day_Field'] = df['FIELD'].replace({'HOME':1,'ROAD':0},regex=True)
df_Day_After['NFL_Next_Day_Game'] = 1
df_Day_After['NFL_Scored'] = df['Pts Scr']
df_Day_After['NFL_Allowed'] = df['Pts Alw']
df_Day_After['NFL_Margin'] = df['Margin']
df_Day_After['NFL_Result'] = df['Game Result'].replace({'W':1,'L':0},regex=True)

df_Day_After.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_After,how='left',on=['Date','DISTRICT'])


# clean CFB data


# clean and merge NHL Day-Of data
df = df_NHL
df_lookup = df_NHL_lookup

df['Team'] = df['Team'].replace({' ':''},regex=True)

# Day-Of DataFrame
df_Day_Of = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','NFL_Field','NFL_Game'])
df_Day_Of['Team'] = df['Team']
df_Day_Of['Date'] = pd.to_datetime(df['Date'])
df_Day_Of['NFL_Field'] = df['FIELD'].replace({'HOME':1,'ROAD':0},regex=True)
df_Day_Of['NFL_Game'] = 1
df_Day_Of = df_Day_Of.merge(df_lookup,how='left',on='Team')
df_Day_Of = df_Day_Of.drop('Team', 1)

df_Day_Of.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_Of,how='left',on=['Date','DISTRICT'])


df.head()


# clean and merge NHL Day-After data
df_Day_After = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','NHL_Next_Day_Field','NHL_Next_Day_Game','NHL_Scored','NHL_Allowed','NHL_Margin','NHL_Result'])
df_Day_After['Team'] = df['Team']
df_Day_After['Date'] = pd.to_datetime(df['Date'])
df_Day_After['Date'] = pd.DatetimeIndex(df_Day_After['Date']) + pd.DateOffset(1)
df_Day_After['NHL_Next_Day_Field'] = df['FIELD'].replace({'HOME':1,'ROAD':0},regex=True)
df_Day_After['NHL_Next_Day_Game'] = 1
df_Day_After['NHL_Scored'] = df['Pts Scr']
df_Day_After['NHL_Allowed'] = df['Pts Alw']
df_Day_After['NHL_Margin'] = df['Pts Scr'] - df['Pts Alw']
df_Day_After['NHL_Result'] = df['Game Result'].replace({'W':1,'L':0,'T':0.5},regex=True)

df_Day_After.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_After,how='left',on=['Date','DISTRICT'])


df_CFB = df_CFB.drop(df_CFB['Rk'] =='Rk')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('(')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('1')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('2')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('3')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('4')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('5')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('6')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('7')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('8')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('9')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('9')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('0')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('1')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('2')
df_CFB['Winner/Tie'] = df_CFB['Winner/Tie'].str.lstrip('3')
df_CFB['Winner/Tie'] = df_CFB['Loser/Tie'].str.lstrip(')')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('(')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('1')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('2')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('3')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('4')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('5')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('6')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('7')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('8')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('9')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('9')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('0')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('1')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('2')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip('3')
df_CFB['Loser/Tie'] = df_CFB['Loser/Tie'].str.lstrip(')')
df_CFB.head()


# clean and merge CFB Winner Day-Of data
df = df_CFB
df = df.reset_index()
df_lookup = df_CFB_lookup
df_lookup = df_lookup.rename(columns={'CFB': 'Team'})

df = df.rename(columns={'Winner/Tie': 'Team'})
df['Team'] = df['Team'].replace({' ':''},regex=True)

# Day-Of DataFrame
df_Day_Of = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','CFB_Game'])
df_Day_Of['Team'] = df['Team']
df_Day_Of['Date'] = pd.to_datetime(df['Date'])
#df_Day_Of['CFB_Field'] = df['FIELD'].replace({'@':0,'NaN':1},regex=True)
df_Day_Of['CFB_Game'] = 1
df_Day_Of = df_Day_Of.merge(df_lookup,how='left',on='Team')
df_Day_Of = df_Day_Of.drop('Team', 1)
df = df.drop('Team',1)

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_Of,how='left',on=['Date','DISTRICT'])


# clean and merge CFB Loser Day-Of data
df = df_CFB
df = df.reset_index()
df_lookup = df_CFB_lookup
df_lookup = df_lookup.rename(columns={'CFB': 'Team'})

df = df.rename(columns={'Loser/Tie': 'Team'})
df['Team'] = df['Team'].replace({' ':''},regex=True)

# Day-Of DataFrame
df_Day_Of = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','CFB_Game'])
df_Day_Of['Team'] = df['Team']
df_Day_Of['Date'] = pd.to_datetime(df['Date'])
#df_Day_Of['CFB_Field'] = df['FIELD'].replace({'@':0,'NaN':1},regex=True)
df_Day_Of['CFB_Game'] = 1
df_Day_Of = df_Day_Of.merge(df_lookup,how='left',on='Team')
df_Day_Of = df_Day_Of.drop('Team', 1)
df = df.drop('Team',1)

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_Of,how='left',on=['Date','DISTRICT'])


# clean and merge CFB Winner Day-After data
df = df_CFB
df = df.reset_index()
df_lookup = df_CFB_lookup
df_lookup = df_lookup.rename(columns={'CFB': 'Team'})

df_Day_After = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','CFB_Next_Day_Game','CFB_Scored','CFB_Allowed','CFB_Margin','CFB_Result'])
df_Day_After['Team'] = df['Team']
df_Day_After['Date'] = pd.to_datetime(df['Date'])
df_Day_After['Date'] = pd.DatetimeIndex(df_Day_After['Date']) + pd.DateOffset(1)
#df_Day_After['CFB_Next_Day_Field'] = df['FIELD'].replace({'@':0,'NaN':1},regex=True)
df_Day_After['CFB_Next_Day_Game'] = 1
df_Day_After['CFB_Scored'] = df['Pts']
df_Day_After['CFB_Allowed'] = df['Pts.1']
df_Day_After['CFB_Margin'] = df['Pts'] - df['Pts.1']
df_Day_After['CFB_Result'] = 1

df_Day_After.head()

# Merge to USDC + Weather
df_USDC_WEATHER = df_USDC_WEATHER.merge(df_Day_After,how='left',on=['Date','DISTRICT'])


# clean and merge CFB Loser Day-After data
df = df_CFB
df = df.reset_index()
df_lookup = df_CFB_lookup
df_lookup = df_lookup.rename(columns={'CFB': 'Team'})

df_Day_After = pd.DataFrame(np.nan, index=range(len(df)), columns=['Team','Date','CFB_Next_Day_Game','CFB_Scored','CFB_Allowed','CFB_Margin','CFB_Result'])
df_Day_After['Team'] = df['Team']
df_Day_After['Date'] = pd.to_datetime(df['Date'])
df_Day_After['Date'] = pd.DatetimeIndex(df_Day_After['Date']) + pd.DateOffset(1)
#df_Day_After['CFB_Next_Day_Field'] = df['FIELD'].replace({'@':0,'NaN':1},regex=True)
df_Day_After['CFB_Next_Day_Game'] = 1
df_Day_After['CFB_Scored'] = df['Pts']
df_Day_After['CFB_Allowed'] = df['Pts.1']
df_Day_After['CFB_Margin'] = df['Pts'] - df['Pts.1']
df_Day_After['CFB_Result'] = 0

df_Day_After.head()

# Merge to USDC + Weather
df_USDC_WEATHER_SPORTS = df_USDC_WEATHER.merge(df_Day_After,how='left',on=['Date','DISTRICT'])

return df_USDC_WEATHER_SPORTS

