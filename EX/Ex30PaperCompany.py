from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 


model = ConcreteModel()
model.N =Param(mutable=True, initialize=15) 
model.i = RangeSet(1,model.N)

model.U = Var(model.i, within=Binary, initialize=0)
model.x = Var(model.i, bounds=(0,4), domain=NonNegativeIntegers,initialize=0)
model.y = Var(model.i, bounds=(0,2), domain=NonNegativeIntegers,initialize=0)
model.z = Var(model.i, bounds=(0,2), domain=NonNegativeIntegers,initialize=0)
model.OF = Var(within=Reals, initialize=0)

def rule_C1(model,i):
        return 5*model.x[i]+7*model.y[i]+9*model.z[i] <=20*model.U[i]
model.C1   = Constraint(model.i,rule=rule_C1)

def rule_C2(model,i):
        return sum(model.x[i] for i in model.i)==10
model.C2   = Constraint(model.i,rule=rule_C2)

def rule_C3(model,i):
        return sum(model.y[i] for i in model.i)==12
model.C3   = Constraint(model.i,rule=rule_C3)
def rule_C4(model,i):
        return sum(model.z[i] for i in model.i)==5
model.C4   = Constraint(model.i,rule=rule_C4)
def rule_OF(model,i):
    return model.OF==sum(model.U[i] for i in model.i)
model.C5   = Constraint(rule=rule_OF)
model.obj1 = Objective(expr=model.OF, sense=minimize)


opt = SolverFactory('glpk')
results=opt.solve(model)
print('OF= ',value(model.OF))
#model.display()


print('   U   x  y   z ')
for i in model.i:
    if value(model.U[i])==1:
        print(i,value(model.U[i]),value(model.x[i]),value(model.y[i]),value(model.z[i]) )
        
        
model.C5.pprint()
