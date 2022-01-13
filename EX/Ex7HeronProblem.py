from pyomo.environ import *
import numpy as np
# heron problem


model = ConcreteModel()
model.L=Param(initialize=10)
model.h1=Param(initialize=2)
model.h2=Param(initialize=4)
model.d1=Var(bounds=(0,model.L), initialize=0)
model.d2=Var(bounds=(0,model.L), initialize=0)
model.x=Var(bounds=(0,model.L), initialize=0)
model.C1=Constraint(expr=  model.d1**2==model.h1**2+model.x**2)
model.C2=Constraint(expr=  model.d2**2==model.h2**2+(model.L-model.x)**2)
model.f1=Objective(expr=model.d1+model.d2,sense=minimize )


solver = SolverFactory('ipopt')
results=solver.solve(model);


print('d1=' , round(value(model.d1),2))
print('d2=' ,round(value(model.d2),2))
print('x=' ,round(value(model.x),2))
print('f1=' ,round(value(model.f1),2))
