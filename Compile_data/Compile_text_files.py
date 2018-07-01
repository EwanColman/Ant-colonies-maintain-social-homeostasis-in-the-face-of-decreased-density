import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle as pk
import os



colony='1'
density='low'

details=pd.read_csv('Video_details.txt',sep=',')
details=details[(details['Colony']==int(colony))&(details['Density']==density)]



output_directory='Colony_'+colony+'_'+density+'_density_locations'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


#    #get a a list of names 
cameras=list(set(details['Camera']))
#cameras=[2,3]
files={}
all_files=[]


folder={}
for camera in cameras:
    if density=='high':
        cam=''
        
    else:
        cam='_camera_'+str(camera)
    folder[camera]='Colony_'+colony+'/Colony_'+colony+'_'+density+'_density'+cam
    files[camera]=os.listdir(folder[camera])
    all_files=all_files+files[camera]

ID_list=[]
Queen_names=[]
for file in all_files:
    file=file.replace('.TXT','.txt')
    file=file.replace('Corpse.txt','corpse.txt')
    file=file.replace('CORPSE.txt','corpse.txt')
    
    print(file)
    s=file.find('.',0)
    ID=file[9:s]
    if (ID[0]=='Q')|(ID[0]=='q'):
        Queen_names.append(ID)
        ID='Queen'
    while ID[0]=='0':
        ID=ID[1:len(ID)]
    ID_list.append(ID)
ID_list=list(set(ID_list))
Queen_names=list(set(Queen_names))
#
print('Ant IDs:',sorted(ID_list))
print()
print('Queen names:',Queen_names)
print()
#
for ID in ID_list:
    output={}
    
    for camera in cameras:
        output[camera]=[]
        temp_details=details[details['Camera']==camera].sort('Order')
        video_names=temp_details['Video'].tolist()
        for video_name in video_names:
            info=temp_details[temp_details['Video']==video_name]
            start=int(info['First_frame'].tolist()[0])
            end=int(info['Last_frame'].tolist()[0])
            missing_file=False
            filename=video_name+'_'+ID+'.txt'
            #deal with the Queen names problem:       
            if ID=='Queen':
                for Queen_ID in Queen_names:
                    temp_filename=video_name+'_'+Queen_ID+'.txt'
                    if temp_filename in files[camera]:
                        filename=temp_filename     
            zeros='0'
            if filename not in files[camera]:
                filename=video_name+'_'+'0'+ID+'.txt'
            if filename not in files[camera]:
                filename=video_name+'_'+'00'+ID+'.txt'                  
            if filename not in files[camera]:
                missing_file=True

                print(folder[camera]+' Video '+video_name+', Ant '+ID+', not found')              
            if missing_file==False:
                df=pd.read_csv(folder[camera]+'/'+filename,header=None,names=['frame','x','y'])
#                print(folder[camera]+'/'+filename)
#                print(start,end)
                for i in range(start,end):
                    row=df.loc[i]
                    if row['x']<150:
                        output[camera].append([0,0])
                    else:
                        output[camera].append([row['x'],row['y']])
            else:   
                for i in range(start,end):
                   output[camera].append([0,0])
    
    final_output=[]
    for i in range(14401):
        largest=0
        location=[i,0,0,0]
        for camera in cameras:
            output[camera][i][0]
            if largest<output[camera][i][0]:
                largest=output[camera][i][0]
                location=[i]+output[camera][i]+[camera]
        final_output.append(location)
                    
    compiled_file = open(output_directory+'/'+ID+'_locations.txt','w') 
    for row in final_output:
        compiled_file.write(str(row[0])+','+str(row[1])+','+str(row[2])+','+str(row[3])+'\n')
    compiled_file.close()
