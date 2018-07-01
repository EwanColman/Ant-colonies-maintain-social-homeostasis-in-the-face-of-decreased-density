import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import pandas as pd
import pickle as pk
import os

#################################################################
# 1. Rotate evrything so that entrance is on bottom right
# 2. 



col='2'
den='low'

if den=='high':
    ymax=46
else:
    ymax=202

T=14400
#ID_list=[]
#files=os.listdir('Boxed/Colony_'+col+'_'+den+'_density_boxed')
#for file in files:
#    ID=file[0:len(file)-14]
#    ID_list.append(ID)
 
groups=pd.read_csv('Node_attributes_colony_'+col+'.csv')

ID_list=groups[groups['Spatial_group_'+den]!=0]['ID'].tolist()

X={}
Y={}
for ID in ID_list:
    df=pd.read_csv('Boxed/Colony_'+col+'_'+den+'_density_boxed/'+ID+'_locations.txt',names=['x','y'])
    X[ID]=df['x'].tolist()
    # flip the y values
    Y[ID]=[ymax-y for y in df['y'].tolist()]
    
   
            
#################################################################
#lines
x_bl={}
y_bl={}
M={}
sin_theta={}
cos_theta={}            
            
p=[]
q=[]
if den=='high':
    cams=[4]
else:
    cams=[4,3,2,1]
for cam in cams:

    x=0
    y=(4-cam)*52
    p.append([x,y])
    #wall bl
    x=0
    y=(4-cam)*52+21.5
    p.append([x,y])
    #wall br
    x=53
    y=(4-cam)*52+21.5
    p.append([x,y])
    #wall tr
    x=53
    y=(4-cam)*52+24.5
    p.append([x,y])
    #wall tl
    x=0
    y=(4-cam)*52+24.5
    p.append([x,y])
    #exit left
    x=0
    if cam==min(cams):        
        y=(4-cam)*52+43
    else:
        y=(4-cam)*52+46
    p.append([x,y])
    
    
    #entrace right
    x=6
    y=(4-cam)*52
    q.append([x,y])      
    #entrance top of wall
    x=6
    y=(4-cam)*52+3
    q.append([x,y]) 
    #bottome right
    x=65
    y=(4-cam)*52+3
    q.append([x,y]) 
    #top right
    x=65
    y=(4-cam)*52+43
    q.append([x,y]) 
    #exit bottom of wall
    x=6
    y=(4-cam)*52+43
    q.append([x,y])    
    #exit right
    
    if cam==min(cams):
        x=0
        y=(4-cam)*52+43
    else:
        x=6
        y=(4-cam)*52+46
    q.append([x,y])     

##################################################################
groups=pd.read_csv('Node_attributes_colony_'+col+'.csv')
#get a dictionary of colors
group_type='Spatial_group_'+den

color={}
for ID in ID_list:
    group=list(set(groups[groups['ID']==ID][group_type]))[0]
    color[ID]=int(group)
               
##########################################################
if 4 in color.values():
    group_colour={0:'k',1:'#ff000c',2:'#fc8f00',3:'#4baf48',4:'#1b6cd1',5:'k'}
elif 3 in color.values():
    group_colour={0:'k',1:'#ff000c',2:'#4baf48',3:'#1b6cd1',5:'k'}
else:
    group_colour={0:'k',1:'#ff000c',2:'#1b6cd1',5:'k'}
#################################################################



##################################################################
trophallaxis=pk.load(open('trophallaxis_locations/trophallaxis_locations_'+col+'_'+den+'.p','rb'))
##################################################################


frames=os.listdir('images_'+str(col)+'_'+den)
frame_numbers=[-1]
for frame in frames:
    if frame[0:5]=='image':
        print('frame',frame[5:len(frame)-4])
        frame_numbers.append(int(frame[5:len(frame)-4]))
frame_number=1+max(frame_numbers)
print(frame_number)

#frame_number=260

