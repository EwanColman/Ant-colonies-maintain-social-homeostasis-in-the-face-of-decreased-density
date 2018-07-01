import pickle as pk
import pandas as pd
import Louvain
import numpy as np

for col in ['1']:
    for den in ['high']:
    
    ######################################################        

        
        Similarity=pk.load(open('../Pickles/Similarity_'+col+'_'+den+'.p','rb'))
        weight={}
        nodes=[]
        for edge in Similarity:
            nodes.append(edge[0])
            nodes.append(edge[1])
            ordered=tuple(sorted((edge[0],edge[1])))  
            #print(ordered)                    

#        N=len(set(nodes))
#        print(N,N*(N-1))
            if ordered not in weight:
                weight[ordered]=Similarity[edge]

        community=Louvain.get_communities(weight)
        
        nodes=set(nodes)
        #print(community)
        actual_color={}
        for c in community:
            for ID in community[c]:
                actual_color[ID]=c
        actual=community.copy()        

        
        #beta is the shape parameter
        beta=4
        changes=[]
        perturbations=[]
        for t in range(100):
            new_weight={}
            total_change=0
            number_of_edges=0
            for edge in weight:          
                mean=weight[edge]
                if mean==0:
                    mean=0.0001
                alpha=mean*beta/(1-mean)
                new_weight[edge]=np.random.beta(alpha,beta)
                total_change=total_change+abs(mean-new_weight[edge])
                number_of_edges=number_of_edges+1

            
            # recalculate communities with new edge weights
            community=Louvain.get_communities(new_weight)

            color={}
            for c in community:
                for ID in community[c]:
                    color[ID]=c
            perturbations.append(total_change/number_of_edges)

           
            ID_list=list(color.keys())
            N=len(ID_list)
       
            count=0
            for ID in ID_list:
                c1=actual_color[ID]
                c2=color[ID]
                numerator=len([i for i in actual[c1] if i in community[c2]])
                denominator=min(len(actual[c1]),len(community[c2]))
                
                if numerator/denominator<0.5:
                    count=count+1
            changes.append(count/N)
            
        print('Mean similarity change:',np.mean(perturbations))
        print('% nodes that changed group:',np.mean(changes))
        print()
        
        
        #        correct=0
#        wrong=0
#        for i in range(N):
#            for j in range(i+1,N):
#                if color[ID_list[i]]==color[ID_list[j]]:
#                    bootstrap_together=True
#                else:
#                    bootstrap_together=False
#                
#                if actual_color[ID_list[i]]==actual_color[ID_list[j]]:
#                    actual_together=True
#                else:
#                    actual_together=False
#                    
#                    
#                if actual_together==bootstrap_together:
#                    correct=correct+1
#                else:
#                    wrong=wrong+1
#                    
#        print(2*correct/(N*(N-1)))
        
        #            M=[]
#            #N=[]
#            for a in actual:
#                m=[]
#                #n=[]
#                for c in community:
#                    m.append(len([ID for ID in community[c] if ID in actual[a]]))
#                    #n.append(len(community[c])*len(actual[a])/len(color))
#                M.append(m)
#                #N.append(n)
#            print(np.array(M))
#            print()
        