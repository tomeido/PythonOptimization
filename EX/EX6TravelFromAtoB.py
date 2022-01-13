from pyomo.environ import *
import numpy as np
# max f1 = 2rcos(theta)/V1+r2theta/V2 <br>
# 0<theta<pi/2 
#find the min time to travel from A to B


model = ConcreteModel()
model.r=Param(initialize=10)
model.V1=Param(initialize=4)
model.V2=Param(initialize=3)
model.theta=Var(bounds=(0,np.pi/2), initialize=np.pi/3)
model.OF=Objective(expr=2*model.r*cos(model.theta)/model.V1+ 2*model.theta*model.r/model.V2,sense=minimize )


solver = SolverFactory('ipopt')
results=solver.solve(model);


print('therta= ',round(value(model.theta)*180/np.pi))
print('OF= ',round(value(model.OF),2))
