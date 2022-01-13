from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 
# Steiner problem


model = ConcreteModel()
model.b=Param(initialize=4,mutable=True)
model.a=Param(initialize=6,mutable=True)
model.x=Var(bounds=(0,model.a), initialize=0.1)
model.y=Var(bounds=(0,model.b), initialize=0.1)
model.f1=Objective(expr= sqrt((model.x-0)**2+(model.y-0)**2)+ sqrt((model.x-0)**2+(model.y-model.b)**2)+sqrt((model.x-model.a)**2+(model.y-0)**2) ,sense=minimize )


solver = SolverFactory('ipopt')
results=solver.solve(model);


print('X=  ' , round(value(model.x),2))
print('Y=  ' ,round(value(model.y),2))
print('OF= ' ,round(value(model.f1),2))


x=[0, value(model.a), 0]
y=[0, 0, value(model.b)]
plt.scatter(x,y)
plt.scatter( value(model.x), value(model.y),s=55)
print(value(model.a),value(model.b))
