import os
import gdal
import numpy as np

src_1 = 'c:/ndvi/data/bands/LC08_L1TP_197031_20190722_20190801_01_T1_2019-07-22_B5.TIF'
src_2 = 'c:/ndvi/data/bands/LC08_L1TP_197031_20190722_20190801_01_T1_2019-07-22_B4.TIF'
dst = 'c:/ndvi/data/img_dst/ndvi_frombands.tif'

raster5 = gdal.Open(src_1)
raster4 = gdal.Open(src_2)

print(f"los tamaños del raster_NIR son {raster4.RasterXSize, raster4.RasterYSize} y del raster_red {raster3.RasterXSize, raster3.RasterYSize}")


####parámetros de geotransformación y proyección
try:
    if raster5.GetGeoTransform() == raster4.GetGeoTransform() and raster5.GetProjection() == raster4.GetProjection():
        print("Geotransform params and projection are ok")
except:
    print('projection or geotransform problems')

###raster shape
try:
    band5 = raster5.GetRasterBand(1).ReadAsArray().astype(np.float32)
    band4 = raster4.GetRasterBand(1).ReadAsArray().astype(np.float32)
    if band5.shape == band4.shape:
        print(f"NIR dimensions : {band5.shape} '\n' Red dimensions :  {band4.shape}")
        print('array size correct')
except:
    print('different array shape')


###create a raster 

ndvi = (band5 - band4) / (band5 + band4)
ndvi[ndvi == 0] = 0



try:
    driver = gdal.GetDriverByName('GTiff')
    dst_file = driver.Create(dst, raster4.RasterXSize, raster4.RasterYSize, 1, gdal.GDT_Float32, options=["COMPRESS=LZW"])
    dst_file.SetProjection(raster4.GetProjection())
    dst_file.SetGeoTransform(raster4.GetGeoTransform())
    dst_file.GetRasterBand(1).SetNoDataValue(0)
    dst_file.GetRasterBand(1).WriteArray(ndvi)
    print(f"{dst_file} created successfully")
except:
    print("problems with raster creation")

iface.addRasterLayer(dst, 'ndvi_bands')

