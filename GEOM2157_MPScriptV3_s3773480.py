print("\nPlease wait while script is running...")

#imports classes
import processing
import qgis.utils

#sets filepath variable
filepath = "H:/4 GIS Programming/Major Project/FINAL/PracticalCartoCorner-master/stage1_GIS/"

#sets project varibles for specific files utilised and created during project
CLNP_Boundary_FileName = "CraterLakeNP_boundary.shp"
CLNP_Elevations_FileName = "CraterLake_DEM.tif"
opBoundaryCRS = "CraterLakeNP_boundary_w122.shp"
opElevationsCRS = "CraterLake_DEM_w122.tif"
opGridLayer = "CraterLakeNP_grid.shp"
opClipLayer = "CraterLakeNP_clip.shp"
opPointsLayer = "CraterLakeNP_points.shp"
opPST = "pointSample_layer.gpkg"
opPointCoord = "pointcoord.shp"

#reprojects boundary vector layer to specific coordinate reference system (crs)-
#a Sinusoidal projection centered on -122.1492º, which passes through Wizard Island, Crater Lake National Park.
print("\nReprojecting boundary layer...")
crs = 'PROJ4:+proj=sinu +lon_0=-122.1492 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs'
processing.run("native:reprojectlayer", {'INPUT':filepath + CLNP_Boundary_FileName, 'TARGET_CRS': crs, 'OUTPUT': filepath + opBoundaryCRS})
CLNP_BoundaryLayer = iface.addVectorLayer(filepath + opBoundaryCRS, opBoundaryCRS[:-4], "ogr")

#reprojects elevation raster layer to specified crs 
print("\nReprojecting elevation layer...")
processing.run("gdal:warpreproject",{'DATA_TYPE' : 0, 'EXTRA' : '', 'INPUT' : filepath + CLNP_Elevations_FileName, 'MULTITHREADING' : False, 'NODATA' : None, 'OPTIONS' : '', 'OUTPUT' : filepath + opElevationsCRS, 'RESAMPLING' : 0, 'SOURCE_CRS' : QgsCoordinateReferenceSystem('EPSG:4326'), 'TARGET_CRS' : QgsCoordinateReferenceSystem('USER:100000'), 'TARGET_EXTENT' : None, 'TARGET_EXTENT_CRS' : None, 'TARGET_RESOLUTION' : None})
CLNP_ElevationsLayer = iface.addRasterLayer(filepath + opElevationsCRS, opElevationsCRS[:-4], "gdal")

#creates a lined grid (vector layer) over the approximate area of Crater Lake National Park 
print("\nCreating grid layer...")
processing.run("qgis:creategrid", {'CRS' : QgsCoordinateReferenceSystem('USER:100000'), 'EXTENT' : '-12653.788513249003,14558.084290046681,4736890.987739637,4772325.753771732 [USER:100000]', 'HOVERLAY' : 0, 'HSPACING' : 4400, 'OUTPUT' : filepath + opGridLayer, 'TYPE' : 1, 'VOVERLAY' : 0, 'VSPACING' : 443.75 })
CLNP_GridLayer = iface.addVectorLayer(filepath + opGridLayer, opGridLayer[:-4], "ogr")


print("\nRemoving vertical grid lines from grid layer...")

#imports QgsField from qgis.core
from qgis.core import QgsField

#Allows grid vector layer to be altered
CLNP_GridLayer.startEditing()

#defines varible for the grid layer attribute table fields
features=CLNP_GridLayer.getFeatures()


#Removes the vertical lines of the line grid using a loop to iterate over each feature (line) of the grid layer attributes table
for f in features:
    topLine = f["top"]
    bottomLine = f["bottom"]
    #if the top point of the line does not equal the bottom point of the line, the feature is deleted. Therefore leaving horizontal lines.
    if topLine != bottomLine:
        CLNP_GridLayer.deleteFeature(f.id())
        CLNP_GridLayer.updateFeature(f)
    else:
        pass
        CLNP_GridLayer.updateFeature(f)
   
##update the vulnerability field in the attributes table.   
CLNP_GridLayer.commitChanges()

#Clips (crops) the vector grid layer to the same shape as the Crater Lake National Park boundary.
print("\nClipping grid layer...")
processing.run("native:clip",{'INPUT' : filepath + opGridLayer, 'OUTPUT' : filepath + opClipLayer, 'OVERLAY' : filepath + opBoundaryCRS})
CLNP_Clip = iface.addVectorLayer(filepath + outputClipLayer, outputClipLayer[:-4], "ogr")

#Converts the lines in the vector grid layer to multiple points based on the data from the elevation data
print("\nConverting lines to points...")
processing.run("qgis:generatepointspixelcentroidsalongline",{'INPUT_RASTER' : filepath + opElevationsCRS, 'INPUT_VECTOR' : filepath + opClipLayer, 'OUTPUT' : filepath + opPointsLayer})
CLNP_Points = iface.addVectorLayer(filepath + opPointsLayer, opPointsLayer[:-4], "ogr")

#Uses the plugin "Point Sampling Tool" plugin to add elevation points to the points layer.
#This plugin should have been installed prior to running the script.
print("\nAdding elevation values to points. Point Sampling Tool plugin will open...")
print("\nPoint Sampling Tool plugin inputs are the following:\n \nLayer Containing sampling points: CraterLakeNP_points, \nLayers with fields/bands to get values from: CraterLake_DEM_w122: Band 1 (raster), \nOutput point vector layer: filepath + pointSample_layer, \nCRS: User:100000")

pst = qgis.utils.plugins['pointsamplingtool']
pst.run()

#adds coordinates to each point in the point layer
print("\nAdding coordinate data to points...")
processing.run("saga:addcoordinatestopoints", {'INPUT' : filepath + opPST, 'OUTPUT' : filepath + opPointCoord })
CLNP_PCoord = iface.addVectorLayer(filepath + opPointCoord, opPointCoord[:-4], "ogr")

#converts the point vector layer to a csv so that it can be utilised in R.
print("\nConverting vector layer to csv...")
QgsVectorFileWriter.writeAsVectorFormat(CLNP_PCoord, filepath + CLNP_csv, crs, CLNP_PCoord.crs(), "CSV", layerOptions=['GEOMETRY=AS_CSV'])
uri = "file:///H:/4%20GIS%20Programming/Major%20Project/FINAL/PracticalCartoCorner-master/stage1_GIS/CLNP_final.csv?type=csv&detectTypes=yes&xField=X&yField=Y&crs=USER:100000&spatialIndex=no&subsetIndex=no&watchFile=no".format(";", "x", "y")
vlayer = QgsVectorLayer(uri, "CLNP_final_csv", "delimitedtext")
QgsProject.instance().addMapLayer(vlayer)

print("\nProcessing Finished. Seeya!")

