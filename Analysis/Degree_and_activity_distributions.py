import matplotlib.pyplot as plt
import pandas as pd 

colour={'high':'r','low':'b'}
h={'Number_of_interactions':11,'Degree':16,'Trophallaxis_duration':15}
w={'Number_of_interactions':90,'Degree':38,'Trophallaxis_duration':90}


p=0
fig=plt.figure(figsize=(17,11))

for col in ['1','2','3']:
    for interaction_type in ['Number_of_interactions','Degree','Trophallaxis_duration']:
        height=h[interaction_type]
        width=w[interaction_type]

        df=pd.read_csv('../Results/Node_attributes_colony_'+col+'.csv')    
        
        p=p+1
        for den in ['high','low']:
            
            ax=fig.add_subplot(3,3,p)
            print()
            print(col)
            
            
        
            print(list(df))
        
            degree=df[interaction_type+'_'+den].tolist()
            if interaction_type=='Trophallaxis_duration':
                degree=[int(i/60) for i in degree]
            total=sum(degree)
            interactions=df['Number_of_interactions_'+den]
        
            dist=[len([i for i in degree if i==j]) for j in range(100)]
           
            s=1
            
            new_dist=[]
            x=[]
            for i in range(1,len(dist)):
                d1=(dist[i]+dist[i-1])/2
                d2=dist[i]
                #d3=(dist[i+1]-dist[i])/2
                
                new_dist=new_dist+[d1,d2]
                x=x+[i-1,i-(1/2)]
                
            ax.fill_between(x,new_dist,color=colour[den],alpha=0.5)
            if den=='high':       
                pos=height-(2/16)*height
            else:
                pos=height-(4/16)*height
            top=[pos+(1/16)*height for i in [0.3*width,0.35*width]]
            bottom=[pos for i in [0.3*width,0.35*width]]
            ax.fill_between([0.3*width,0.35*width],bottom,top,color=colour[den],alpha=0.5)        
            ax.text(0.38*width,pos,den+' (total='+str(int(total))+')',size=20)        
            
            ax.set_xlim([0,width])
            ax.set_ylim([0,height])
            

            
            m=0
            x_labs=[]
            gap=5*int(width/(4*5))
            while m<width-gap:
                m=m+gap
                x_labs.append(m)

                
            m=0
            y_labs=[]
            gap=2*int(height/(4*2))
            while m<height-gap:
                m=m+gap
                y_labs.append(m)
                
            if p>6:
                ax.set_xlabel(interaction_type.replace('_',' '),size=20)
                ax.set_xticks(x_labs)
            else:
                ax.set_xticks([])
            if (p-1) % 3==0:
                ax.set_yticks(y_labs)
            else:
                ax.set_yticks([])
            if p==4:
                ax.set_ylabel('Number of ants',size=20)  
            ax.tick_params(labelsize=20)
            
plt.figtext(0.91,0.8,'Colony 1',rotation=90,fontsize=20)
plt.figtext(0.91,0.55,'Colony 2',rotation=90,fontsize=20)
plt.figtext(0.91,0.3,'Colony 3',rotation=90,fontsize=20)

fig.subplots_adjust(hspace=0,wspace=0)       


plt.savefig('../Results/Frequency_distributions.pdf', format='pdf',bbox_inches='tight',dpi=512) 