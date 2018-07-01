import matplotlib.pyplot as plt
from matplotlib.path import Path
import pandas as pd
import os
import matplotlib.patches as patches


col='1'
den='low'

verts1 = []
codes1 = []
verts2 = []
codes2 = []

if den=='high':
    cams=[4]
else:
    cams=[4,3,2,1]
for cam in cams:
#actual locations of corner coordinates
    #entrance left 
    x=0
    y=(4-cam)*52.
    verts1.append((x,y))
    if codes1==[]:
        codes1.append(Path.MOVETO)
    else:
        codes1.append(Path.LINETO)
    #wall bl
    x=0
    y=(4-cam)*52+21.5
    verts1.append((x,y))
    codes1.append(Path.LINETO)
    #wall br
    x=53
    y=(4-cam)*52+21.5
    verts1.append((x,y))
    codes1.append(Path.LINETO)
    #wall tr
    x=53
    y=(4-cam)*52+24.5
    verts1.append((x,y))
    codes1.append(Path.LINETO)
    #wall tl
    x=0
    y=(4-cam)*52+24.5
    verts1.append((x,y))
    codes1.append(Path.LINETO)
    #exit left
    x=0
    if cam==min(cams):        
        y=(4-cam)*52+43
    else:
        y=(4-cam)*52+46
    verts1.append((x,y))
    codes1.append(Path.LINETO)
    
    
    #entrace right
    x=6
    y=(4-cam)*52
    verts2.append((x,y))
    codes2.append(Path.LINETO)  
    #entrance top of wall
    x=6
    y=(4-cam)*52+3
    verts2.append((x,y))
    codes2.append(Path.LINETO)    
    #bottome right
    x=65
    y=(4-cam)*52+3
    verts2.append((x,y))
    codes2.append(Path.LINETO)
    #top right
    x=65
    y=(4-cam)*52+43
    verts2.append((x,y))
    codes2.append(Path.LINETO)  
    #exit bottom of wall
    x=6
    y=(4-cam)*52+43
    verts2.append((x,y))
    codes2.append(Path.LINETO) 
    #exit right    
    if cam==min(cams):
        x=0
        y=(4-cam)*52+43
    else:
        x=6
        y=(4-cam)*52+46
    verts2.append((x,y))
    codes2.append(Path.LINETO)    
         
verts2=list(reversed(verts2))    
verts2.append((0,0)) 
codes2.append(Path.CLOSEPOLY)

verts=verts1+verts2
codes=codes1+codes2
 
path = Path(verts, codes)

x_lines=[0.1,5.9,53.1,64.9]
y_lines=[0.1]
for cam in cams:
    y_lines=y_lines+[(4-cam)*52+3.1,(4-cam)*52+21.4,(4-cam)*52+24.6,(4-cam)*52+42.9]


#fig = plt.figure(figsize=(4,8))
#ax = fig.add_subplot(111)
#patch = patches.PathPatch(path, facecolor='orange', lw=2)
#ax.add_patch(patch)

output_directory='Boxed/Colony_'+col+'_'+den+'_density_boxed'

files=os.listdir('Interpolated/Colony_'+col+'_'+den+'_density_interpolated')
ID_list=[]
for file in files:
    ID=file[0:len(file)-14]
    ID_list.append(ID)

for ID in ID_list:
    compiled_file = open(output_directory+'/'+ID+'_locations.txt','w')
    df=pd.read_csv('Interpolated/Colony_'+col+'_'+den+'_density_interpolated/'+ID+'_locations.txt',names=['x','y'])

    for i,row in df.iterrows():
        x=row['x']
        y=row['y']
        point=[x,y]           
    
        if path.contains_point(point)==0 and x>0 and y>0:
            closest_y=100
            for yl in y_lines:
                if abs(y-yl)<closest_y:
                    closest_y=abs(y-yl)
                    new_y=yl
                    
            closest_x=100
            for xl in x_lines:
                if abs(x-xl)<closest_x:
                    closest_x=abs(x-xl)
                    new_x=xl
                    
            print('x',closest_x)
            print('y',closest_y)
            print(x,y)
            print(new_x,new_y)
            
            
            if path.contains_point([new_x,y])==1 and path.contains_point([x,new_y])==1:
                if closest_x<closest_y:        
                    new_point=[new_x,y]
                else:
                    new_point=[x,new_y]    
                    
            elif path.contains_point([new_x,y])==1:
                new_point=[new_x,y]
                
            elif path.contains_point([x,new_y])==1:
                new_point=[x,new_y]
                
            else:
                print('Move x and y')
                new_point=[new_x,new_y]
        else: 
            new_point=point
        compiled_file.write(str(i)+','+str("%.3f" % new_point[0])+','+str("%.3f" % new_point[1])+'\r')#str(new_X[i])+','+str(new_Y[i])
    compiled_file.close()