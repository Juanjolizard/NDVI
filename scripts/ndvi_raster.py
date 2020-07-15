import gdal
import numpy as np

src = 'c:/ndvi/data/img_src/barcelona_raster_completo.tif'
dst = 'c:/ndvi/data/img_dst/output_ndvi.tif'

raster = gdal.Open(src)

print(f"el raster que vamos a abrir tiene un total de : {raster.RasterCount} bandas")


###definir la función: que calcule el indice y cree el raster output
band4 = raster.GetRasterBand(4).ReadAsArray().astype(np.float32)
band3 = raster.GetRasterBand(3).ReadAsArray().astype(np.float32)

ndvi = (band4 - band3) / (band4 + band3) ###operación entre arrays de numpy
print(type(ndvi)) ###tipo array, como era de suponer


driver = gdal.GetDriverByName('GTiff')
dst_file = driver.Create(dst, raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Float32, options=["COMPRESS=LZW"])
dst_file.GetRasterBand(1).WriteArray(ndvi)

iface.addRasterLayer(dst,'output_ndvi') ###se añade la capa a qgis cuando todo termine