for t in range(frame_number,T):
    print(t)
    if den=='high':
        fig = plt.figure(figsize=(7,10))#change for linux
        ax=fig.add_subplot(111) 
        #plt.axes(ylim=(-5, 70), xlim=(-5, 50))
        ax.set_xlim([-5,50])
        ax.set_ylim([-5,70])
    else:
        fig = plt.figure(figsize=(20,10))
        ax=fig.add_subplot(111)
        #plt.axes(ylim=(-5, 70), xlim=(-5, 200))
        ax.set_xlim([-5,206])
        ax.set_ylim([-5,70])
#    for cam in cams:
#        for i in range(len(p)-1):
#            ax.plot([p[i][1],p[i+1][1]],[p[i][0],p[i+1][0]],color='k',linewidth=2)
#        for i in range(len(q)-1):
#            ax.plot([q[i][1],q[i+1][1]],[q[i][0],q[i+1][0]],color='k',linewidth=2)    

    #######Draw patches#############

#top patch    
    verts = [(ymax,68)]
    codes=[Path.MOVETO]
    for i in range(len(q)):
        verts.append((ymax-q[i][1],q[i][0]))
        codes.append(Path.LINETO)
    verts.append((0,0))
    codes.append(Path.LINETO)
    verts.append((0,68))
    codes.append(Path.LINETO)
    verts.append((ymax,68))
    
    codes.append(Path.CLOSEPOLY)

    path = Path(verts, codes)    
    
    path=Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='k', lw=2)
     
    ax.add_patch(patch)

#bottom patch
    
    verts = [(ymax,-3)]
    codes=[Path.MOVETO]
    for i in range(len(p)):
        verts.append((ymax-p[i][1],p[i][0]))
        codes.append(Path.LINETO)
    verts.append((0,0))
    codes.append(Path.LINETO)
    verts.append((0,-3))
    codes.append(Path.LINETO)
    verts.append((ymax,-3))
    
    codes.append(Path.CLOSEPOLY)


    path = Path(verts, codes)    
    
    path=Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='k', lw=2)
     
    ax.add_patch(patch)
    for ID in ID_list:
        
        if ID=='Queen':
            colour=group_colour[color[ID]]
            size=800
            name='Q'
            a=0.3
        else:
            size=600
            if ID=='corpse':
                name='X'
            else:
                name=ID
            colour=group_colour[color[ID]]
            a=0.3
    
        trail_length=min(t,15)
        for i in range(1,trail_length):    
            x=X[ID][t-i:t+1]
            y=Y[ID][t-i:t+1]
            
            for j in range(i+1):
                if x[j]==0.0 and y[j]==ymax:
                    x[j]=3
            
            
            ax.plot(y,x,color='k',linewidth=3,zorder=1,alpha=0.003*(trail_length-i)**(1.7))    
    
        if X[ID][t]!=0:
            #make a patch
            ax.scatter([Y[ID][t]],[X[ID][t]],s=size,c='w',zorder=2,edgecolors='k',linewidth=1.5)
            ax.scatter([Y[ID][t]],[X[ID][t]],s=size,c=colour,linewidth=0,zorder=3,alpha=a)
            if den=='low':            
                text_y=Y[ID][t]-0.5*len(name)
            else:
                text_y=Y[ID][t]-0.3*len(name)
            ax.text(text_y,X[ID][t]-0.5,name,zorder=4,fontsize=10)#change for linux
            
            #add the trail

    for l in trophallaxis[t]:
        if len(l)>0:
            ax.plot([ymax-l[0][1],ymax-l[1][1]],[l[0][0],l[1][0]],color='r',linewidth=10,zorder=1)
    plt.tight_layout()
    ax.axis('off')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.ioff()
    plt.savefig('images_'+str(col)+'_'+den+'/image'+str(t)+'.png')
    plt.close()
#then use:
print()
print('cd ~/Desktop/Animation_codes_and_data/images_'+col+'_'+den)
print('ffmpeg -f image2 -r 10 -i image%01d.png -vcodec libx264 -y -crf 25 ../colony_'+col+'_'+den+'_video.mp4')
print()
#ffmpeg -f image2 -r 10 -i image%01d.png -vcodec mpeg4 -y ../colony_3_low_video.mp4
