# This file contains code to determine whether there is RADARSAT-1 coverage
# for the locations and dates given in lakeice-measurements.xlsx.

import pandas as pd

def get_coord_1(row):
    row = str(row)
    x = row.split('(')[1].split(' ')[0]
    return x

def get_coord_2(row):
    row = str(row)
    y = row.split('(')[1].split(' ')[1].split(')')[0]
    return y

def get_year(row):
    if type(row) == str:
        return row.split('-')[0]
    return 0
def get_month(row):
    if type(row) == str:
        return row.split('-')[1]
    return 0

df = pd.read_excel("lakeice-measurements.xlsx") # Reads the data

df_r1 = pd.read_csv('r1_data_with_aws.csv') # Reads the R1 metadata file

df_r1['long'] = [get_coord_1(row) for row in df_r1['scene-centre']] # Changes the coordinates to separate columns
df_r1['lat'] = [get_coord_2(row) for row in df_r1['scene-centre']] # Changes the coordinates to separate columns
df_r1['month'] = [get_month(row) for row in df_r1['start-date']] # Changes the date to separate columns
df_r1['year'] = [get_year(row) for row in df_r1['start-date']] # Changes the date to separate columns
df_r1 = df_r1.astype({'long': 'float64', 'lat': 'float64', 'month': 'int64', 'year': 'int64'})

def has_imagery(row, df_r1):
    # Checks if a measurement has nearby coverage around the same time
    df_restricted = df_r1[(df_r1['long'] >= float(row[1]['LONG']-15.0)) & (df_r1['long'] <= float(row[1]['LONG'])+15.0) & (df_r1['lat'] >= float(row[1]['LAT'])-15.0) & (df_r1['lat'] <= float(row[1]['LAT'])+15.0)]
    if df_restricted.empty:
        return None
    else:
        year = int(str(row[1]['DATE']).split('-')[0])
        month = int(str(row[1]['DATE']).split('-')[1])
        df_restricted = df_restricted[(df_restricted['year'] == year) & (df_restricted['month'] == month)]
        if df_restricted.empty:
            return None
        else:
            print(df_restricted['download_link'].str.split('https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/').to_list()[0][1])
            return df_restricted['download_link'].str.split('https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/').to_list()[0][1]

df['has_coverage'] = [has_imagery(row, df_r1) for row in df.iterrows()]

output_df = df[df['has_coverage'].notnull()]

output_df.to_csv('output2.csv')