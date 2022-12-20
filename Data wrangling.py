import pandas as pd

# Create a DataFrame from the first table
df1 = pd.read_csv("Un-banked bitcoin adoption/adoption_dict.csv")[1:]

# Create a DataFrame from the second table
df2 = pd.read_csv("Un-banked bitcoin adoption/banked_dict.csv")

# Merge the DataFrames on the 'Country' column
df = pd.merge(df1, df2, on='key')
df.rename(columns={'key': 'country', 'value_x': 'rank','value_y':'unbanked-percentage'}, inplace=True)

df.to_csv("Un-banked bitcoin adoption/joined_table.csv")

