from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 


model = AbstractModel()
model.i = Set()
model.j = Set()
model.Demand =Param(model.j) 
model.pmin = Param(model.i)
model.pmax = Param(model.i)
model.Cost = Param(model.i)

model.distance = Param(model.i,model.j, within=Reals)

model.x = Var(model.i,model.j, bounds=(0,300), within=Reals)
model.OF = Var(within=Reals)

def Pbounds(model,i):
    return (model.pmin[i] , model.pmax[i])
model.P = Var(model.i, bounds=Pbounds, domain=Reals)

def rule_C1(model,i):
        return  sum(model.x[i,j] for j in model.j)==model.P[i]
model.C1   = Constraint(model.i,rule=rule_C1)

def rule_C2(model,j):
        return  sum(model.x[i,j] for i in model.i)>=model.Demand[j]
model.C2   = Constraint(model.j,rule=rule_C2)
def rule_OF(model):
    return model.OF==sum(model.P[i]*model.Cost[i] for i in model.i) + sum(model.x[i,j]*model.distance[i,j] for i in model.i for j in model.j)
model.C3   = Constraint(rule=rule_OF)
model.obj1 = Objective(expr=model.OF, sense=minimize)



opt = SolverFactory('glpk')
instance = model.create_instance("Ex31.dat")
results = opt.solve(instance) # solves and updates instance
print('OF= ',value(instance.OF))



for i in instance.i:
    print(value(instance.P[i]),value(instance.pmin[i]),value(instance.pmax[i]))
    for j in instance.j:
        print((i,j),value(instance.x[i,j]))
        
        
fig = plt.figure(figsize=(7,7))
Ni=3
Nj=4
supplyY=np.linspace(0.1,0.9,Ni)
supplyX=0.1*np.ones_like(supplyY)
demandY=np.linspace(0.1,0.9,Nj)
demandX=0.9*np.ones_like(demandY)

for i in instance.i:
    for j in instance.j:
        if value(instance.x[i,j])>0.1:
            plt.plot([supplyX[Ni-i],demandX[Nj-j]],[supplyY[Ni-i],demandY[Nj-j]],lw=value(instance.x[i,j])/30)
for c in range(0,Ni):
    plt.scatter(supplyX[c],supplyY[c],s=250)
    plt.text(supplyX[Ni-c-1]-0.05,supplyY[Ni-c-1],'S'+str(c+1),fontweight='bold')
for c in range(0,Nj):
    plt.scatter(demandX[c],demandY[c],s=250)
    plt.text(demandX[Nj-c-1]+0.03,demandY[Nj-c-1],'D'+str(c+1),fontweight='bold')
plt.axis('off')



