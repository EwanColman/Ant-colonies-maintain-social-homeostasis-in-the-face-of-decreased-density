import networkx as nx

def nodes_and_edges(Weight):
    ID_list=sorted(list(set([edge[0] for edge in Weight]+[edge[1] for edge in Weight])))
    #ID_list=list(set([edge[0] for edge in Weight]+[edge[1] for edge in Weight]))
    edge_list=[]
    #make an adjacency list
    neighbors={}
    for ID in ID_list:
        neighbors[ID]=[ID] 
    
    for edge in sorted(list(Weight.keys())):
        if (edge[1],edge[0]) not in edge_list:
            edge_list.append(tuple(sorted(edge)))
            neighbors[edge[0]].append(edge[1])
            neighbors[edge[1]].append(edge[0])
    
    return ID_list,edge_list,neighbors

def get_totals(Weight,ID_list,edge_list):
    strength={}
    #get total similarity for every node
    for ID in ID_list:
        #total_similarity[i]=k_i
        strength[ID]=sum([Weight[edge] for edge in edge_list if edge[0]==ID])+sum([Weight[edge] for edge in edge_list if edge[1]==ID])
    #total_total_similarity=2m
    total_weight=sum([strength[ID] for ID in ID_list])

    return strength,total_weight

#
def modularity2(partition, graph) :
    if type(graph) != nx.Graph :
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = graph.size(weight='weight')
    if links == 0 :
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph :
        com = partition[node]
        deg[com] = deg.get(com, 0.) + graph.degree(node, weight = 'weight')
        for neighbor, datas in graph[node].items() :
            weight = datas.get("weight", 1)
            if partition[neighbor] == com :
                if neighbor == node :
                    inc[com] = inc.get(com, 0.) + float(weight) / 2
                else :
                    inc[com] = inc.get(com, 0.) + float(weight) / 2.

    res = 0.
    for com in set(partition.values()) :
        print('Mod strength 2',deg.get(com, 0.))
        print('Internal 2',inc.get(com, 0.))
        print((inc.get(com, 0.) / (links)))
        res += (inc.get(com, 0.) / links) - (deg.get(com, 0.) / (2.*links))**2
    print()
    return res

def modularity(Weight,color):
    ID_list,edge_list,neighbors=nodes_and_edges(Weight) 
#    module_strength={}  
#    internal={}
#    for c in set(color.values()):
#        module_strength[c]=0
#        internal[c]=0
    strength,total_weight=get_totals(Weight,ID_list,edge_list)

    Q=0
    for edge in edge_list:
        ID1=edge[0]
        ID2=edge[1]
        if color[ID1]==color[ID2]:
            x=Weight[edge]-(strength[ID1]*strength[ID2]/total_weight)
            if ID1==ID2: 
                Q=Q+x/total_weight
            else:
                Q=Q+2*x/total_weight
#            internal[color[ID1]]=internal[color[ID1]]+Weight[edge]
#        for i in [ID1,ID2]:
#            module_strength[color[i]]=module_strength[color[i]]+Weight[edge]

    return Q

def assortativity(Weight,color):
    ID_list,edge_list,neighbors=nodes_and_edges(Weight) 

    strength,total_weight=get_totals(Weight,ID_list,edge_list)
    
    e={}
    a={}
    colors=list(set(color.values()))
    for i in colors:
        e[i]=0
        a[i]=0

    for edge in edge_list:
        
        ID1=edge[0]
        ID2=edge[1]
        if color[ID1]==color[ID2]:
            i=color[ID1]
            e[i]=e[i]+2*Weight[edge]/total_weight
        for ID in [ID1,ID2]:
            i=color[ID1]
            a[i]=a[i]+(Weight[edge]/total_weight)
    
    eii=sum([e[i] for i in colors])
    aibi=sum([a[i]**2 for i in colors])

    r=(eii-aibi)/(1-aibi)

    return r

