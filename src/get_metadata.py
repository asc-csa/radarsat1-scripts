import pandas as pd
import boto3
from pandas_schema import Column, Schema
from pandas_schema.validation import (
    InListValidation,
    CustomElementValidation
)
from botocore import UNSIGNED
from botocore.config import Config
from geopy.geocoders import Nominatim

# Setting up access
BUCKET_NAME = 'radarsat-r1-l1-cog'
s3client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
paginator = s3client.get_paginator('list_objects_v2')

def date_validator(str):
    """ Validates that the date is in the correct format.

    :param str: String containing the date to be validated.
    """
    if int(str.split('-')[0]) < 1996 or int(str.split('-')[0]) > 2013:
        return False
    if int(str.split('-')[1]) < 1 or int(str.split('-')[1]) > 12:
        return False
    if int(str.split('-')[2].split('T')[0]) < 1 or int(str.split('-')[2].split('T')[0]) > 31:
        return False
    return True

def check_int(num):
    """ Checks if a string is an integer.
    
    :param num: String to be checked.
    """
    try:
        int(num)
    except ValueError:
        return False
    return True

def check_float(num):
    """ Checks if a string is a float.

    :param num: String to be checked.
    """
    try:
        float(num)
    except ValueError:
        return False
    return True

# A series of validations to check different aspects of the data.
date_validation = [CustomElementValidation(lambda d: date_validator(d), 'Date is not valid')]
int_validation = [CustomElementValidation(lambda d: check_int(d), 'Int is not valid')]
float_validation = [CustomElementValidation(lambda d: check_float(d), 'Float is not valid')]
bool_validation = [CustomElementValidation(lambda d: d or not d, 'Bool is not valid')]
point_validation = [CustomElementValidation(lambda d: 'POINT' in d, 'Point is not valid')]
polygon_validation = [CustomElementValidation(lambda d: 'POLYGON' in d, 'Polygon is not valid')]
version_validation = [CustomElementValidation(lambda d: 'V' in d or 'VER' in d, 'Polygon is not valid')]
title_validation = [CustomElementValidation(lambda d: 'rsat1_' in d, 'Polygon is not valid')]
url_validation = [CustomElementValidation(lambda d: 'https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/' in d, 'URL is not valid')]

# We then declare the schema for the data using pandas_schema to validate the data
schema = Schema([
    Column('product-type', [CustomElementValidation(lambda s: len(s) == 3, 'was not 3 characters')]),
    Column('start-date', date_validation),
    Column('product-format', [InListValidation(['CEOS'])]),
    Column('scene-centre', point_validation),
    Column('pixel-spacing', float_validation),
    Column('sensor', [InListValidation(['RADARSAT-1'])]),
    Column('image-pixels', int_validation),
    Column('sensor-mode', [InListValidation(['Fine', 'High Incidence', 'Low Incidence', 'ScanSAR Narrow', 'ScanSAR Wide', 'Standard', 'Wide', None])], allow_empty=True),
    Column('orbit-direction', [InListValidation(['Ascending', 'Descending', None])], allow_empty=True),
    Column('polarization', [InListValidation(['HH', 'HV', 'VH', 'VV', None])], allow_empty=True),
    Column('corner-coordinates', polygon_validation),
    Column('processing-level', [InListValidation(['l1'])]),
    Column('processor-version', version_validation),
    Column('product-id', [CustomElementValidation(lambda s: len(s) == 8, 'was not 3 characters')], allow_empty=True),
    Column('public-good', bool_validation),
    Column('low-incidence-angle', int_validation),
    Column('high-incidence-angle', int_validation),
    Column('image-lines', int_validation),
    Column('end-date', date_validation),
    Column('absolute-orbit', int_validation),
    Column('beam', [InListValidation(['Fine 1', 'Fine 2', 'Fine 3', 'Fine 4', 'Fine 5', 'High Incidence 3', 'High Incidence 4', 'High Incidence 6', 'Low Incidence 1', 'ScanSAR Narrow A (W1 W2)', 'ScanSAR Narrow B (W2 S5 S6)', 'ScanSAR Wide A (W1 W2 W3 S7)', 'ScanSAR Wide B (W1 W2 S5 S6)', 'Standard 1', 'Standard 2', 'Standard 3', 'Standard 4', 'Standard 5', 'Standard 6', 'Standard 7', 'Wide 1', 'Wide 2', 'Wide 3', None])], allow_empty=True),
    Column('delivery-date', date_validation),
    Column('processing-date', date_validation),
    Column('band', [InListValidation(['C'])]),
    Column('spatial-resolution', int_validation),
    Column('order-key'),
    Column('position', [InListValidation(['EH3', 'EH4', 'EH6', 'EL1', 'F1', 'F2', 'F3', 'F4', 'F5', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'SCNA', 'SCNB', 'SCWA', 'SCWB', 'W1', 'W2', 'W3', None])], allow_empty=True),
    Column('sequence-id', int_validation),
    Column('title', title_validation),
    Column('archive-visibility-start-date', date_validation),
    Column('geodetic-terrain-height', int_validation),
    Column('processor-name', [InListValidation(['MMSSARP', 'MSSAR', 'RSARPS/S', None])], allow_empty=True),
    Column('look-orientation', [InListValidation(['left', 'right', None])], allow_empty=True),
    Column('lut-applied', [InListValidation(['Ice', 'Land', 'Mixed', 'Point Target', 'Sea', 'Unity', None])], allow_empty=True),
    Column('download_link', url_validation)
])


