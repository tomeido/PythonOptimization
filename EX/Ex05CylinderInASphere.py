from pyomo.environ import *
import numpy as np
# max f1 = 2*pi*r^2*h 
# h^2+r^2 =R^2 
# 0<h<R
# 0<r<R
# find the maximum volume of a cylinder in a sphere 


model = ConcreteModel()
model.R=Param(initialize=1)
model.h=Var(bounds=(0,model.R), initialize=model.R)
model.r=Var(bounds=(0,model.R), initialize=model.R)
model.C=Constraint(expr=model.r**2+model.h**2==model.R**2)
model.OF=Objective(expr=2*np.pi*(model.r**2)*model.h,sense=maximize)


solver = SolverFactory('ipopt')
results=solver.solve(model);


print('r=' ,round(value(model.r),2))
print('h=' ,round(value(model.h),2))
print('OF=',round(value(model.OF),2))


print('r=' ,value(model.r))


