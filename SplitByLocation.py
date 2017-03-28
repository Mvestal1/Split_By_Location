import arcpy
import os

layerToSplit = arcpy.GetParameterAsText(0)
layerToSplitBy = arcpy.GetParameterAsText(1)
fieldToSplitBy = arcpy.GetParameterAsText(2)
finishedFolder = arcpy.GetParameterAsText(3)

fieldList = [row[0] for row in arcpy.da.SearchCursor(layerToSplitBy, fieldToSplitBy)]
field = ''
arcpy.MakeFeatureLayer_management(layerToSplitBy,"Split_Layer")
arcpy.MakeFeatureLayer_management(layerToSplit, "Layer1")
for field in fieldList:
    whereClause = fieldToSplitBy + " ='%s'" % field
    arcpy.SelectLayerByAttribute_management("Split_Layer", "CLEAR_SELECTION")
    arcpy.SelectLayerByAttribute_management("Split_Layer","NEW_SELECTION",whereClause)
    arcpy.SelectLayerByLocation_management("Layer1","INTERSECT","Split_Layer",'',"NEW_SELECTION")
    selectcount= int(arcpy.GetCount_management("Test").getOutput(0))
    if selectcount > 0:
        newName = layerToSplit + field
        outFile = os.path.join(finishedFolder, newName)
        arcpy.Clip_analysis (layerToSplit, layerToSplitBy, outFile)
        message = 'creating ' + field
        arcpy.AddMessage(message)
    else:
        a = '1'
