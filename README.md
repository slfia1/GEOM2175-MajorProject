# GEOM2175-MajorProject
Testing site for Semester 2 2019 Geo-spatial Programming Course

The cover art for Joy Division’s 1979 album Unknown Pleasures (designed by Peter Saville) is based on a plot from an astronomy dissertation (Craft 1970), and displays radio intensities from the first known pulsar. 

Practical Cartographer’s Corner has developed a workflow that produces elevtion maps in a format stylisticly similar to the Joy Division albam cover. using QGIS. This workflow uses QGIS3, R and Adobe Illustrator or Photoshop.
See https://cartographicperspectives.org/index.php/journal/article/view/1536/1726 for workflow.

The aim of my GEOM2175 Major Project was to automate part 1 of the 
Practical Cartographer’s Corner workflow in QGIS3, in which the required transects are created and prepared in preperation for plotting in R. 

Before running this project script you will need to install thhe plugin "Point Sampling Tool". this is done by clicking on Plugins> Manage and install plugins...> Not installed> install Plugin > close. 

If installed correctly the plugin will be located at Plugins> Analyses> Point Sampling Tool.

Instructions on the correct input and output parameters will apear in the Python console. Script will continue to run once you complete and close the plugin.

The files required to run this script are CraterLake_DEM.tif and all of the CraterLakeNP_boundary files.
