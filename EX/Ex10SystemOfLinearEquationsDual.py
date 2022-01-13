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


model.dual = Suffix(direction=Suffix.IMPORT)


opt = SolverFactory('glpk')
instance = model.create_instance("Ex10.dat")
results = opt.solve(instance) 


for m in instance.M:
    print(instance.dual[instance.con[m]])
