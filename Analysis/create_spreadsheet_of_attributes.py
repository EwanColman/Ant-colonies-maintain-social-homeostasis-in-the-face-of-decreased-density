import pickle as pk
import pandas as pd
import Louvain
import numpy as np

outside_high={'1':['598','698'],
              '2':['66','108','424','495','565','702','765','796'],
              '3':['32','429','458','671','699','726','727','763','788','822']}

dead_after_high={'1':['528','598','631','646','698'],
                 '2':[],
                 '3':['71','543','643']}

foragers={'1':['528','594','598','643','646','666','698'],
          '2':['66'],
          '3':['47','699','763']}


cols=['Mean_position','Median_position','nearest_point','furthest_point','Standard_deviation','Mean_speed','Trophallaxis_group','Spatial_group','Number_of_interactions','Trophallaxis_duration','Degree']
    

for col in ['1','2','3']:
    partition={}
    ID_list={}
    for den in ['high','low']:
        ID_list[den]=pk.load(open('../Pickles/ID_list_'+col+'_'+den+'.p','rb'))
    ID_list_combined=list(set(ID_list['high']+ID_list['low']+outside_high[col]))
    
    ######################################################
    forager={}    
    output_df=pd.DataFrame(columns=['ID','Forager'])    
    for ID in ID_list_combined: 
        #forager
        if ID in foragers[col]:
            forager[ID]=True
        else:
            forager[ID]=False
        row=[]
        row.append(ID)
        row.append(forager[ID])
        output_df.loc[len(output_df)]=row 
    
        
        
    for den in ['high','low']:
        print()
        print(col,den)        
             
        node_order=pk.load(open('../Pickles/node_order_'+col+'_'+den+'.p','rb'))
        df=pd.read_csv('../Data/Trophallaxis/Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna() 
             
        spatial_group={}
        trophallaxis_group={}
        position={}
        median={}
        nearest={}
        furthest={}
        std={}
        speed={}
        degree={}
        interactions={}
        duration={}

        for ID in ID_list_combined:

            #network attributes
            ID_df=df[(df['Ant_ID']==ID)|(df['Ant_ID_(partner)']==ID)]
            #degree
            degree[ID]=max(0,len(set(pd.concat([ID_df['Ant_ID'],ID_df['Ant_ID_(partner)']])))-1)
            #interactins
            interactions[ID]=len(ID_df)
            #duration
            duration[ID]=sum(ID_df['end_time'])-sum(ID_df['start_time'])

            if ID in [row[0] for row in node_order]:          
                #position           
                position[ID]=[row[1] for row in node_order if row[0]==ID][0]
                median[ID]=[row[6] for row in node_order if row[0]==ID][0]
                #speed
                std[ID]=[row[2] for row in node_order if row[0]==ID][0]
                #
                nearest[ID]=[row[4] for row in node_order if row[0]==ID][0]
                furthest[ID]=[row[3] for row in node_order if row[0]==ID][0]
                speed[ID]=[row[5] for row in node_order if row[0]==ID][0]
                        
                
            else:
                position[ID]='Outside'
                median[ID]='Outside'
                std[ID]='Outside'
                speed[ID]='Outside'
                nearest[ID]='Outside'
                furthest[ID]='Outside'
                
        ###################spatial_community##########################################        
        
        Similarity=pk.load(open('../Pickles/Similarity_'+col+'_'+den+'.p','rb'))
        if ('Queen', 'Queen') in Similarity:
            print('yeps',Similarity[('Queen', 'Queen')])
        Weight={}
        for edge in Similarity:
            ordered=tuple(sorted((edge[0],edge[1])))
            if ordered not in Weight:
                Weight[ordered]=Similarity[edge]
        community=Louvain1.get_communities(Weight)

        community_order=[]
        for c in community:
            nodes=community[c]
            mean_position=np.mean([position[ID] for ID in community[c]])
            community_order.append([c,mean_position])
        community_order=sorted(community_order, key=lambda item: item[1], reverse=False)
        
        for i in range(len(community)):
            #get name of community
            c=community_order[i][0]
            for ID in community[c]:
                spatial_group[ID]=i+1
                                
        #######################Network Community###################################
        
        Weight={}
        for i,row in df.iterrows():
            ID1=str(row['Ant_ID'])
            ID2=str(row['Ant_ID_(partner)'])
            if ID1=='q':
                ID1='Queen'
            if ID2=='q':
                ID2='Queen'

            ordered=tuple(sorted((ID1,ID2)))
            #weighted by duration            
#            if ordered not in Weight:            
#                Weight[ordered]=0
#            Weight[ordered]=Weight[ordered]+row['duration']
            #unweighted            
            Weight[ordered]=1
        community=Louvain1.get_communities(Weight)

        community_order=[]
        for c in community:
            nodes=community[c]
            mean_position=np.mean([position[ID] for ID in community[c]])
            community_order.append([c,mean_position])
        community_order=sorted(community_order, key=lambda item: item[1], reverse=False)
        
        for i in range(len(community)):
            #get name of community
            c=community_order[i][0]
            for ID in community[c]:
                trophallaxis_group[ID]=i+1
         
   
        ###########################################################################

        new_df=pd.DataFrame(columns=cols)
   
   
        for ID in ID_list_combined:
                                    
            if den=='low' and ID in dead_after_high[col]:
                trophallaxis_group[ID]=0#'Dead'
                spatial_group[ID]=0#'Dead'
            if den=='high' and ID in outside_high[col]:
                trophallaxis_group[ID]=0#'Outside'
                spatial_group[ID]=0#'Outside'
            
            if ID not in trophallaxis_group:
                trophallaxis_group[ID]=0#'Inactive'


#            print('Name:',ID)
#            print('Spatial group:',spatial_group[ID])
#            print('Trohallaxis group:',trophallaxis_group[ID])
#            print('Position:',position[ID])
#            print('Speed',speed[ID])
#            print('Forager:',forager[ID])
#            print('Degree:',degree[ID])
#            print('Interactions:',interactions[ID])
#            print('Duration:',duration[ID])
        

            row=[]

            if not position[ID]=='Outside':
                row.append(str(int(position[ID])))
                row.append(str(int(median[ID])))
                row.append(str(int(nearest[ID])))
                row.append(str(int(furthest[ID])))
                row.append(str(int(std[ID])))
                row.append(str("%.3f" % speed[ID]))
            else:
                 row.append('Outside')
                 row.append('Outside')
                 row.append('Outside')
                 row.append('Outside')
                 row.append('Outside')
                 row.append('Outside')
            
            row.append(str(trophallaxis_group[ID]))
            row.append(str(spatial_group[ID]))
            row.append(interactions[ID])
            row.append(duration[ID])
            row.append(degree[ID])
            
    
            new_df.loc[len(new_df)]=row   
#        print('new_df')
#        print(new_df.head())
        output_df=output_df.join(new_df,lsuffix='_high', rsuffix='_low')
     


        
        
   # final_output=output_df['high'].join(output_df['low'])
#    print('output')
#    print(output_df.head())
    output_df.to_csv('../Results/Node_attributes_colony_'+col+'.csv',index=False)
#    ###########################################################################
#    cols=['ID','spatial_group_high','spatial_group_low','trophallaxis_group_high','trophallaxis_group_low','mean_location_high','mean_speed_high','mean_location_low','mean_speed_low']
#    output_df=pd.DataFrame(columns=cols)
#    for ID in ID_list_combined:
#        ah=[row for row in node_order['high'] if row[0]==ID]
#        if ah==[]:
#            attribs_high=[ID,0,0,0,0]
#        else:
#            attribs_high=ah[0]
#        al=[row for row in node_order['low'] if row[0]==ID]
#        if al==[]:
#            attribs_low=[ID,0,0,0,0]
#        else:
#            attribs_low=al[0]
#        
#        output_df.loc[len(output_df)]=[ID,spatial_group['high'][ID],spatial_group['low'][ID],trophallaxis_group['high'][ID],trophallaxis_group['low'][ID],attribs_high[1],attribs_high[4],attribs_low[1],attribs_low[4]]
#
#
#    new_group={}
#    for den in ['high','low']:
#        print(den)
#        print()
#        for group_type in ['spatial','trophallaxis']:
#            print(group_type)
#            ordered=[]
#            for group_number in set(output_df[group_type+'_group_'+den].tolist()):
#                temp_df=output_df[output_df[group_type+'_group_'+den]==group_number]
#                ordered.append([group_number,sum(temp_df['mean_location_'+den])/len(temp_df)])
#            ordered=sorted(ordered, key=lambda item: item[1], reverse=False)
#            print(ordered)
#            new_group[group_type+'_group_'+den]={}
#            indexes=sorted([ordered[i][0] for i in range(len(ordered))])
#            print(indexes)
#
#            for i in range(len(ordered)):
#                new_group[group_type+'_group_'+den][ordered[i][0]]=indexes[i]
#            print(new_group[group_type+'_group_'+den])
#            print()
#    
#    new_output_df=pd.DataFrame(columns=cols)
#    for i,row in output_df.iterrows():
#        new_row=[]
#        for c in cols:
#            if c in new_group:               
#                new_row.append(new_group[c][row[c]])
#            elif c in ['mean_location_high','mean_speed_high','mean_location_low','mean_speed_low']:  
#                new_row.append(str("%.3f" %  row[c]))           
#            else:
#                new_row.append(row[c])
#        #print(new_row)
#        new_output_df.loc[len(new_output_df)]=new_row   
#    new_output_df.to_csv('Node_attributes_colony_'+col+'.csv')
#    
