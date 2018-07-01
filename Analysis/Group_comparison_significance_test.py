import community
import pickle as pk
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import scipy.stats as st
import numpy as np

def make_matrix(group):
    keys=list(group.keys())
    X=keys[0]
    Y=keys[1]
#    print(X)
#    print(Y)
    M_o=[]
    M_e=[]
    M_j=[]
    for i in range(len(group[X])):
        m_o=[]
        m_e=[]
        m_j=[]
        g_lo=group[X][i]
        for j in range(len(group[Y])):
            g_hi=group[Y][j]

            expected=len(g_hi)*len(g_lo)/N
            observed=len([k for k in g_lo if k in g_hi])
            denomenator=len(list(set(g_lo+g_hi)))
            
#            obs_list.append(observed)
#            exp_list.append(expected)        
            m_j.append(observed/denomenator)
            m_o.append(observed)            
            m_e.append(expected)
        M_o.append(m_o)
        M_e.append(m_e)
        M_j.append(m_j)
    return np.array(M_o),np.array(M_e),np.array(M_j)


# Choose the groups you want to compare
A='Spatial_group_high'
B='Trophallaxis_group_high'


for col in ['1','2','3']:
    print()
    print(col)
    
    df=pd.read_csv('../Results/Node_attributes_colony_'+col+'.csv')    
    
    #remove ants that are outside and that are inactive
    if A[0]=='S' and B[0]=='S':
        pass        
    else:
        df=df[(df[A]>0)&(df[B]>0)]    
    
    
    group={A:[],B:[]}
    for group_type in [A,B]:
        list_of_groups=sorted(list(set(df[group_type].tolist())))
        print(group_type+':',list_of_groups)
        for m in list_of_groups:
            group[group_type].append(df[df[group_type]==m]['ID'].tolist())
        
    
    ID_list=df['ID'].tolist()#
    N=len(ID_list)
    M=make_matrix(group)

    #print(np.transpose(M[1]))
    print(M[0])
    #print(np.transpose(M[0]))
    print()
    #print(M[1])
    #print(M[2])
#    
##    print(np.array(M_o))
##    print(np.array(M_e))
#
    actual_cs,p=st.chisquare(M[0],M[1],axis=None)
    actual_jac=np.sum(M[2])
    print('actual=',actual_cs)
    print('Jaccard=',actual_jac)
    print()  
    
#
######################Significance test########################################
    count1=0
    count2=0
    T=10000
    max_cs=0
    max_jac=0
    for t in range(T):
        new_group={}
        for group_type in [A,B]:
            new_group[group_type]=[]
            fake_list=list(np.random.permutation(len(ID_list)))
            i=0        
            for g in group[group_type]:
                new_group[group_type].append(fake_list[i:i+len(g)])
                i=i+len(g)
        M=make_matrix(new_group)
        
        cs,p=st.chisquare(M[0],M[1],axis=None)
        Jaccard=np.sum(M[2])
        
        if cs>actual_cs:
            count1=count1+1
        if max_cs<cs:
            max_cs=cs

    
        if Jaccard>actual_jac:
            count2=count2+1
        if max_jac<Jaccard:
            max_jac=Jaccard

    print('Chi-square')
    print(count1,'in',T)
    print('p=',count1/T)
    print('max cs',max_cs)
    print()
    print('Jaccard')
    print(count2,'in',T)
    print('max Jaccard',max_jac)
    print()    
    
##############################################################################
    
