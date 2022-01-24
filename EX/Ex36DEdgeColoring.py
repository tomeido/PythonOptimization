import matplotlib.pyplot as plt
import networkx as nx
G=nx.random_regular_graph(4, 30, seed=None)
pos=nx.spring_layout(G)
nx.draw(G, node_color='black',font_color='white',font_weight='bold',width=1,pos=pos,with_labels=True)


from pyomo.environ import *
import numpy as np
import random 
import pandas as pd


model = AbstractModel()
model.N=Param(mutable=True,initialize=len(G.nodes))
model.E=Param(mutable=True,initialize=len(G.edges))
model.i = RangeSet(0,model.N-1)
model.j = Set(initialize=model.i)
model.L = Param(model.i,model.j, default=0,mutable=True)
model.kolor=RangeSet(1,model.E/4)
model.X = Var(model.i,model.j,model.kolor, initialize=0, domain=Binary)
model.y = Var(within=NonNegativeReals, initialize=0)
                                                     
def rule_C1(model,i,c):
    exi=0
    for j in model.j:
        if value(model.L[i,j])==1:
            exi+=model.X[i,j,c]
        if value(model.L[j,i])==1:
            exi+=model.X[j,i,c]    
    return exi <=1
model.C1 = Constraint(model.i,model.kolor,rule=rule_C1)

def rule_C2(model):
    return model.y>=sum(c*model.X[i,j,c] for c in model.kolor for i in model.i for j in model.j  if (value(model.L[i,j])==1)) 
model.C2 = Constraint(rule=rule_C2)

def rule_C3(model,i,j):
    if value(model.L[i,j])==1:
        return sum(model.X[i,j,c] for c in model.kolor)==1
    else:
        return Constraint.Skip
model.C3 = Constraint(model.i,model.j,rule=rule_C3)
model.OF=Objective(expr=model.y, sense=minimize)
opt = SolverFactory('glpk')
opt.options["mipgap"] = 0


Lines={edg:1 for edg in G.edges}
data = {None: {
    'N': {None: len(G.nodes)},       
    'L': Lines,}}
instance = model.create_instance(data)


results = opt.solve(instance) # solves and updates instance


print('OF= ', value(instance.y))
for i in instance.i:
    for j in instance.j:
        for c in instance.kolor:
            if value(instance.X[i,j,c])>0:
                print((i,j,c),value(instance.X[i,j,c]))
                
                
print ("The solver returned a status of:"+str(results.solver.status))
from pyomo.opt import SolverStatus, TerminationCondition
if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
     print ("this is feasible and optimal")
elif results.solver.termination_condition == TerminationCondition.infeasible:
     print ("do something about it? or exit?")
else:
     print (str(results.solver))
    
    
#instance.C1.pprint()
instance.C2.pprint()
#instance.C3.pprint()
instance.display()
for i in instance.i:
    for j in instance.j:
        if value(instance.L[i,j]) >0:
            print((i,j),value(instance.L[i,j]))
            
            
cvec=[]
edgelist=[edg for edg in G.edges ]
for (i,j) in edgelist:
    for c in instance.kolor:
        if value(instance.X[i,j,c])>0:
            cvec.append(c)
l1=nx.draw(G,node_color='black',font_color='white',font_weight='bold',pos=pos, width=3, edge_color=cvec,with_labels=True)


