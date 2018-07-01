import pandas as pd
import numpy as np
import pickle as pk
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import os
import cv2
#import draw_nest
#
def transform(x,y,box):

    if box!=0:
        a=np.array([x,y,1])
        row=np.dot(h[box],a)
        x=row[0]-x_adjust[box]
        y=row[1]-y_adjust[box]
        if den=='low':
            y=y+(4-box)*52  
    return [x,y]

col='2'
den='low'

ID_list=[]
files=os.listdir('Colony_'+col+'/Colony_'+col+'_'+den+'_density_locations')
for file in files:
    ID=file[0:len(file)-14]
    ID_list.append(ID)

real_points={}
real_points['top_right']=[65,43]
real_points['bottom_right']=[65,3]
real_points['entrance_left']=[0,0]
real_points['entrance_right']=[6,0]
real_points['entrance_top_of_wall']=[6,3]
real_points['exit_left']=[0,46]
real_points['exit_right']=[6,46]
real_points['exit_bottom_of_wall']=[6,43]
real_points['wall_tr']=[53,24.5]
real_points['wall_br']=[53,21.5]
real_points['wall_tl']=[0,24.5]
real_points['wall_bl']=[0,21.5]
real_points['top_left']=[0,43]

mdf=pd.read_csv('measurements.csv',sep=',')

h={}
x_adjust={}
y_adjust={}

if den=='high':
    cameras=[1]
else:
    cameras=[1,2,3,4]

for cam in cameras: 
    print('cam',cam)
    if cam==1:
        points=['top_right', 'bottom_right', 'entrance_left', 'entrance_right', 'entrance_top_of_wall',  'wall_tl', 'wall_bl','top_left']#
    else:
        points=['top_right', 'bottom_right', 'entrance_left', 'entrance_right', 'entrance_top_of_wall',  'exit_left', 'exit_right', 'exit_bottom_of_wall', 'wall_tl', 'wall_bl']
    temp_df=mdf[(mdf['colony']==int(col))&(mdf['density']==den)&(mdf['camera']==cam)]
    object_points=[]
    image_points=[]
    
    for header in points:
        objp=real_points[header]
        object_points.append(objp)
        image_points.append([temp_df.iloc[0][header],temp_df.iloc[1][header],1]) 
    object_points=np.array(object_points)
    #y_max=max([i[1] for i in image_points])
    image_points=[[i[0],i[1]] for i in image_points]
    image_points=np.array(image_points)

    h[cam],status= cv2.findHomography(image_points,object_points)
    print()
    print('h=',h[cam])
    print('det=',np.linalg.det(h[cam]))
    print()
    x_vals=[]
    y_vals=[]
    for header in points:
        temp_df=mdf[(mdf['colony']==int(col))&(mdf['density']==den)&(mdf['camera']==cam)]
        a=np.array([temp_df.iloc[0][header],temp_df.iloc[1][header],1])
        row=np.dot(h[cam],a)
        x_vals.append(row[0])
        y_vals.append(row[1])
        #print(header,'\t',a,'\t',row)
    x_adjust[cam]=min(x_vals) 
    y_adjust[cam]=min(y_vals) 
    
    for header in points:
        print(header,'\t',transform(temp_df.iloc[0][header],temp_df.iloc[1][header],cam))
#
#
output_directory='Corrected/Colony_'+col+'_'+den+'_density_corrected'
n=0
for ID in ID_list:
    print(n,ID)
    n=n+1
    z=pd.read_csv('Colony_'+col+'/Colony_'+col+'_'+den+'_density_locations/'+ID+'_locations.txt',sep=',',header=None,names=['x','y','box'])
    location=[]
    for i,row in z.iterrows():
        new_row=transform(row['x'],row['y'],row['box'])
        location.append(new_row)
    compiled_file = open(output_directory+'/'+ID+'_locations.txt','w')
    for row in location:
        compiled_file.write(str(row[0])+','+str(row[1])+'\n')
    compiled_file.close()

