
##################################################################
#spatial similarity between groups

import community
import networkx as nx
import matplotlib.pyplot as plt
import pickle as pk
import pandas as pd
from random import shuffle
import Louvain1
import numpy as np


for col in ['1','2','3']:
    fig=plt.figure()
    stats=pd.read_csv('../Results/Node_attributes_colony_'+col+'.csv')
     
    for den in ['high','low']:
        N=len(stats[(stats['Spatial_group_'+den]!=10)])   
        ax=fig.add_subplot(111)
        df=pd.read_csv('../Data/Trophallaxis/Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna() 
        df=df.sort('start_time')
        #ID_list=list(set(pd.concat([df['Ant_ID'],df['Ant_ID_(partner)']])))
        #N=len(ID_list)
        edges=[]
        
        x=[]
        y=[]
        interaction_duration=0
        for i,row in df.iterrows():
            edge=tuple(sorted([row['Ant_ID'],row['Ant_ID_(partner)']]))
            if edge not in edges:
                edges.append(edge)
            
            interaction_duration=interaction_duration+row['end_time']+row['start_time']
            x.append(i)
            y.append(len(edges)/(N*(N-1)))
        ax.plot(x,y)
        density=2*len(edges)/(N*(N-1))
        #ax.plot([0,i],[0,len(edges)/N])
        print(col,den,density)

