import pandas as pd
import pickle as pk
import os

excel_file='SGL15HD_4_hours'
col='3'
den='high'

df=pd.read_csv('Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str}).dropna()
ID_list=[]
files=os.listdir('Boxed/Colony_'+col+'_'+den+'_density_boxed')
for file in files:
    ID=file[0:len(file)-14]
    ID_list.append(ID)


#df=df[(df['end_time']<8200)]

big_list=[[] for i in range(14401)]

count=0
for i,row in df.iterrows():
    print(i)
    ID1=row['Ant_ID']
    ID2=row['Ant_ID_(partner)']
    if ID2=='q':
        ID2='Queen'
    if ID1=='q':
        ID1='Queen'
    if ID1 in ID_list and ID2 in ID_list:   
    
        loc_df1=pd.read_csv('Boxed/Colony_'+col+'_'+den+'_density_boxed/'+ID1+'_locations.txt',sep=',',names=['x','y'])
        loc_df2=pd.read_csv('Boxed/Colony_'+col+'_'+den+'_density_boxed/'+ID2+'_locations.txt',sep=',',names=['x','y'])
        start_time=max(1,int(row['start_time']))
        end_time=min(14401,int(row['end_time']))
        for t in range(start_time,end_time):
            l1=loc_df1.loc[t]
            l2=loc_df2.loc[t]
            big_list[t].append([[l1['x'],l1['y']],[l2['x'],l2['y']]])
                
pk.dump(big_list,open('trophallaxis_locations_'+col+'_'+den+'.p','wb'))
#we want a list of 14400 lists, each containing the start and end points of the line
    