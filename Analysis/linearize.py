import random

def linearity(ID_list,edge_list):
    position={}    
    i=0    
    for ID in ID_list:
        position[ID]=i
        i=i+1
        neighbors={}

    for ID in ID_list:
        neighbors[ID]=[]

    for edge in edge_list:
        ID1=edge[0]
        ID2=edge[1]
        neighbors[ID1].append(ID2)
        neighbors[ID2].append(ID1)
        
    lin=0
    for ID1 in ID_list:
        #add distance to each neighbor 
        for ID2 in neighbors[ID1]:
            lin=lin+abs(position[ID2]-position[ID1])
    return lin

def linearize(edge_list):
    ID_list=list(set([edge[0] for edge in edge_list]+[edge[1] for edge in edge_list]))  
    N=len(ID_list)
    #print('N',N)
    #ID_list=random.sample(ID_list,N)
    degree=[]
    for ID in ID_list:
        deg=len([e for e in edge_list if e[0]==ID or e[1]==ID])
        degree.append([ID,deg])
    new_degree=sorted(degree,key=lambda x: x[1],reverse=False)
    ID_list=[a[0] for a in new_degree]    
    
    neighbors={}
    for ID in ID_list:
        neighbors[ID]=[]    
    
    for edge in edge_list:
        ID1=edge[0]
        ID2=edge[1]
        neighbors[ID1].append(ID2)
        neighbors[ID2].append(ID1)

    best_linearity=linearity(ID_list,edge_list)
    best_ID_list=ID_list.copy()
    for j in range(100):
        ID_list=best_ID_list.copy()
        #how many do we want to randomize?
        sample_size=int(N/10)
        #choose some random IDs
        samp1=random.sample(ID_list,sample_size)
        samp2=random.sample(samp1,sample_size)
        for s in range(sample_size):
            k=ID_list.index(samp1[s])
            ID_list[k]=samp2[s]
#            
        
        position={}
        i=0
        for ID in ID_list:
            position[ID]=i
            i=i+1
         
        left_of={}
        right_of={}
        for ID in ID_list:
            left_of[ID]=len([i for i in neighbors[ID] if position[i]<position[ID]])
            right_of[ID]=len([i for i in neighbors[ID] if position[i]>position[ID]])
              
        
        improvable=True
        
        while improvable==True:
            best_improvement=0
            for i in range(N-1): 
    #       for j in range(1000): 
    #            i=int((N-1)*random.random())
                #choose consecutive neighbors
                ID1=ID_list[i]
                ID2=ID_list[i+1] 

                #calculate the improvement 
                #ID1 moves to the right so anything to the right of it gets closer (by 1)
                #anything to the left of it gets farther (by 1), opposite is true for ID2
                
                #if a neighbor switches from being on the right to the left then the distance doesn't change
                if sorted((ID1,ID2)) in edge_list:        
                    improvement=2*((right_of[ID1]-1-left_of[ID1])+(left_of[ID2]-1-right_of[ID2]))
                else:
                    improvement=2*((right_of[ID1]-left_of[ID1])+(left_of[ID2]-right_of[ID2]))
                if improvement>best_improvement:
                    best_improvement=improvement
                    best_swap=[ID1,ID2]

            if best_improvement<=0:
                improvable=False
            else:
                #improvements can be made 
                improvable=True
                ID1=best_swap[0]
                ID2=best_swap[1]
                #update the positions and the ID list with switched values
                ID_list[position[ID1]]=ID2
                ID_list[position[ID2]]=ID1
                
                position[ID1]=position[ID1]+1
                position[ID2]=position[ID2]-1
                
                if sorted((ID1,ID2)) in edge_list:
                    right_of[ID1]=right_of[ID1]-1
                    left_of[ID1]=left_of[ID1]+1
                    right_of[ID2]=right_of[ID2]+1
                    left_of[ID2]=left_of[ID2]-1

        l=linearity(ID_list,edge_list)
        if l<best_linearity:
            best_linearity=l
            best_ID_list=ID_list.copy()
        #print(j,best_linearity)
    return best_ID_list
###############################################################################

