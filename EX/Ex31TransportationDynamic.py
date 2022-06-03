from pyomo.environ import *
import numpy as np


model = AbstractModel()
model.i = Set()
model.j = Set()
model.t = Set()
model.Demand   = Param(model.j) 
model.pmin     = Param(model.i)
model.pmax     = Param(model.i)
model.Cost     = Param(model.i)
model.pattern  = Param(model.t)
model.distance = Param(model.i,model.j, within=Reals)
model.x = Var(model.t,model.i,model.j, bounds=(0,300), within=Reals)
model.OF = Var(within=Reals)

def Pbounds(model,t,i):
    return (model.pmin[i] , model.pmax[i])
model.P = Var(model.t,model.i, bounds=Pbounds, domain=Reals)

def rule_C1(model,t,i):
        return  sum(model.x[t,i,j] for j in model.j)==model.P[t,i]
model.C1   = Constraint(model.t,model.i,rule=rule_C1)

def rule_C2(model,t,j):
        return  sum(model.x[t,i,j] for i in model.i)>=model.Demand[j]*model.pattern[t]
model.C2   = Constraint(model.t,model.j,rule=rule_C2)

def rule_OF(model):
    return model.OF==sum(model.P[t,i]*model.Cost[i] for i in model.i for t in model.t) + sum(model.x[t,i,j]*model.distance[i,j] for i in model.i for j in model.j for t in model.t)
model.C3   = Constraint(rule=rule_OF)
model.obj1 = Objective(expr=model.OF, sense=minimize)


opt = SolverFactory('glpk')
instance = model.create_instance("Ex31-dynamic.dat")
results = opt.solve(instance) # solves and updates instance
print('OF= ',value(instance.OF))


for t in instance.t:
    for i in instance.i:
        print('t=',t,value(instance.P[t,i]),value(instance.pmin[i]),value(instance.pmax[i]))
for t in instance.t:
    for i in instance.i:
        for j in instance.j:
            print((t,i,j),value(instance.x[t,i,j]))
            
            
            
