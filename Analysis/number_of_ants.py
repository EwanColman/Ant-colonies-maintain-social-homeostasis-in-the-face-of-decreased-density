import pandas as pd
import matplotlib.pyplot as plt
import pickle

output={}

for col in ['1','2','3']:
    print()
    print('Colony',col)
    for den in ['high','low']:
        output[col+den]=[0]
        
        print(den,'density')
        df=pd.read_csv('../Data/Trophallaxis/Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str})#.dropna() 
        #ID_list=list(set(pd.concat([df['Ant_ID'],df['Ant_ID_(partner)']]))) 
        previous_start_time=0        
        ID_list=[]
        times=df['start_time'].tolist()
        for t in range(14401):
            if t in times:
                temp_df=df[df['start_time']==t]
                new_IDs=pd.concat([temp_df['Ant_ID'],temp_df['Ant_ID_(partner)']]).tolist()
                ID_list=list(set(ID_list+new_IDs))
            output[col+den].append(len(ID_list))
        print(ID_list)
        print()
output_file = open('../Results/number_of_ants.csv','w') 
output_file.write('time,1 high,1 low,2 high,2 low,3 high,3 low\n')

for i in range(14401): 
    str1=str(i)+','
    for col in ['1','2','3']:
        for den in ['high','low']:
           str1=str1+str(output[col+den][i])+','+str()
    str1=str1+'\n' 
    output_file.write(str1)
output_file.close()

        