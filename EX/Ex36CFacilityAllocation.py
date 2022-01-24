import matplotlib.pyplot as plt
import networkx as nx
G=nx.random_regular_graph(3, 20, seed=None)
pos=nx.spring_layout(G)
l1=nx.draw(G, pos=pos,with_labels=True)
#labels = nx.draw_networkx_labels(G, pos=pos,font_color='white',font_weight='bold'  )
plt.show()


from pyomo.environ import *
import numpy as np
import random 
import pandas as pd


model = AbstractModel()
model.N=Param(mutable=True,initialize=len(G.nodes))
model.i = RangeSet(0,model.N-1)
model.j = Set(initialize=model.i)
model.L = Param(model.i,model.j, default=0,mutable=True)
model.X = Var(model.i, domain=Binary)
model.y = Var(within=NonNegativeReals, initialize=0)
def rule_C1(model,i):
        return model.X[i]+ sum(model.X[j] for j in model.j if value(model.L[i,j])==1)>=1
model.C1 = Constraint(model.i, rule=rule_C1)
def rule_C2(model):
    return model.y>=sum(model.X[i] for i in model.i)
model.C2 = Constraint(rule=rule_C2)
model.OF=Objective(expr=model.y, sense=minimize)


Lines={edg:1 for edg in G.edges}
data = {None: {
    'N': {None: len(G.nodes)},       
    'L': Lines,}}
instance = model.create_instance(data)


opt = SolverFactory('glpk')
results = opt.solve(instance) # solves and updates instance


print(value(instance.y))
for i in instance.i:
    if value(instance.X[i])>0:
        print(i,value(instance.X[i]))
        
        
print ("The solver returned a status of:"+str(results.solver.status))
from pyomo.opt import SolverStatus, TerminationCondition
if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
     print ("this is feasible and optimal")
elif results.solver.termination_condition == TerminationCondition.infeasible:
     print ("do something about it? or exit?")
else:
     print (str(results.solver))
    
    
#instance.C1.pprint()


cvec=[]
for i in G.nodes:
    cvec.append(value(instance.X[i]))
l1=nx.draw(G, pos=pos,node_color=cvec,with_labels=True)
labels = nx.draw_networkx_labels(G, pos=pos, font_color='white' ,font_weight='bold' )
plt.show()


