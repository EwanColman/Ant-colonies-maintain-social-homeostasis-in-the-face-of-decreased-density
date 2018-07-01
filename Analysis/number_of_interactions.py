import pandas as pd

output1={}
output2={}

for col in ['1','2','3']:
    print()
    print('Colony',col)
    for den in ['high','low']:
        output1[col+den]=[0]
        output2[col+den]=[0]
        
        print(den,'density')
        df=pd.read_csv('../Data/Trophallaxis/Colony_'+col+'_'+den+'_formatted.txt',sep='\t',dtype={'Ant_ID':str,'Ant_ID_(partner)':str})#.dropna() 
        #ID_list=list(set(pd.concat([df['Ant_ID'],df['Ant_ID_(partner)']]))) 
        number_of_interactions=[0 for i in range(14401)]
        cumulative_interactions=[0 for i in range(14401)]
        for i,row in df.iterrows():
            for t in range(int(row['start_time']),int(row['end_time'])):
                number_of_interactions[t]=number_of_interactions[t]+1
            
            for u in range(int(row['start_time']),14401):       
                cumulative_interactions[u]=cumulative_interactions[u]+1

        cumulative_duration=[]
        for t in range(14401):
            cumulative_duration.append(sum(number_of_interactions[0:t]))
            
            
        output1[col+den]=cumulative_interactions
        output2[col+den]=cumulative_duration

output_file = open('../Results/cumulative_interactions.csv','w') 
output_file.write('time,1 high,1 low,2 high,2 low,3 high,3 low\n')

for i in range(14401): 
    str1=str(i)+','
    for col in ['1','2','3']:
        for den in ['high','low']:
           str1=str1+str(output1[col+den][i])+','+str()
    str1=str1+'\n' 
    output_file.write(str1)
output_file.close()

output_file = open('../Results/cumulative_duration.csv','w') 
output_file.write('time,1 high,1 low,2 high,2 low,3 high,3 low\n')

for i in range(14401): 
    str1=str(i)+','
    for col in ['1','2','3']:
        for den in ['high','low']:
           str1=str1+str(output2[col+den][i])+','+str()
    str1=str1+'\n' 
    output_file.write(str1)
output_file.close()

        