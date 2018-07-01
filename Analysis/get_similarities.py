import community
import pandas as pd
import networkx as nx
import numpy as np
import pickle as pk
import matplotlib.pyplot as plt
import os
import random
from scipy.stats import ks_2samp
###############################################
def distance(x,y):
    #is it in top left quadrant of box? (top_left=1 if true, 0 otherwise)
    top_left=(int(y/26)-2*int(y/52))*(1-int(x/53)) 
    #how many more walls are there to walk around?
    more_walls=int(y/52)
    #total vertical distance    
    d=y    
    #horizontal distance to the left
    d=d+x
    #distance to go around first wall
    d=d+2*top_left*(53-x)
    #distance to go around other walls
    d=d+2*53*more_walls
    return d
##############################################


for col in ['1','2','3']:
    for den in ['high','low']:        
#        files=os.listdir('../../Tracking_codes/Corrected/Colony_'+col+'_'+den+'_density_corrected')
        files=os.listdir('../Data/Ant_locations/Colony_'+col+'_'+den+'_density')
        ID_list=[]
        for file in files:
            s=file.find('_',0)
            ID=file[0:s]
            ID_list.append(ID)
        ID_list=list(set(ID_list))
        for x in ['A','B','corpse']:
            if x in ID_list:
                ID_list.remove(x)
        ################################################
        print(col,den,len(ID_list))
        T=14400
        n=0
        distances={}
        mean=[]
        #ID_list=ID_list[0:5]
        node_order=[]
        for ID in ID_list:
            n=n+1
            print(n,ID)
#            loc_df=pd.read_csv('../../Tracking_codes/Interpolated/Colony_'+col+'_'+den+'_density_interpolated/'+ID+'_locations.txt',sep=',',names=['time','x','y'])
            loc_df=pd.read_csv('../Data/Ant_locations/Colony_'+col+'_'+den+'_density/'+ID+'_locations.txt',sep=',',names=['time','x','y'])

            loc_df=loc_df[loc_df['time']<T]
            distances[ID]=[]
            previous=None
            distance_moved=0
            number_of_steps=0
            for i,row in loc_df.iterrows():
                ##############################################################################
                if previous!=None:
                    step_size=((previous['x']-row['x'])**2+(previous['y']-row['y'])**2)**(1/2)
                    distance_moved=distance_moved+step_size
                    if row['x']>0:
                        number_of_steps=number_of_steps+1
                previous={'x':row['x'],'y':row['y']}
                ##############################################################################
                dist_to=distance(row['x'],row['y'])
                if dist_to>0:
                    distances[ID].append(dist_to)
            mean=np.mean(distances[ID])
            std=np.std(distances[ID])
            median=np.median(distances[ID])
            node_order.append([ID,mean,std,max(distances[ID]),min(distances[ID]),distance_moved/number_of_steps,median])
        node_order=sorted(node_order, key=lambda item: item[1], reverse=False)
        
        ID_list=[i[0] for i in node_order]
        N=len(ID_list)
        

        D=[distances[ID] for ID in ID_list]
       
        KS_dict={}
        Similarity={}
        for i in range(N-1):
            for j in range(i+1,N):
                KS=ks_2samp(D[i],D[j])
                KS_dict[(i,j)]=KS[0]
                KS_dict[(j,i)]=KS[0]
                Similarity[(ID_list[i],ID_list[j])]=1-KS[0]
                Similarity[(ID_list[j],ID_list[i])]=1-KS[0]
                
        pk.dump(Similarity,open('../Pickles/Similarity_'+col+'_'+den+'.p','wb'))
        pk.dump(ID_list,open('../Pickles/ID_list_'+col+'_'+den+'.p','wb'))
        pk.dump(node_order,open('../Pickles/node_order_'+col+'_'+den+'.p','wb'))


            