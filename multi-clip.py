#!/usr/bin/env python3
__author__ = 'smw'
__email__ = 'smw@ceh.ac.uk'
__status__ = 'Development'

import os
import sys
import arcpy
import timeit


start = timeit.default_timer()

lcm_vector = r'E:\land-cover-map\data\LCM2015_GB.gdb\lcm2015gbvector'
print('\n\nlcm_vector:\t\t{0}'.format(lcm_vector))

shp_folder = r'E:\land-cover-map\data\ShapeFiles'
print('\n\nshp_folder:\t\t{0}'.format(shp_folder))


out_gdb = r'E:\land-cover-map\data\out_gdb.gdb'
print('\n\nout_gdb:\t\t{0}'.format(out_gdb))


if arcpy.Exists(out_gdb):
    print('\n\nout_gdb exists.')
else:
    print('\n\nCreating out_gdb...')
    arcpy.CreateFileGDB_management(out_folder_path=os.path.dirname(out_gdb),
                                   out_name=os.path.basename(out_gdb))

print('\n\nLooping through shapefiles...')
arcpy.env.workspace = shp_folder
featureclasses = arcpy.ListFeatureClasses(wild_card='*',
                                          feature_type='Polygon')
for fc in featureclasses:
    print('\tfc:\t\t{0}'.format(fc))

    out_fc = os.path.join(out_gdb,
                          '{0}_{1}'.format(os.path.basename(lcm_vector), os.path.splitext(fc)[0]))
    print('\t\tout_fc:\t\t{0}'.format(out_fc))
    if arcpy.Exists(out_fc):
        arcpy.Delete_management(out_fc)

    # print('\t\tClipping...')
    # arcpy.Clip_analysis(in_features=lcm_vector,
    #                     clip_features=fc,
    #                     out_feature_class=out_fc)

    print('\t\tSelecting...')
    fl = 'featurelayer'
    if arcpy.Exists(fl):
        arcpy.Delete_management(fl)
    arcpy.MakeFeatureLayer_management(in_features=lcm_vector,
                                      out_layer=fl)

    arcpy.SelectLayerByLocation_management(in_layer=fl,
                                           overlap_type='INTERSECT',
                                           select_features=fc,
                                           selection_type='NEW_SELECTION')
    selected_features = int(arcpy.GetCount_management(fl)[0])
    print('\t\tselected_features:\t\t{0}'.format(selected_features))

    if selected_features > 0:
        arcpy.CopyFeatures_management(in_features=fl,
                                      out_feature_class=out_fc)
        copied_features = int(arcpy.GetCount_management(out_fc)[0])
        print('\t\tcopied_features:\t\t{0}'.format(copied_features))

    if arcpy.Exists(fl):
        arcpy.Delete_management(fl)


stop = timeit.default_timer()
total_time = stop - start
mins, secs = divmod(total_time, 60)
hours, mins = divmod(mins, 60)
print('\n\nTotal running time:\t\t{0}:{1}:{2:.2f}\n'.format(str(int(hours)).zfill(2), str(int(mins)).zfill(2), secs))
