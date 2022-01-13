from pyomo.environ import *
import numpy as np


model = AbstractModel()
model.N = Set()
model.M = Set()
model.c = Param(model.N)
model.a = Param(model.M, model.N)
model.b = Param(model.M)
model.x = Var(model.N, within=NonNegativeReals)
def con_rule(model, m):
    return sum(model.a[m,i]*model.x[i] for i in model.N) >= model.b[m]
model.con = Constraint(model.M, rule=con_rule)

def obj_rule(model):
    return sum(model.c[i]*model.x[i] for i in model.N)
model.OF = Objective(rule=obj_rule,sense=minimize)


opt = SolverFactory('glpk')
instance = model.create_instance("Ex10.dat")
results = opt.solve(instance) # solves and updates instance


for i in instance.N:
    print('X'+str(i)+'= ',round(value(instance.x[i]),2))
print('OF=',round(value(instance.OF),2))
