# GEOM2175-MajorProject
Testing site for Semester 2 2019 Geo-spatial Programming Course

The cover art of Joy Division’s 1979 album Unknown Pleasures (designed by Peter Saville), is based on a plot from an astronomy dissertation (Craft 1970), and displays radio intensities from the first known pulsar. 

Practical Cartographer’s Corner (PCC) has developed a workflow that produces elevtion maps in a format stylisticly similar to the Joy Division albam cover. PCC's workflow uses QGIS3, R and Adobe Illustrator or Photoshop.
See https://cartographicperspectives.org/index.php/journal/article/view/1536/1726 for workflow.

The aim of this GEOM2175 Major Project was to automate part 1 of the PPC workflow in QGIS3. Part 1 creates and prepares the required transects for plotting in R. 

Before running the project script you will need to install the plugin "Point Sampling Tool". This is done by clicking on Plugins> Manage and install plugins...> Not installed> install Plugin > close. The plugin can be downloaded from https://plugins.qgis.org/plugins/pointsamplingtool/.

If installed correctly, the plugin will be located at Plugins> Analyses> Point Sampling Tool.

Instructions on the correct input and output parameters will apear in the Python console. The project script will continue to run once you have completed and closed the plugin.

The files required to run this script are CraterLake_DEM.tif and the CraterLakeNP_boundary files.
