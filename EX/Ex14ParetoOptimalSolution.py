from pyomo.environ import *
import matplotlib.pyplot as plt


model = ConcreteModel()
model.epsilon=Param(initialize=-100,mutable=True)
model.x1 = Var(bounds=(1,2), within=NonNegativeReals)
model.x2 = Var(bounds=(1,3), within=NonNegativeReals)
model.eq1= Constraint(expr= -1.2*model.x1**2+5*model.x2>=model.epsilon)
model.obj1 = Objective(expr=2*model.x1-0.5*model.x2**2, sense=maximize)
model.obj2 = Objective(expr=-1.2*model.x1**2+5*model.x2, sense=maximize)
opt = SolverFactory('ipopt')


model.obj2.deactivate() 
results = opt.solve(model) # solves and updates instance
print('x1 = ',round(value(model.x1),2))
print('x2 = ',round(value(model.x2),2))
print('obj1 = ',round(value(model.obj1),2))
print('obj2 = ',round(value(model.obj2),2))
maxOF1=value(model.obj1)
minOF2=value(model.obj2)


model.obj1.deactivate() 
model.obj2.activate() 
results = opt.solve(model) # solves and updates instance
print('x1 = ',round(value(model.x1),2))
print('x2 = ',round(value(model.x2),2))
print('obj1 = ',round(value(model.obj1),2))
print('obj2 = ',round(value(model.obj2),2))
minOF1=value(model.obj1)
maxOF2=value(model.obj2)


model.obj1.activate() 
model.obj2.deactivate() 
Nsteps=21
X=[]
Y=[]
print('  x1  ',' x2 ',' OF1 ',' OF2 ',' Epsilon ')
for counter in range(1,Nsteps+1):
    model.epsilon=minOF2+(maxOF2-minOF2)*(counter-1)/(Nsteps-1)
    results = opt.solve(model) # solves and updates instance
    print("%5.2f"% value(model.x1),"%5.2f"% value(model.x2),"%5.2f"% value(model.obj1),"%5.2f"% value(model.obj2), "%5.2f"% value(model.epsilon))
    X.append(value(model.obj1))
    Y.append(value(model.obj2))
    
    
fig = plt.figure(figsize=(6,6))
plt.scatter(X,Y)
plt.xlabel('OF1',fontweight='bold')
plt.ylabel('OF2',fontweight='bold')
plt.grid()
plt.show()


