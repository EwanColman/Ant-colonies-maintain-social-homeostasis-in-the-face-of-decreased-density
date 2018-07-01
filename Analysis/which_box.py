import pandas as pd
import numpy as np
import pickle as pk
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import os
import random

global col
global den

def which_box(x):
    b=0
    while x>b*52:
        b=b+1
    return b
        



col='1'
den='low'

output={}
##############################################
for col in ['1','2','3']:
        
    print()
    print('Colony',col)
    plt.figure()
    files=os.listdir('../Data/Ant_locations/Colony_'+col+'_'+den+'_density')
    ID_list=[]
    
    for file in files:
        s=file.find('_',0)
        ID=file[0:s]
        ID_list.append(ID)
    ID_list=list(set(ID_list))
    if 'corpse' in ID_list:
        ID_list.remove('corpse')
    ################################################
    number_of_ants={}
    for box in [0,1,2,3,4]:
        number_of_ants[box]=[0 for t in range(14401)]
    
    n=0
    for ID in ID_list:
        loc_df=pd.read_csv('../Data/Ant_locations/Colony_'+col+'_'+den+'_density/'+ID+'_locations.txt',sep=',',names=['time','x','y','box'])

        s=0
        for x in loc_df['x']:
            b=which_box(x)
            number_of_ants[b][s]=number_of_ants[b][s]+1
            s=s+1
         
    for box in [0,1,2,3,4]: 
        plt.plot(number_of_ants[box])


    output_file = open('../Results/number_of_ants_in_each_box_'+col+'.csv','w') 
    output_file.write('time,Box 1,Box 2,Box 3,Box 4\n')
    for i in range(14400): 
        str1=str(i+1)+','
        for box in [1,2,3,4]:
            str1=str1+str(number_of_ants[box][i])+','
        str1=str1+'\n' 
        output_file.write(str1)
    output_file.close()
#        
        
