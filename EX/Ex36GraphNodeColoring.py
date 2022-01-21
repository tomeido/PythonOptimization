import matplotlib.pyplot as plt
import networkx as nx
G = nx.grid_2d_graph(5,5) 
pos = nx.spring_layout(G, iterations=100)


from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 
import pandas as pd


model = AbstractModel()
model.N=Param(mutable=True)
model.i = RangeSet(1,model.N)
model.j = Set(initialize=model.i)
model.kolor=RangeSet(1,model.N)
model.L = Param(model.i,model.j, initialize=0,mutable=True)
model.X = Var(model.i,model.kolor, domain=Binary)
model.y = Var(within=NonNegativeReals)

def rule_C1(model,i,j,c):
    return model.L[i,j]*(model.X[i,c]+ model.X[j,c])<=1
model.C1 = Constraint(model.i, model.j, model.kolor, rule=rule_C1)

def rule_C2(model,i,c):
    return model.y>=c*model.X[i,c]
model.C2 = Constraint(model.i, model.kolor, rule=rule_C2)

def rule_C3(model,i):
    return sum(model.X[i,c] for c in model.kolor)==1
model.C3 = Constraint(model.i, rule=rule_C3)
model.OF=Objective(expr=model.y, sense=minimize)



opt = SolverFactory('glpk')
model.N=len(G.nodes)
#instance = model.create_instance('Ex36.dat')
instance = model.create_instance()



counter=1
edges=[]
coordinates=[]
nodes=[]
xvec=[]
yvec=[]
for nd in G.nodes:
    print(nd)
    nodes.append(counter)
    coordinates.append(nd)
    xvec.append(nd[0])
    yvec.append(nd[1])
    counter+=1
    
mygraph = {'nodes': nodes,
          'xy': coordinates,
           'x': xvec,
           'y': yvec}
df = pd.DataFrame(mygraph, columns = ['nodes', 'xy','x','y'])
    
for i in instance.i:
    for j in instance.j:
        instance.L[i,j]=0

for edg in G.edges:
    fn=edg[0]
    tn=edg[1]
    ind1=(df['x'] == fn[0]) & (df['y'] == fn[1])
    f=df.loc[ind1,'nodes']
    ind2=(df['x'] == tn[0]) & (df['y'] == tn[1])
    t=df.loc[ind2,'nodes']
    i=f.iloc[0]
    j=t.iloc[0]
    instance.L[i,j]=1
    instance.L[j,i]=1
    
    
results = opt.solve(instance) 
for i in instance.i:
    for j in instance.j:
        if value(instance.L[i,j])>0:
            print((i,j),value(instance.L[i,j]))
