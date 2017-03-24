import arcpy
import os

layerToSplit = arcpy.GetParameterAsText(0)
layerToSplitBy = arcpy.GetParameterAsText(1)
fieldToSplitBy = arcpy.GetParameterAsText(2)
finishedFolder = arcpy.GetParameterAsText(3)

fieldList = [row[0] for row in arcpy.da.SearchCursor(layerToSplitBy, fieldToSplitBy)]
field = ''
for field in fieldList:
    whereClause = fieldToSplitBy + " ='%s'" % field
    arcpy.SelectLayerByAttribute_management(layerToSplitBy, "CLEAR_SELECTION")
    arcpy.SelectLayerByAttribute_management(layerToSplitBy,"NEW_SELECTION",whereClause)
    newName = layerToSplit + field
    outFile = os.path.join(finishedFolder, newName)
    arcpy.Clip_analysis (layerToSplit, layerToSplitBy, outFile)
    message = 'creating ' + field
    arcpy.AddMessage(message)

arcpy.AddMessage('Deleting empty shapefiles')
#Delete Empty Shapefiles
deleteList = []
filelist = [a for a in os.listdir(finishedFolder)]
for a in filelist:
	statinfo = os.stat(os.path.join(finishedFolder, a))
	c = ''
	c = statinfo.st_size
	if c < 1000 and a.endswith('.shp'):
		print a
		b = os.path.splitext(a)
		deleteList.append(b)
	else:
		d = 1
filelist2 = []
for b in deleteList:
    for w in filelist:
        if w.startswith(b) and os.path.join(finishedFolder,w):
            os.remove(os.path.join(finishedFolder,w))
        else:
            print w
