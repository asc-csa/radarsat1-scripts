# Sample outputs for RADARSAT-1 scripts

This file contains sample outputs when using the scripts, along with a brief explanation.

## [downloading_files.py](downloading_files.py)

This file contains 5 sample functions to use for downloading imagery from the RADARSAT-1 satellite.

* download_directory(year, month, limit) - Downloads up to *limit* images from a given year and month.
* download_all() - Downloads all images in the S3 bucket. Note that this can take a significant amount of storage.
* download_file(file_name) - Downloads a given file from the S3 bucket.
* download_by_country(country_name, limit) - Downloads up to *limit* images of a given country.
* download_by_coordinates(latitude, longitude, range, limit) - Downloads up to *limit* images in a *range x range* square of a given latitude and longitude.

Images will be downloaded into a directory *year/month* where the script is run. This is a sample image downloaded from the satellite:

<img src="sample_outputs/image_sample.PNG" height="400">

The image also contains georeference data, allowing it to be opened with QGIS or GDAL.

## [get_metadata.py](get_metadata.py)

This file contains 4 sample functions for downloading metadata for images without downloading the image itself. Data is then returned as a Pandas DataFrame.

* get_data_from_month_and_year(year, month) - Retrieves all metadata for images from a given month and year
* get_data_from_date_range(start_year, start_month, end_year, end_month) - Retrieves all metadata for images between a starting month and ending month
* get_data_by_country(country_name) - Retrieves all metadata for images of a given country
* get_data_from_filename(file_name) - Retrieves all metadata for a specific image.

An example output following a call of `get_data_from_month_and_year(2000, 6)` is:

<img src="sample_outputs/metadata_output.PNG" height="400">

## [sample_algorithms.py](sample_algorithms.py)

This file contains 3 scripts that demonstrate some possible uses of the above functions.

* create_a_map(start_year, start_month, end_year, end_month) - Creates a Plotly scatter map and density map showing the locations of all images for a given time period.
* borders(img_url) - Attempts to find borders between water and land.
* chart_imagery_by_date(start_year, start_month, end_year, end_month) - Creates a Matplotlib pyplot showing the amount of imagery for a given date.

A sample call to create_a_map using the entire lifespan of RADARSAT-1:

<img src="sample_outputs/maps.PNG">

A sample call to borders using an image from RADARSAT-1:

<img src="sample_outputs/borders_output.PNG">

A sample call to chart_imagery_by_date between January 2000 and August 2000:

<img src="sample_outputs/chart_output.PNG">
