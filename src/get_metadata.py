import pandas as pd
import plotly.express as px
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from geopy.geocoders import Nominatim

# Setting up access
BUCKET_NAME = 'radarsat-r1-l1-cog'
s3client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
paginator = s3client.get_paginator('list_objects_v2')

def get_data_from_month_and_year(year = -1, month = -1):
    """Gets the data from the S3 bucket for a given month / year.

    :param year: Year of the data to be downloaded.
    :param month: Month of the data to be downloaded.
    """

    # We limit our data by year or by month (if given)
    if month != -1:
        prefix = str(year) + "/" + str(month) + "/"
    elif year != -1:
        prefix = str(year) + "/"
    else:
        prefix = ""
    print(prefix)

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
            return pd.DataFrame()

        # Otherwise, we iterate through the contents
        for file in bucket['Contents']:
            try:
                metadata = s3client.head_object(Bucket='radarsat-r1-l1-cog', Key=file['Key'])

                # During the first iteration, we create a list of columns using the metadata tags
                if column_names:
                    columns = []
                    for column in metadata["Metadata"]:
                        columns.append(column)
                    columns.append('download_link')
                    list.append(columns)
                    column_names = False
                temp = [None] * len(columns)

                # We then append the value of each metadata field
                counter = 0
                for key, value in metadata["Metadata"].items():
                    for i in range(len(columns) - 1):
                        if columns[i] == key:
                            temp[i] = value
                            counter += 1
                            break
                temp[counter] = 'https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/' + file['Key']
                list.append(temp)
                if (len(temp) != len(columns)):
                    print("Not equal!")
                
            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))

    # We pop the first element of the list, which is the column names for the dataframe
    column_names = list.pop(0)

    # We can then create a dataframe and return it
    return pd.DataFrame(list, columns=column_names)

def get_data_from_date_range(start_year=1996, start_month=3, end_year=2013, end_month=3):
    """Gets the data from the S3 bucket for a given date range.

    :param start_year: Year of the start of the date range.
    :param start_month: Month of the start of the date range.
    :param end_year: Year of the end of the date range.
    :param end_month: Month of the end of the date range.
    """
    # Initialize an empty dataframe
    super_data = pd.DataFrame()

    # Iterate through the years
    while start_year <= end_year:
        # If we are in the same year, we iterate through the months
        if start_month > 12:
            start_year += 1
            start_month = 1
        # If we reach the end month, we break
        if start_year == end_year and start_month > end_month:
            break

        # We then get the data for the current month
        if super_data.empty: # If the dataframe is empty, we just start it with the data
            super_data = get_data_from_month_and_year(start_year, start_month)
        else: # Otherwise, we append the data for the current month
            data = get_data_from_month_and_year(start_year, start_month)
            super_data = super_data.append(data, ignore_index = True)
        start_month += 1

    return super_data

def get_data_by_country(country_name):
    """Gets the data from the S3 bucket for a given country.

    :param country_name: Name of the country to download metadata from.
    """

    # We set up our parameters to make the call
    parameters = {
        'Bucket': BUCKET_NAME,
    }

    page_iterator = paginator.paginate(**parameters)

    # Variables needed for the script
    list = [] # A list of lists containing the metadata
    column_names = True # Only runs during first iteration

    # Iterates through the bucket
    for bucket in page_iterator:
        for file in bucket['Contents']:
            try:
                metadata = s3client.head_object(Bucket='radarsat-r1-l1-cog', Key=file['Key'])

                # During the first iteration, we create a list of columns using the metadata tags
                if column_names:
                    columns = []
                    for column in metadata["Metadata"]:
                        columns.append(column)
                    columns.append('download_link')
                    list.append(columns)
                    column_names = False
                temp = [None] * len(columns)
                
                # We then have to use the metadata to get the longitude and latitude
                test = metadata['Metadata']['scene-centre']
                temp_coords = test.split("(")[1].split(" ")
                temp_coords[1] = temp_coords[1].replace(")", "")
                long = str(temp_coords[0])
                lat = str(temp_coords[1])

                # We then check if the longitude and latitude are in the country
                coordinates = lat + ", " + long
                geolocator = Nominatim(user_agent="radarsat-r1-l1-cog")
                location = geolocator.reverse(coordinates, language='en')
                address = location.address

                # If the address is not null, we know it's in a country
                if (address):
                    address = address.split(",")
                    country = address[-1].strip()

                    # We then ensure the country matches the one we want
                    if country.lower() == country_name.lower():
                        # We then append the value of each metadata field
                        counter = 0
                        for key, value in metadata["Metadata"].items():
                            for i in range(len(columns) - 1):
                                if columns[i] == key:
                                    temp[i] = value
                                    counter += 1
                                    break
                        temp[counter] = 'https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/' + file['Key']
                        list.append(temp)
                        if (len(temp) != len(columns)):
                            print("Not equal!")
                
            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))

    # We pop the first element of the list, which is the column names for the dataframe
    column_names = list.pop(0)

    # We can then create a dataframe and return it
    return pd.DataFrame(list, columns=column_names)

def get_data_from_filename(file_name):
    """Gets the data from the S3 bucket for a given file.

    :param file_name: Name of the file to download metadata from.
    """

    # We set up our parameters to make the call
    parameters = {
        'Bucket': BUCKET_NAME,
        'Key': file_name
    }

    # We then get the metadata for the file
    metadata = s3client.head_object(**parameters)

    # We then append the value of each metadata field
    list = []
    for key, value in metadata["Metadata"].items():
        list.append(value)

    # We can then create a dataframe and return it
    return pd.DataFrame(list, columns=metadata["Metadata"].keys())

df = get_data_from_month_and_year(1997,7)
print(df)
print(df[df['sensor-mode'] == 'Fine'])