import pandas as pd
import numpy as np

# Read from the patternset1.csv and MAIN_dataset.xlsx and then update the columns UUID, and  Main Bug Pattern 1 through 7
def update_dataset_UUID_pattern():
    df_pattern = pd.read_csv('../DATA/patternset1.csv', delimiter=',')
    # Read from xlsx file
    df = pd.read_excel('../DATA/MAIN_dataset.xlsx')

    # Read from the df dataframe each line, and get the UUID and Main Bug Pattern 1, 2, 3, through 7 for a specific index
    # and then insert it into the df dataframe at the corresponding index

    for index, row in df.iterrows():
        index = row['Index']
        uuid = row['UUID']
        row1 = row['Main_Bug_Pattern_1']
        row2 = row['Main_Bug_Pattern_2']
        row3 = row['Main_Bug_Pattern_3']
        row4 = row['Main_Bug_Pattern_4']
        row5 = row['Main_Bug_Pattern_5']
        row6 = row['Main_Bug_Pattern_6']
        row7 = row['Main_Bug_Pattern_7']
        df_pattern.loc[df_pattern['Index'] == index, 'UUID'] = uuid
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_1'] = row1
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_2'] = row2
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_3'] = row3
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_4'] = row4
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_5'] = row5
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_6'] = row6
        df_pattern.loc[df_pattern['Index'] == index, 'Main_Bug_Pattern_7'] = row7

    df_pattern.to_csv('../DATA/patternset2.csv', index=False)


def update_owner():
    df_owner = pd.read_csv('../DATA/repo-owner.csv', delimiter=',')
    df_pattern = pd.read_csv('../DATA/patternset.csv', delimiter=',')

    # Read from the df_owner dataframe each line, and get the repo owner for a specific repo name and then insert
    # it into the df_pattern dataframe at the corresponding repo name

    for index, row in df_owner.iterrows():
        repo_name = row['name']
        owner = row['owner']
        df_pattern.loc[df_pattern['Repository'] == repo_name, 'Owner'] = owner

    df_pattern.to_csv('../DATA/patternset1.csv', index=False)

def main():
    # update_owner()
    update_dataset_UUID_pattern()

if __name__ == '__main__':
    main()
