###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Nathan Mitchell", "01254873"])

###################################################################### 
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    arcpy.env.workspace=input_geodatabase
    #two new fields will be added onto fcPoint, the FID and Distance
    arcpy.analysis.Near(fcPoint,fcPolyline)
    

######################################################################
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    arcpy.env.workspace=input_geodatabase
    #setup delimters
    delimitedF=arcpy.AddFieldDelimiters(fcPoint,pointFieldName)
    #create update cursor for fcPoint feature class on field pointFieldName where delemiter is equal to pointFieldValue
    cursor=arcpy.da.UpdateCursor(fcPoint, [pointFieldName],delimitedF+"="+pointFieldValue)
    #All indicies with pointFieldValue will replace existing values and delete the rest
    for row in cursor:
        if row[0] != pointFieldValue:
            del row
        else:
            row[0] = pointFieldValue
            cursor.updateRow(row)
    #spatial join on the trimmed table to only pull if pointFieldName=pointFieldValue (only Nursing Homes)
    arcpy.analysis.SpatialJoin(fcPolygon,fcPoint,fcPolygon)

######################################################################
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    arcpy.env.workspace=workspace
    #initialize empty list 
    myList=[]
    #extracting values of attribute from point feature
    for row in arcpy.da.SearchCursor(fcPoint,pointFieldName):
    #if the attribute is unique it will be added to list
        if row[0] not in myList:
            myList.append(row[0])
    #adding a field for each element in the list
    #using countPointsByTypeWithinPolygon function to join the counts
    for i in myList:
        arcpy.management.AddField(fcPoint, i.strip()[:12]+"_Count", "STRING")
        countPointsByTypeWithinPolygon(workspace, fcPoint, pointFieldName, i+"_Count", fcPolygon)

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
