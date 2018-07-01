import matplotlib.pyplot as plt
import pandas as pd
import pickle as pk
from matplotlib.path import Path
import matplotlib.patches as patches

import numpy as np



for col in ['1','2','3']:    

    df=pd.read_csv('../Results/Node_attributes_colony_'+col+'.csv')
    if col=='1':
        for i,row in df.iterrows():
            print(i,row['Spatial_group_low'])
            if row['Spatial_group_low']==2:
                df.set_value(i, 'Spatial_group_low', 3)
                print(df.ix[i]['Spatial_group_low'])
    
    N=len(df)
    
    
    fig=plt.figure(figsize=(4,3))
    ax=fig.add_subplot(111)   
    ax.set_xlim([-0.1,1.1])
    ax.set_ylim([-10,135])
    #ax.set_title('Colony '+col,size=30)    
    
    x=0  
    group={}
    gap={}
    group_numbers={}
    number_of_groups={}
    for den in ['high','low']:
        
        group[den]={}
        for i,row in df.iterrows():
            ID=row['ID']
            #Get group
            group[den][ID]=row['Spatial_group_'+den]          
        
#        if col=='1' and den=='low':
#            for ID in group['low']:
#                if group['low'][ID]==2:                
#                    group['low'][ID]=3
        
        ##########################################################
        #if 3 in group[den].values():
        group_colour={0:'k',1:'#ff000c',2:'#4baf48',3:'#1b6cd1'}
#        else:
#            group_colour={1:'#ff000c',2:'#1b6cd1'}
#        if den=='high':
#            group_colour[0]='m'
#        else:
#            group_colour[0]='k'
        ##########################################################        
        group_numbers[den]=list(set(group[den].values()))#list(sorted(set(df['Spatial_group_'+den])))        
        print('numbers', group_numbers[den])
        #calculate the gap
        number_of_groups[den]=len(group_numbers[den])
        print(number_of_groups[den])
        gap[den]=(125-N)/(number_of_groups[den]-1)
        #get sizes
        
        y=0
        for n in group_numbers[den]:
            group_size=len(df[df['Spatial_group_'+den]==n])
            print(n,group_size)
            
            patch = patches.Rectangle((x,y),-0.05,group_size, facecolor=group_colour[n], lw=0,alpha=0.9)                
            ax.add_patch(patch)
            if den=='high':
                shift=-0.1
            else:
                shift=0.03
            #ax.text(x+shift,y-2+group_size/2,n,fontsize=30)          
            y=y+group_size+gap[den]
        x=x+1.03
        
    #find the values to plot lines
    
    #matrix of group pair sizes
    size=[]
    for n in group_numbers['high']:
        s=[]
        for m in group_numbers['low']:
            s.append(len(df[(df['Spatial_group_high']==n)&(df['Spatial_group_low']==m)]))         
        size.append(s)

     
    #row and column sums
    H=[]        
    for n in range(number_of_groups['high']):
        H.append(sum(size[n][0:len(group_numbers['low'])]))
    L=[]
    for m in range(number_of_groups['low']):   
        L.append(sum([size[i][m] for i in range(len(group_numbers['high']))]))

    
    for s in range(len(size)):
        print(size[s],H[s])
    
    print(L)
    print()
    
    edge_color={(0,0):'k',
                (0,1):'#703c41',
                (1,0):'#703c41',
                (0,2):'#346d45',
                (2,0):'k',
                (0,3):'k',
                (3,0):'k',
                (1,1):'#ff000c',
                (1,2):'#d1d11b',
                (2,1):'#d1d11b',
                (1,3):'#ca80d6',
                (3,1):'#ca80d6',
                (2,2):'#4baf48',
                (2,3):'#17c7d1',
                (3,2):'#17c7d1',
                (3,3):'#1b6cd1'}

    
    
    for n in range(number_of_groups['high']):
        for m in range(number_of_groups['low']):
            
            #high
            first_bit=sum([H[i]+gap['high'] for i in range(n)])
            second_bit=sum([size[n][i] for i in range(m)])

            y_high=first_bit+second_bit

            #low
            first_bit=sum([L[i]+gap['low'] for i in range(m)])
            second_bit=sum([size[i][m] for i in range(n)])

            y_low=first_bit+second_bit   

            if size[n][m]>0:
                x=[i/100 for i in range(100)]
                y_bottom=[(1/2)*(y_high*(np.cos(np.pi*i)+1)+(1-np.cos(np.pi*i))*y_low) for i in x]                
                y_top=[i+size[n][m] for i in y_bottom]
                
                ax.fill_between(x,y_bottom,y_top,color='#ad9a8a',linewidth=0,alpha=0.5) #edge_color[(group_numbers['high'][n],group_numbers['low'][m])]    

    
    ax.text(-0.05,135,'High',fontsize=30)
    ax.text(0.75,135,'Low',fontsize=30)
           
    ax.axis('off')
    plt.savefig('../Results/group_change_'+col+'.pdf', format='pdf',bbox_inches='tight',dpi=512)
#