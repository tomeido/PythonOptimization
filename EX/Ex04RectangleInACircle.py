from pyomo.environ import *
# max f1 = 4XY <br>
# st  X^2+Y^2=R^2
# 0<X,Y<R
#find the maximum area of a rectangle in a circle 



model = ConcreteModel()
model.R=Param(initialize=10)
model.x=Var(bounds=(0,model.R), initialize=model.R)
model.y=Var(bounds=(0,model.R), initialize=model.R)
model.C1=Constraint(expr=model.x**2+model.y**2==model.R**2)
model.f1=Objective(expr=4*model.x*model.y,sense=maximize)



solver = SolverFactory('ipopt')
results=solver.solve(model);



print('x= ',round(value(model.x),3))
print('y= ',round(value(model.y),3))
print('OF= ',round(value(model.f1),3) )



model.x.fix(1)
results=solver.solve(model);



print('x= ',round(value(model.x),3))
print('y= ',round(value(model.y),3))
print('OF= ',round(value(model.f1),3) )



model.x.unfix()
model.y.fix(1)
results=solver.solve(model);



print('x= ',round(value(model.x),3))
print('y= ',round(value(model.y),3))
print('OF= ',round(value(model.f1),3) )



model.x.unfix()
model.y.unfix()
results=solver.solve(model);



print(results)