def get_data_from_month_and_year(year = -1, month = -1, to_csv=True):
    """Gets the data from the S3 bucket for a given month / year.

    :param year: Year of the data to be downloaded.
    :param month: Month of the data to be downloaded.
    :param to_csv: Whether or not to convert the output to CSV.
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
                for key, value in metadata["Metadata"].items():
                    for i in range(len(columns) - 1):
                        if columns[i] == key:
                            temp[i] = value
                            break
                temp[len(columns) - 1] = 'https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/' + file['Key']
                list.append(temp)
                if (len(temp) != len(columns)):
                    print("Not equal!")
                
            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))

    # We pop the first element of the list, which is the column names for the dataframe
    column_names = list.pop(0)

    # We can then look for errors in the data
    df = pd.DataFrame(list, columns=column_names)
    try:
        errors = schema.validate(df)
        pd.DataFrame(errors).to_csv("errors.csv")
    except:
        pass

    # We can then create a dataframe and return it
    if to_csv:
        df.to_csv(str(year) + '-' + str(month) + "_data.csv")
    return df

def get_data_from_date_range(start_year=1996, start_month=3, end_year=2013, end_month=3, to_csv=True):
    """Gets all the data from the S3 bucket for a given date range.

    :param start_year: Year of the start of the date range.
    :param start_month: Month of the start of the date range.
    :param end_year: Year of the end of the date range.
    :param end_month: Month of the end of the date range.
    :param to_csv: Whether or not to convert the output to CSV.
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
            super_data = get_data_from_month_and_year(start_year, start_month, False)
        else: # Otherwise, we append the data for the current month
            data = get_data_from_month_and_year(start_year, start_month, False)
            super_data = super_data.append(data, ignore_index = True)
        start_month += 1
    if to_csv:
        super_data.to_csv("data.csv")
    return super_data

def get_data_by_country(country_name, to_csv=True):
    """Gets the data from the S3 bucket for a given country.

    :param country_name: Name of the country to download metadata from.
    :param to_csv: Whether or not to convert the output to CSV.
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
                if location:
                    address = location.address

                # If the address is not null, we know it's in a country
                if address and location:
                    if type(address) is list:
                        country = address[len(address) - 1]
                    else:
                        address = address.split(",")
                        country = address[-1].strip()

                    # We then ensure the country matches the one we want
                    if country.lower() == country_name.lower():
                        # We then append the value of each metadata field
                        for key, value in metadata["Metadata"].items():
                            for i in range(len(columns) - 1):
                                if columns[i] == key:
                                    temp[i] = value
                                    break
                        temp[len(columns) - 1] = 'https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/' + file['Key']
                        list.append(temp)
                        if (len(temp) != len(columns)):
                            print("Not equal!")
            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))

    # We pop the first element of the list, which is the column names for the dataframe
    column_names = list.pop(0)
    df = pd.DataFrame(list, columns=column_names)

    # We can then look for errors in the data
    try:
        errors = schema.validate(df)
        pd.DataFrame(errors).to_csv("errors.csv")
    except:
        pass

    # We can then create a dataframe and return it
    if to_csv:
        df.to_csv(country_name + "_data.csv")
    return df

def get_data_from_filename(file_name, to_csv=True):
    """Gets the data from the S3 bucket for a given file.

    :param file_name: Name of the file to download metadata from.
    :param to_csv: Whether or not to convert the output to CSV.
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
    cols = []
    for key, value in metadata["Metadata"].items():
        list.append(value)
        cols.append(key)

    # We can then create a dataframe
    df = pd.DataFrame([list], columns=cols)

    # We can then look for errors in the data
    try:
        errors = schema.validate(df)
        pd.DataFrame(errors).to_csv("errors.csv")
    except:
        pass

    if to_csv:
        df.to_csv(file_name + ".csv")
    return df

def get_data_for_attribute(attribute_name, attribute_value, to_csv=True):
    """Gets data from the S3 bucket filtered by a given attribute.

    :param attribute_name: Name of the attribute to filter by.
    :param attribute_value: Value of the attribute to filter by.
    :param to_csv: Whether or not to convert the output to CSV.
    """

    # We then set up our parameters to make the call
    parameters = {
        'Bucket': BUCKET_NAME
    }

    page_iterator = paginator.paginate(**parameters)

    # Variables needed for the script
    list = [] # A list of lists containing the metadata
    column_names = True # Only runs during first iteration

    # Iterates through the bucket
    for bucket in page_iterator:
        # If there is no data, we return an empty dataframe
        if not 'Contents' in bucket:
            return pd.DataFrame()

        # Otherwise, we iterate through the contents
        for file in bucket['Contents']:
            try:
                metadata = s3client.head_object(Bucket='radarsat-r1-l1-cog', Key=file['Key'])

                # We first check that the attribute is contained in the metadata.
                if metadata["Metadata"] and attribute_name in metadata["Metadata"]:
                    # If so, we check that the attribute value is contained in the metadata.
                    if metadata["Metadata"][attribute_name].lower() == attribute_value.lower():
                        pass
                    else: # If it doesn't match, we continue with the next file
                        continue
                else: # If it's not in the metadata, we continue with the next file
                    continue

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
                for key, value in metadata["Metadata"].items():
                    for i in range(len(columns) - 1):
                        if columns[i] == key:
                            temp[i] = value
                            break
                temp[len(columns) - 1] = 'https://s3-ca-central-1.amazonaws.com/radarsat-r1-l1-cog/' + file['Key']
                list.append(temp)
                if (len(temp) != len(columns)):
                    print("Not equal!")
                
            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))
                return

    # We pop the first element of the list, which is the column names for the dataframe
    column_names = list.pop(0)

    # We can then look for errors in the data
    df = pd.DataFrame(list, columns=column_names)
    try:
        errors = schema.validate(df)
        pd.DataFrame(errors).to_csv("errors.csv")
    except:
        pass

    # We can then create a dataframe and return it
    if to_csv:
        df.to_csv(attribute_name + "_" + attribute_value + "_data.csv")
    return df