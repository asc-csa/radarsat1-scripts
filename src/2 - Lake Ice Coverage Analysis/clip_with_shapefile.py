# Note: Not currently working

from osgeo import gdal

# Files used for this example
inras = r'1998/10/RS1_X0492758_SCWB_19981008_212713_HH_SCW.tif'
outras = r'output/RS1_clip1.tif'
outras_comp = r'output/RS1_clip2.tif' #compressed, optional
invec = r'shapefile/Inland_lakes_mergedWGS84.shp'

# We start by opening the raster file
dataset = gdal.Open(inras)

print("Beginning clip...")
gdal.Warp(outras, dataset, dstSRS=dataset.GetProjection(),
                    format='GTiff',
                    cutlineDSName=invec,
                    cropToCutline=True,
                    dstNodata = 0)

#Optional - gdal warp doesn't handle compression well so the files balloon
translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co COMPRESS=LZW"))
gdal.Translate(outras_comp, outras, options=translateoptions)

print("Finished.")
