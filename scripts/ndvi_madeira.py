import os
import gdal
import numpy as np

src4_july = 'c:/ndvi/data/bands/madeira/MADEIRA_2016-07-26_B4.tif'
src5_july = 'c:/ndvi/data/bands/madeira/MADEIRA_2016-07-26_B5.tif'
src4_aug = 'c:/ndvi/data/bands/madeira/MADEIRA_2016-08-11_B4.tif'
src5_aug = 'c:/ndvi/data/bands/madeira/MADEIRA_2016-08-11_B5.tif'
dst_1 = 'c:/ndvi/data/img_dst/ndvi_july.tif'
dst_2 = 'c:/ndvi/data/img_dst/ndvi_aug.tif'

files = [src4_aug,src5_aug,src4_july,src5_july]

for file in files:
    if os.path.isfile(file):
        print(f'{file} is correct')
    else:
        print('incorrect files')

raster_nir_july = gdal.Open(src5_july)
raster_red_july = gdal.Open(src4_july)
raster_nir_aug = gdal.Open(src5_aug)
raster_red_aug = gdal.Open(src4_aug)

##check number of bands

print(f"el raster {raster_nir_july} tiene un total de {raster_nir_july.RasterCount} bandas")

###geotransform 

try:
    if raster_nir_july.GetGeoTransform() == raster_red_july.GetGeoTransform() and raster_nir_aug.GetGeoTransform() == raster_red_aug.GetGeoTransform():
        print("Geotransform params are ok")
except:
    print('geotransform problems')

###projection

try:
    if raster_nir_july.GetProjection() == raster_red_july.GetProjection() and raster_nir_aug.GetProjection() == raster_red_aug.GetProjection():
        print("Geotransform projection is ok")
except:
    print('geotransform problems')

###get bands arrays and check array shape


try:
    band4_july = raster_red_july.GetRasterBand(1).ReadAsArray().astype(np.float32)
    band5_july = raster_nir_july.GetRasterBand(1).ReadAsArray().astype(np.float32)
    band4_aug = raster_red_aug.GetRasterBand(1).ReadAsArray().astype(np.float32)
    band5_aug = raster_nir_aug.GetRasterBand(1).ReadAsArray().astype(np.float32)
    print('bands ok')
except:
    print("problem generating bands")

try:
    if band4_july.shape == band4_aug.shape:
        print('array size ok')
except:
    print("array problem")
ndvi_july = (band5_july - band4_july) / (band5_july + band4_july)
ndvi_july[ndvi_july == -999] 

ndvi_aug = (band5_aug - band4_aug) / (band5_aug + band4_aug)
ndvi_aug[ndvi_aug == -999] 

def get_ndvi(dst_file,ndvi_array,raster):
    try:
        driver = gdal.GetDriverByName('GTiff')
        dst_file = driver.Create(dst_file, raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Float32, options=["COMPRESS=LZW"])
        dst_file.SetProjection(raster.GetProjection())
        dst_file.SetGeoTransform(raster.GetGeoTransform())
        dst_file.GetRasterBand(1).SetNoDataValue(-999)
        dst_file.GetRasterBand(1).WriteArray(ndvi_array)
        print(f"{dst_file} created successfully")
    except:
        print("problem.............")

get_ndvi(dst_1,ndvi_july,raster_nir_july)

get_ndvi(dst_2,ndvi_aug,raster_nir_aug)

##load raster layers in qgis (symbology)

iface.addRasterLayer(dst_1)
iface.addRasterLayer(dst_2)