def modulize(Weight):
    m=0
    #get the nodes and edges
    ID_list,edge_list,neighbors=nodes_and_edges(Weight)
    strength,total_weight=get_totals(Weight,ID_list,edge_list)

    color={}
    colors=[]
    weight_in_color={}
    #assign nodes to groups 
    for i in range(len(ID_list)):
        ID=ID_list[i]
        
        if (ID,ID) not in edge_list:
            Weight[(ID,ID)]=0         
        
        c='c'+str(i)
        color[ID]=c 
        colors.append(c)            
        for ID2 in ID_list:
            if ID2 in neighbors[ID]:
                #at this stage the similarity it has with c is the similarity it has with the only node in c
                weight_in_color[(ID2,c)]=Weight[tuple(sorted((ID2,ID)))]
            else:
                weight_in_color[(ID2,c)]=0
   
    #color_group is the list of nodes in a particular color  
    color_group={}
    
    total_weight_of_color={}
    for c in colors:
        color_group[c]=[ID for ID in ID_list if color[ID]==c]
        #get total similarity for every community 
        total_weight_of_color[c]=sum([strength[i] for i in color_group[c]])
    #get the initial value of Q
    Q=modularity(Weight,color)
    
    N=len(ID_list)
    unimprovable=0
    n=0
    while unimprovable<N:
        
        ID=ID_list[n]
        n=(n+1) % N
        #print(n)
        #source is the community ID is currently in
        source=color[ID]
        #compute the weight of edges between ID and nodes in source community (including itself)
        Similarity_to_source=weight_in_color[(ID,source)]    
        #compute the expectation 
        Expected_similarity_to_source=strength[ID]*total_weight_of_color[source]/total_weight
        
        best_delta=0
        #instead of choosing all possible target communities, rule out the ones ID has no connection to
        for target in [x for x in colors if x!=source]:           
            #compute the weight of edges between ID and nodes in target community (including itself)           
            Similarity_to_target=weight_in_color[(ID,target)]+Weight[(ID,ID)]
            #compute the expectation
            Expected_similarity_to_target=strength[ID]*(strength[ID]+total_weight_of_color[target])/total_weight
            #compute the total change if ID moved from source community to target community
            delta_Q=(Similarity_to_target-Expected_similarity_to_target-Similarity_to_source+Expected_similarity_to_source)*(1/total_weight)    

            #keep track of the largest
            if delta_Q>best_delta:    
                best_delta=delta_Q
                best_target=target
       #print('best_delta:',best_delta)     
        if best_delta>0.00000001:
            m=m+1
            old_Q=0
            for edge in edge_list:
                ID1=edge[0]
                ID2=edge[1]
                if color[ID1]==color[ID2]:
                    x=Weight[edge]-(strength[ID1]*strength[ID2]/(total_weight))
                    old_Q=old_Q+x/(total_weight)
            
            color[ID]=best_target
#            print('targets:',[x for x in colors if x!=source])
#            print(ID,'moved from',source,'to',best_target)
#            print('color_group[source]',color_group[source])
#            print('color_group[best_target]',color_group[best_target])

            
            
            color_group[source].remove(ID)    
            color_group[best_target].append(ID)
            if len(color_group[source])==0:                
                color_group.pop(source)
                colors.remove(source)

            #update the total_similarity of source
            total_weight_of_color[source]=total_weight_of_color[source]-strength[ID]
            #update the total_similarity of target        
            total_weight_of_color[best_target]=total_weight_of_color[best_target]+strength[ID]
            #update similarity to the source/target community of every node
            for ID2 in neighbors[ID]:
                weight_in_color[(ID2,source)]=weight_in_color[(ID2,source)]-Weight[tuple(sorted((ID2,ID)))]
                weight_in_color[(ID2,best_target)]=weight_in_color[(ID2,best_target)]+Weight[tuple(sorted((ID2,ID)))]

            new_Q=0
            for edge in edge_list:
                ID1=edge[0]
                ID2=edge[1]
                if color[ID1]==color[ID2]:
                    x=Weight[edge]-(strength[ID1]*strength[ID2]/(total_weight))
                    new_Q=new_Q+x/(total_weight)                
