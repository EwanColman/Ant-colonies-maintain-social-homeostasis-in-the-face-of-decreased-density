
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

global output_df
global p

def reduce(df):
    new_df=pd.DataFrame(columns=('Location','Ant_ID', 'Ant_ID_(partner)', 'start_time','end_time','duration')) 
    list_of_rows=[]
    n=0
    for i,row in df.iterrows():
        if row['Ant_ID']=='q':
            ID1='Queen'
        else:
            ID1=row['Ant_ID']

        if row['Ant_ID_(partner)']=='q':
            ID2='Queen'
        else:
            ID2=row['Ant_ID_(partner)']
            
        norm_row=[ID1, ID2, row['synced_start'],row['synced_end'],row['synced_end']-row['synced_start']]
        alt_row=[ID2, ID1, row['synced_start'],row['synced_end'],row['synced_end']-row['synced_start']]
       
        if alt_row in list_of_rows:
            #pass
            n=n-1    
        else:
            n=n+1
            new_df.loc[len(new_df)]=[row['Location'],str(ID1), str(ID2), row['synced_start'],row['synced_end'],row['synced_end']-row['synced_start']]
            list_of_rows.append(norm_row)
            #print(len(list_of_rows))
        if n>1:
            print(row)
            n=n-1
    return new_df
    
for colony in [1,2,3]:
    for density in ['high','low']:
        working_df=pd.read_excel('Colony_'+str(colony)+'_trophallaxis_final.xlsx',sheetname=density+' density')
  #      working_df=pd.read_excel('Colony_'+str(colony)+'_trophallaxis_12_hours.xlsx')
    #    working_df=pd.read_excel('Colony_2_trophallaxis_data_fixed_half_second_issue.xlsx',sheetname=density+' density')        
        
        working_df=working_df.sort('synced_start')
        print(working_df.head())
#        ID_list=[]
#        ID_dict={}
#        for ID in working_df['Ant_ID']:
#            if ID in ID_list:
#                pass
#            else:
#                ID_list.append(ID)
#                ID_dict[ID]=len(ID_list)-1
                
        print(working_df.head())
        print(len(working_df))
        working_df=reduce(working_df)
        print(working_df.head())
        print(len(working_df))
        
        working_df.to_csv('Colony_'+str(colony)+'_'+density+'_formatted.txt', sep='\t')
    
#
#


            
        
    
    
    
    