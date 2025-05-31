#%%

'''
question: Thailand tends to spend or invest in their health more or less?
'''

import pandas as pd
df = pd.read_csv('health_financing_indicators_tha.csv')
df

#%%
df.info()
df.describe()
df.head()
df.isna().all()

#%%
# delete the first row
df = df.iloc[1:].reset_index(drop=True)
df

#%%
# check what is written in the column that mostly have NaN
for col in df.columns:
    non_null_values = df[col].dropna().unique()
    if len(non_null_values) <= 5:
        print(f"Column: {col}")
        print(f"Non-null values: {non_null_values}\n")


#%% 
# delete unrelated or unused columns
cols_del = ['GHO (URL)', 'Low', 'High', 'DIMENSION (TYPE)', 'DIMENSION (CODE)', 'DIMENSION (NAME)']
df.drop(columns=cols_del, inplace=True)
df
# %%
# check if there is any NaN left in the column
df.isna().any()
# result: no NaN anymore.

#%%
# rename columns
df.rename(columns={
    'GHO (CODE)': 'Indicator_code',
    'GHO (DISPLAY)': 'Indicator_name',
    'YEAR (DISPLAY)': 'Year',
    'STARTYEAR': 'Start_year',
    'ENDYEAR': 'End_year',
    'REGION (CODE)': 'Region_code',
    'REGION (DISPLAY)': 'Region',
    'COUNTRY (CODE)': 'Country_code',
    'COUNTRY (DISPLAY)': 'Country',
    'Numeric': 'Value_numeric',
    'Value': 'Value_rounded'
}, inplace=True)
df

#%% 
# view distinct indicator name in column Indicator_name
# there are 12 indicators
df['Indicator_name'].unique()
# view number of each indicator
# df['Indicator_name'].value_counts()

#%% 
# shorten indicator names
indicator_mapping = {
    'Current health expenditure (CHE) per capita in US$': 'CHE_pc',
    'External health expenditure (EXT) as percentage of current health expenditure (CHE) (%)': 'EXT_pct_CHE',
    'Domestic general government health expenditure (GGHE-D) as percentage of current health expenditure (CHE) (%)': 'GGHE_pct_CHE',
    'Domestic general government health expenditure (GGHE-D) as percentage of gross domestic product (GDP) (%)': 'GGHE_pct_GDP',
    'Domestic private health expenditure (PVT-D) per capita in US$': 'PVT_pc',
    'Domestic general government health expenditure (GGHE-D) per capita in US$': 'GGHE_pc',
    'External health expenditure (EXT) per capita in US$': 'EXT_pc',
    'Current health expenditure (CHE) as percentage of gross domestic product (GDP) (%)': 'CHE_pct_GDP',
    'Out-of-pocket expenditure as percentage of current health expenditure (CHE) (%)': 'OOP_pct_CHE',
    'Domestic general government health expenditure (GGHE-D) as percentage of general government expenditure (GGE) (%)': 'GGHE_pct_GGE',
    'Out-of-pocket expenditure (OOP) per capita in US$': 'OOP_pc',
    'Domestic private health expenditure (PVT-D) as percentage of current health expenditure (CHE) (%)': 'PVT_pct_CHE'
}

df['Indicator_name'] = df['Indicator_name'].replace(indicator_mapping).str.strip()
df

#%%
df['Indicator_name'].unique()

# %%

# change data types of numerical data.
# now, they are stored as object type.
df['Value_numeric'] = pd.to_numeric(df['Value_numeric'], errors='coerce')
df['Value_rounded'] = pd.to_numeric(df['Value_rounded'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Start_year'] = pd.to_numeric(df['Start_year'], errors='coerce')
df['End_year'] = pd.to_numeric(df['End_year'], errors='coerce')
# df['Year'] = df['Year'].astype(int)
df['Value_numeric'] = df['Value_numeric'].round(3)
df['Value_rounded'] = df['Value_rounded'].round(3)
df
df.info()

#%%
# make a new table that stores only percentage value
percent_indicators = [
    'EXT_pct_CHE',
    'GGHE_pct_CHE',
    'GGHE_pct_GDP',
    'CHE_pct_GDP',
    'OOP_pct_CHE',
    'GGHE_pct_GGE',
    'PVT_pct_CHE'
]

df_percent = df[df['Indicator_name'].isin(percent_indicators)].copy()
df_percent

#%%
# rename columns in df_percent
df_percent.rename(columns={'Value_numeric': 'Value_percent'}, inplace=True)
df_percent

#%%
# create a new table that stores only numerical value
df_numeric = df[~df['Indicator_name'].isin(percent_indicators)].copy()
df_numeric
df_numeric['Indicator_name'].unique()
df_numeric['Indicator_name'].value_counts()
df_numeric


#%% 
# convert us dollars to Thai baht
exchange_rate = 35
df_numeric['Value_baht'] = df_numeric['Value_numeric'] * exchange_rate
df_numeric


# %%
df_numeric.head()
df_percent.head()
df_numeric.describe()
df_percent.describe()




'''
create a visualization for EDA
'''

# %%
import seaborn as sns
import matplotlib.pyplot as plt

# select only indicator CHE_pc
df_che = df[df['Indicator_name'] == 'CHE_pc']

# create line plot
plt.figure(figsize=(10,6))
sns.lineplot(data=df_che, x='Year', y='Value_baht', marker='o')

plt.title("Trend of Current Health Expenditure per Capita (2000–2022)")
plt.xlabel("Year")
plt.ylabel("Health Expenditure per Capita (THB)")
plt.grid(True)
plt.tight_layout()
plt.show()


# %%
