# This file contains code to determine whether there is RADARSAT-1 coverage
# for the locations and dates given in lakeice-measurements.xlsx.

import pandas as pd
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# Setting up access
BUCKET_NAME = 'radarsat-r1-l1-cog'
s3client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
paginator = s3client.get_paginator('list_objects_v2')


def check_for_imagery(year = -1, month = -1, lat=0, long=0, validate = True):
    """Determines if there is imagery for a given location at a given month and year.

    :param year: Year of the data to be checked.
    :param month: Month of the data to be checked.
    :param lat: Latitude of the data to be checked.
    :param long: Longitude of the data to be checked.
    :param validate: Whether or not to validate the data.
    """

    # We limit our data by year or by month (if given)
    if month != -1:
        prefix = str(year) + "/" + str(month) + "/"
    elif year != -1:
        prefix = str(year) + "/"
    else:
        prefix = ""

    # We then set up our parameters to make the call
    parameters = {
        'Bucket': BUCKET_NAME,
        'Prefix': prefix
    }

    page_iterator = paginator.paginate(**parameters)

    # Variables needed for the script
    list = [] # A list of lists containing the metadata
    column_names = True # Only runs during first iteration

    # Iterates through the bucket
    for bucket in page_iterator:
        # If there is no data, we return an empty dataframe
        if not 'Contents' in bucket:
            print("Note: There is no imagery for year", year, "month", month)
            return False

        # Otherwise, we iterate through the contents
        for file in bucket['Contents']:
            try:
                metadata = s3client.head_object(Bucket='radarsat-r1-l1-cog', Key=file['Key'])

                # We then use the metadata to get the longitude and latitude
                test = metadata['Metadata']['scene-centre']
                if len((test).split("(")) < 2:
                    continue
                temp = test.split("(")[1].split(" ")
                temp[1] = temp[1].replace(")", "")
                longitude = str(temp[0])
                latitude = str(temp[1])

                # We use the difference between the longitude and latitude to determine if the data is in the correct location
                diff_long = abs(float(long) - float(longitude))
                diff_lat = abs(float(lat) - float(latitude))

                # We then append the value of each metadata field
                if (diff_long <= 1.0 and diff_lat <= 1.0):
                    return True # If the data is within the range, we return true
                
            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))
    return False # If the data is not within the range, we return false

df = pd.read_excel("lakeice-measurements.xlsx") # Reads the data

has_coverage = [] # List to contain whether or not the data has R1 coverage
test = {} # Indicator to show whether a given coordinate and date has already been tested

# Iterates through the data
for index, row in df.iterrows():
    date_str = str(row['DATE'])
    name = str(row['NAME']) # Retrieves the name of the lake
    date = date_str.split('-') # Splits the date into year, month, and day

    # We then check if the data has already been tested
    if name+date[0]+date[1] not in test:
        # If it has not, we check if the data has R1 coverage
        lat = float(row['LAT'])
        long = 0.0 - float(row['LONG']) # west = negative
        res = check_for_imagery(int(date[0]), int(date[1]), lat, long, False)

        # We then append whether the lake has coverage or not
        has_coverage.append(res)
        test[name+date[0]+date[1]] = res
    else:
        # If the data has already been tested, we append the result from that check
        print("Already checked")
        has_coverage.append(test[name+date[0]+date[1]])

# We then add the results to the dataframe and output it to a CSV
df['R1 Coverage'] = has_coverage
df.to_csv('lakeice-measurements-with-indicator.csv')

# We also output a dataframe only showing where the indicator is true, since these can be used to check the data
df_trues = df[df['R1 Coverage'] == True].copy()
df_trues.to_csv('R1_Lake_Coverage_Trues_Only.csv')