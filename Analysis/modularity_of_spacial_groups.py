
##################################################################
#spatial similarity between groups

import community
import networkx as nx
import matplotlib.pyplot as plt
import pickle as pk
import pandas as pd
from random import shuffle
import Louvain
import numpy as np
import scipy.stats as st

fig=plt.figure(figsize=(4,5))

fs=20
m=-0.6
shape={'1':'D','2':'^','3':'s'}
marker_size={'1':60,'2':90,'3':70}
for col in ['1','2','3']:
    m=m+0.3
    n=m
    attribs=pd.read_csv('../Results/Node_attributes_colony_'+col+'.csv') 
    ID_list=attribs['ID'].tolist()
    for den in ['high','low']:
        ax=fig.add_subplot(111)
        n=n+1
        print(col,den)
        color={}
        for ID in ID_list:
            attrib='Spatial_group_'+den
            row=attribs[attribs['ID']==ID].iloc[0]
            color[ID]=row[attrib]
           
        df=pd.read_csv('../Data/Trophallaxis/Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna() 


        #ID_list=list(set(pd.concat([df['Ant_ID'],df['Ant_ID_(partner)']])))
                
        Weight={}
        for i,row in df.iterrows():
            ID1=str(row['Ant_ID'])
            ID2=str(row['Ant_ID_(partner)'])
            duration=row['end_time']-row['start_time']
            if ID1=='q':
                ID1='Queen'
            if ID2=='q':
                ID2='Queen'

            ordered=tuple(sorted((ID1,ID2)))
            if ordered in Weight:
                Weight[ordered]=Weight[ordered]+duration
            else:
                Weight[ordered]=duration
            #Weight[ordered]=1
            
        actual_modularity=Louvain.modularity(Weight,color)
        #print('Modularity:',actual_modularity)

        assortativity=Louvain.assortativity(Weight,color)
        print('Assortativity:',assortativity)

         
        comm=Louvain.get_communities(Weight)
        #######################################################################    
        # Use jackknife method to get the variance
        variance=0
        for edge in Weight:
        # loop over all the edges
            #remove an edge 
            new_weight=Weight.copy()
            new_weight.pop(edge)
            #and calculate assortativity
            jackknife_assortativity=Louvain.assortativity(new_weight,color)        
                #subtract from original result, square, add to the running total
            variance=variance+(jackknife_assortativity-assortativity)**2
            
        sd=np.sqrt(variance)
        print('Standard deviation:',sd)
        
        print('Standard deviations from 0:',assortativity/sd)
        print('p-value:',2*st.norm.sf(assortativity/sd))        
        
        
        ax.plot([n,n],[assortativity+sd,assortativity-sd],zorder=1,color='k',linewidth=2)
        ax.plot([n-0.03,n+0.03],[assortativity+sd,assortativity+sd],zorder=1,color='k',linewidth=2)
        ax.plot([n-0.03,n+0.03],[assortativity-sd,assortativity-sd],zorder=1,color='k',linewidth=2)
        ax.scatter([n],[assortativity],marker=shape[col],zorder=2,facecolor='w',linewidth=2,s=marker_size[col],c='k')
    ax.text(0.7,0.735-m/4,'Colony '+col,size=fs)
    ax.scatter([0.6],[0.76-m/4],marker=shape[col],zorder=2,facecolor='w',linewidth=2,s=marker_size[col],c='k')
ax.plot([1.5,1.5],[-0.2,1],':',linewidth=2,color='k')
ax.set_ylabel('Assortativity',size=fs)
ax.set_xlabel('Density',size=fs)
ax.plot([0,2.5],[0,0],'k',linewidth=2)
plt.yticks([-0.2,0,0.2,0.4,0.6,0.8],size=fs)
plt.xticks([1,2],['High','Low'],size=fs)

plt.ylim([-0.22,0.9])
plt.xlim([0.5,2.5])
plt.savefig('../Results/assortativity.pdf', format='pdf',bbox_inches='tight',dpi=512)
#        color={}
#        for c in comm:
#            nodes=comm[c]
#            for node in nodes:
#                color[node]=c
#                
#                    
#        maximum_modularity=Louvain1.modularity(Weight,color)
##        print('max:',maximum_modularity)
#       
#
#        G=nx.Graph()
#        total_weight=0
#        for edge in Weight:
#            G.add_edge(edge[0],edge[1],weight=1)
#
#        
#        p=community.best_partition(G)
##        print('network x:',Louvain1.modularity(Weight,p))
##        print('clustering:',nx.average_clustering(G))
#        print()


  
#        edges=[]
#        for w in Weight:
#            edges.append([w[0],w[1]])
#        
#        count=0
#        for t in range(1000):
#            Weight={}
#            perm=list(np.random.permutation(len(edges)))
#            for i in range(len(edges)):
#                new_edge=tuple(sorted((edges[i][0],edges[perm[i]][1])))
#                Weight[new_edge]=1
#    
#            
#    
#            modularity=Louvain1.modularity(Weight,color)
#            if modularity>actual_modularity:
#                count=count+1
#        print(count)
#        print(count/1000)
