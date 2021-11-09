import boto3
import os
import traceback
from botocore.config import Config
from botocore import UNSIGNED
from geopy.geocoders import Nominatim

MY_CONFIG = Config(
    region_name = 'ca-central-1',
    signature_version = UNSIGNED,
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

BUCKET_NAME = 'radarsat-r1-l1-cog'
S3_CLIENT = boto3.client('s3', config=MY_CONFIG)
S3_RESOURCE = boto3.resource('s3', config=MY_CONFIG)

def download_directory(year, month, limit=5):
    """ Download a directory of files from the RADARSAT-1 bucket.

    :param year: Year of the files to download
    :param month: Month of the files to download
    :param limit: Maximum number of files to download
    """
    bucket = S3_RESOURCE.Bucket(BUCKET_NAME)
    count = 0

    # Create a directory address with the year + month
    directory = str(year) + "/" + str(month)

    # Iterate through the objects in the bucket
    for obj in bucket.objects.filter(Prefix=directory):
        print("Downloading picture " + str(count + 1) + "/" + str(limit) + ": " + str(obj.key))

        # If that location does not already exist, we create it.
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        
        # We can then download the file to the address
        bucket.download_file(obj.key, obj.key)

        # We ensure only a maximum of limit files are downloaded
        count += 1
        if count >= limit:
            break

def download_all():
    """ Download all the files from the RADARSAT-1 bucket. """
    bucket = S3_RESOURCE.Bucket(BUCKET_NAME)

    # Iterate through the objects in the bucket
    for obj in bucket.objects.all():
        print("Downloading: " + str(obj.key))

        # If that location does not already exist, we create it.
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        
        # We can then download the file to the address
        bucket.download_file(obj.key, obj.key)

def download_file(file_name):
    """ Download a file from the RADARSAT-1 bucket.

    :param file_name: Name of the file to download
    """
    bucket = S3_RESOURCE.Bucket(BUCKET_NAME)
    bucket.download_file(file_name, file_name)

def download_by_country(country_name, limit=float("inf")):
    """ Download all the files from the RADARSAT-1 bucket for a given country.

    :param country_name: Name of the country to download
    :param limit: Maximum number of files to download
    """

    page_iterator = S3_CLIENT.get_paginator('list_objects_v2').paginate(Bucket=BUCKET_NAME)
    count = 0

    # Iterates through the bucket
    for bucket in page_iterator:
        for file in bucket['Contents']:
            try:
                metadata = S3_CLIENT.head_object(Bucket='radarsat-r1-l1-cog', Key=file['Key'])
                
                # We then have to use the metadata to get the longitude and latitude
                test = metadata['Metadata']['scene-centre']
                temp = test.split("(")[1].split(" ")
                temp[1] = temp[1].replace(")", "")
                long = str(temp[0])
                lat = str(temp[1])

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
                        filename = metadata['Metadata']['scene-centre'] + ".tif"
                        date = metadata['Metadata']['end-date'].split('-')
                        key = date[0] + "/" + date[1] + "/" + filename

                        # We then download the file
                        if not os.path.exists(os.path.dirname(key)):
                            os.makedirs(os.path.dirname(key))
                        print("Downloading: " + str(file['Key']))
                        S3_CLIENT.download_file('radarsat-r1-l1-cog', file['Key'], file['Key'])
                        
                        # We ensure only a maximum of limit files are downloaded
                        count += 1
                        if count >= limit:
                            return

            except Exception as e:
                print(e)
                print("Failed {}".format(file['Key']))

def download_by_coordinates(latitude, longitude, range=1.5, limit=float("inf")):
    """ Download all the files from the RADARSAT-1 bucket for a given coordinate.

    :param latitude: Latitude of the coordinate to download. Note that southern values should be negative.
    :param longitude: Longitude of the coordinate to download. Note that western values should be negative.
    :param limit: Maximum number of files to download
    """
    page_iterator = S3_CLIENT.get_paginator('list_objects_v2').paginate(Bucket=BUCKET_NAME)
    count = 0

    # Iterates through the bucket to examine each file
    for bucket in page_iterator:
        for file in bucket['Contents']:
            try:
                metadata = S3_CLIENT.head_object(Bucket='radarsat-r1-l1-cog', Key=file['Key'])

                # We then use the metadata to get the longitude and latitude
                test = metadata['Metadata']['scene-centre']

                # Some files have an incorrect scene-centre metadata. If found, we skip them
                if len((test).split("(")) < 2:
                    continue

                # We then have to use the metadata to get the longitude and latitude
                temp = test.split("(")[1].split(" ")
                temp[1] = temp[1].replace(")", "")
                long = str(temp[0])
                lat = str(temp[1])

                # We then check if the longitude and latitude are around the given coordinates based on the range given
                diff_long = abs(float(long) - float(longitude))
                diff_lat = abs(float(lat) - float(latitude))

                # If the difference of latitude and longitude is less than the range, the file is around the coordinates and we download it
                if (diff_long <= range and diff_lat <= range):
                    filename = metadata['Metadata']['scene-centre'] + ".tif"
                    date = metadata['Metadata']['end-date'].split('-')
                    key = date[0] + "/" + date[1] + "/" + filename

                    # We then download the file
                    if not os.path.exists(os.path.dirname(key)):
                        os.makedirs(os.path.dirname(key))
                    print("Downloading: " + str(file['Key']))
                    S3_CLIENT.download_file('radarsat-r1-l1-cog', file['Key'], file['Key'])
                    
                    # We ensure only a limited number of files are downloaded
                    count += 1
                    if count >= limit:
                        return
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print("Failed {}".format(file['Key']))

download_by_coordinates(61.4, -114.7, 2.5, 10)