#            if int((10**10)*(new_Q-old_Q))!=int((10**10)*best_delta):
#                print(m,',',ID,'moved from',source,'to',best_target)
#                print('real change',new_Q-old_Q)
#                print('best_delta',best_delta)           
#                print()
            #reset the counter
            unimprovable=0
        else:
            #if no improvements occur in N iterations then this number reaches N and the loop ends
            unimprovable=unimprovable+1
    
        #update Q
        Q=Q+best_delta      

    ####################### MERGE COMMUNITIES #####################################    
    #create a network where each community is a node

    #colors=sorted(list(color_group.keys()))
    #make a dictionary of edges
    new_weight={}
    for c_i in colors:
        for c_j in colors:
            if (c_j,c_i) not in new_weight:
                new_weight[tuple(sorted((c_i,c_j)))]=0
      
    for edge in edge_list:
        #there are two new edges (one in each direction unless they are the same)
        #new_edges=#set([(color[edge[0]],color[edge[1]]),(color[edge[1]],color[edge[0]])])
        #for new_edge in new_edges:
        new_edge=tuple(sorted((color[edge[0]],color[edge[1]])))
#        if new_edge not in new_similarity:
#            new_edge=(color[edge[1]],color[edge[0]])
        new_weight[new_edge]=new_weight[new_edge]+Weight[edge]

    #print(sum(new_similarity.values()),total_total_similarity)
    return color_group,new_weight

def get_hierarchy(Weight):
    community={}
    old_sim=0
    new_sim=1
    n=0
    #stopping criteria: no change has occured
    while old_sim!=new_sim:
        n=n+1        
        #partition produces 0) the partition 1) a dictionary of similarities between groups partition 
        one_pass=modulize(Weight)
        #reassign
        com=one_pass[0]
        
        old_sim=len(Weight)
        Weight=one_pass[1]
        new_sim=len(Weight)

        if n==1:
            community[n]=com
        else:
            community[n]={}
            for color in com:
                community[n][color]=sum([community[n-1][i] for i in com[color]],[])
    return community

def get_communities(weight):
    Weight=weight.copy()
    community=get_hierarchy(Weight)
    
    new_community=community[len(community)]   
    
    output={}
    i=0                  
    for c in new_community:
        output[i]=new_community[c]
        i=i+1
    return output

def get_m_communities(W,m):
    #W is the original graph which we will need later
    Weight=W.copy()
    community=get_hierarchy(W)    
    n=len(community)
    
    #m is the required number of modules
    ID_list,edge_list,neighbors=nodes_and_edges(Weight)
    #community is a dictionary of dictionaries
    initial_partition={}    
    for i in range(len(ID_list)): 
        initial_partition[i]=[ID_list[i]]
    community[0]=initial_partition
    
    #find the level (n) for which the number of communities is either correct or too large     
    while len(community[n])<m: 
        n=n-1
    new_community=community[n]
    
    while len(new_community)>m:  
        #make the color disctionary        
        color={}
        for c in new_community:
            nodes=new_community[c]
            for node in nodes:
                color[node]=c
        #get the best two modules to combine      
        best_modularity=0
        colors=list(new_community.keys())
        for i in range(len(colors)-1):
            c1=colors[i]
            for j in range(i+1,len(colors)):
                c2=colors[j]
                new_color=color.copy()   
                for node in new_community[c1]:
                    new_color[node]=c2
                #here you really want to calculate the expected change yu would get from combining the two
                new_modularity=modularity(W,new_color)
                if new_modularity>best_modularity:
                    best_modularity=new_modularity
                    best_color=new_color.copy()
        print('number_of_colors',len(set(best_color.values())))
        new_community={}
        for c in set(best_color.values()):
            new_community[c]=[]
        for node in best_color:
            new_community[best_color[node]].append(node)            
    
    #convert community names to integers
    output={}
    i=0                  
    for c in new_community:
        output[i]=new_community[c]
        i=i+1
    
    return output
    

