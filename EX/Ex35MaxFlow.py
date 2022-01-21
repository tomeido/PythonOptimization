from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 


model = AbstractModel()

model.i = Set(initialize=range(0,7))
model.j = Set(initialize=model.i)
model.flow = Var(model.i,model.j,bounds=(0,100), within=NonNegativeReals)
model.cap = Param(model.i,model.j, within=Reals, mutable=True)
model.G = Var(bounds=(0,100), within=NonNegativeReals, initialize=0)

def rule_C1(model,i):
    if   i==0:
        return model.G        ==sum(model.flow[i,j]-model.flow[j,i] if i!=j else 0 for j in model.j)
    elif i==6:
        return        -model.G==sum(model.flow[i,j]-model.flow[j,i] if i!=j else 0 for j in model.j)
    else: 
        return        0       ==sum(model.flow[i,j]-model.flow[j,i] if i!=j else 0 for j in model.j)
model.C1   = Constraint(model.i,rule=rule_C1)

def rule_C2(model,i,j):
    if i!=j:
        return model.flow[i,j]<= model.cap[i,j]
    else:
        return Constraint.Skip
model.C2   = Constraint(model.i,model.j,rule=rule_C2)

model.obj1 = Objective(expr=model.G, sense=maximize)
opt = SolverFactory('glpk')


instance = model.create_instance("EX35.dat")
results = opt.solve(instance) # solves and updates instance
print('OF= ',value(instance.obj1))




    plt.text(data[str(i)][0],data[str(i)][1]-0.2,str(i),fontsize=14)
    
    for j in instance.j:
        if (i!=j):
            if value(instance.flow[i,j]>0.001):
                plt.plot([data[str(i)][0],data[str(j)][0]],[data[str(i)][1],data[str(j)][1]],lw=value(instance.flow[i,j]),color='blue',alpha=0.5)
     
plt.axis('off')


instance.display()
