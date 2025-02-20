import pandas as pd

# Read data from dataset.csv in the DATA folder into dataframe df
df = pd.read_csv('../DATA/dataset.csv', delimiter=',')

# Print top 5 rows of dataframe
print(df.head())
