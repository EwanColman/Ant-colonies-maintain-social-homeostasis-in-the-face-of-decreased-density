import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib import cm
import matplotlib.patches as patches
import pandas as pd
import math
import linearize as lin



size=75
colour='r'
space=15


for col in ['1','2','3']:
    
    for den in['high','low']:
        df=pd.read_csv('../Results/Node_attributes_colony_'+col+'.csv')
        number_of_groups=len(set(df['Spatial_group_'+den]))
        
        
        
        
        
        
        #read the trophallaxis data
        df1=pd.read_csv('../Data/Trophallaxis/Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna() 
        #create the edgelist
        ID_list=list(set(df1['Ant_ID']))
        edge_list=[]
        for ID1 in ID_list:
            ID_df=df1[(df1['Ant_ID']==ID1)]
            for ID2 in set(ID_df['Ant_ID_(partner)']):
                edge=sorted((ID1,ID2))
                if edge not in edge_list:
                    edge_list.append(edge)
        #get the linearized order of nodes
        #ordered_list=lin.linearize(edge_list)
        #give a number to each ID
        order={}
        i=0
        for ID in ID_list:
            order[ID]=i
            i=i+1
        
        
        #N will be the total number of positions
        group={}
        # -1 only if group 0 not included
        space=60/(number_of_groups-1)
        print(space)
        N=0
        for i,row in df.iterrows():
            N=N+1
            #color[row['ID']]=row['spatial_group_'+den]
            if row['Spatial_group_'+den] not in group:    
                group[row['Spatial_group_'+den]]=[row['ID']]
                #for each new group we add an empty space
                N=N+space
            else:
                group[row['Spatial_group_'+den]].append(row['ID'])
        
        # include this to remove dead/outside ants        
        if 0 in group.keys():
            group.pop(0)
            number_of_groups=number_of_groups-1
            N=N-space
#        print(group)        
            
        
        if den=='low':
            outside='k'
        else:
            outside='m'
        
        ##########################################################
        if 4 in group.keys():
            group_colour={0:outside,1:'#ff000c',2:'#fc8f00',3:'#4baf48',4:'#1b6cd1'}
            edge_color={(1,1):group_colour[1],
                        (1,2):'#f96d22',
                        (1,3):'#b2852c',
                        (1,4):'#d04fea',
                        (2,2):group_colour[2],
                        (2,3):'#bbbf00',
                        (2,4):'#ff77c8',
                        (3,3):group_colour[3],
                        (3,4):'#16e5b6',
                        (4,4):group_colour[4]}
        elif 3 in group:
            group_colour={0:outside,1:'#ff000c',2:'#4baf48',3:'#1b6cd1'}
            edge_color={(1,1):group_colour[1],
                        (1,2):'#bbbf00',
                        (1,3):'#d04fea',
                        (2,2):group_colour[2],
                        (2,3):'#16e5b6',
                        (3,3):group_colour[3]}
        else:
            group_colour={0:outside,1:'#ff000c',2:'#1b6cd1'}
            edge_color={(1,1):group_colour[1],
                        (1,2):'#d04fea',
                        (2,2):group_colour[2]}
        
        #start the figure 
        fig=plt.figure(figsize=(10,10))
        
        
        #get positions  
        position={}
        color={}
        #go through each group
        n=0
        

        if 0 in group:
            groups=[i+1 for i in range(number_of_groups-1)]+[0]
        else:
            groups=[i+1 for i in range(number_of_groups)]
        print(groups)
        print(group.keys())
        for g in groups:
            #sort them by degree
            group_edges=[]
            for edge in edge_list:
                if edge[0] in group[g] and edge[1] in group[g]:
                    group_edges.append(edge)
            group_ordered=lin.linearize(group_edges)
            for ID in group[g]:
                if ID not in group_ordered:
                    group_ordered.append(ID)
            group_ordered.reverse()       
            
        #    degree=[]    
        #    for ID in group[g]:
        #        ID_df=df1[(df1['Ant_ID']==ID)|(df1['Ant_ID_(partner)']==ID)]
        #        deg=len(set(set(pd.concat([ID_df['Ant_ID'],ID_df['Ant_ID_(partner)']]))))
        #        #loc=list(df[(df['ID']==ID)]['mean_location_'+den])
        #        #deg=loc[0]
        #        #degree.append([ID,deg])
        #        if ID in order:
        #            degree.append([ID,order[ID]])
        #        else:
        #            degree.append([ID,N+1])
        #    new_degree=sorted(degree,key=lambda x: x[1],reverse=False)
        #    group_ordered=[a[0] for a in new_degree]
        #    even=True
        #    evens=[]
        #    odds=[]
        #    for ID in group_ordered:
        #        if even==True:
        #            evens.append(ID)
        #            even=False
        #        else:
        #            odds=[ID]+odds
        #            even=True
        #    group_ordered=odds+evens
        #    if g==0:
        #        colour='k'
        #    else:
        #        cval=cval+(1/(number_of_groups-1))
        #        #val=(cval+0.11)%1
        #        colour=cm.hsv(((0.11+1-cval)%1))
            colour=group_colour[g]
                
            
            
            x=[]
            y=[]
            #go through each node in the group
            for ID in group_ordered:
                color[ID]=g
                position[ID]=(math.cos(2*math.pi*n/N),math.sin(2*math.pi*n/N))
                x.append(math.cos(2*math.pi*n/N))
                y.append(math.sin(2*math.pi*n/N))
                #move n along for the next node
                n=n+1
            n=n+space
            #draw the nodes
            ax = fig.add_subplot(111)    
            ax.scatter(x,y,s=size,c=colour,lw=0.0,alpha=0.8)
        
        #df1=df1[df1['start_time']<30*60]
        
        
        
        for edge in edge_list:
            #draw and edge!
            ID1=edge[0]
            ID2=edge[1]
            pos=position[ID1]
            x1=pos[0]
            y1=pos[1]
            pos=position[ID2]
            x2=pos[0]
            y2=pos[1]
        
            c=edge_color[tuple(sorted((color[edge[0]],color[edge[1]])))]
        
            d=math.sqrt(((x1-x2)**2)+((y1-y2)**2))
            
            d=(d/2)
            z=0.98
            verts = [
                (z*x1, z*y1),  # P0
                ((1-d)*x1, (1-d)*y1), # P1
                ((1-d)*x2, (1-d)*y2), # P2
                (z*x2, z*y2), # P3
                ]
            
            codes = [Path.MOVETO,
                     Path.CURVE4,
                     Path.CURVE4,
                     Path.CURVE4,
                     ]
            
            path = Path(verts, codes)
        
            ax = fig.add_subplot(111)
            if c=='#d8e000':
                a=1
            else:
                a=0.5    
            
            patch = patches.PathPatch(path,facecolor='none', edgecolor=c,lw=1,alpha=0.5)
            ax.add_patch(patch)
        plt.xlim([-1.1,1.1])
        plt.ylim([-1.1,1.1])
        plt.axis('off')
        plt.savefig('../Results/trophallaxis_network_'+col+'_'+den+'.pdf', format='pdf',bbox_inches='tight',dpi=512)
