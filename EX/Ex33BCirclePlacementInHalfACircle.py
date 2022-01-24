from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np


model = AbstractModel()
model.i = Set()
model.j = Set(initialize=model.i)
model.R = Param(model.i)
def lowband(model,i):
    return (model.R[i],15)
model.x = Var(model.i, bounds=(0,15), within=NonNegativeReals, initialize=3)
model.y = Var(model.i, bounds=lowband, within=NonNegativeReals, initialize=5)
model.Radius = Var( bounds=(0,100), within=NonNegativeReals, initialize=6)
def rule_eq1(model,i,j):
    if i<j:
        return (model.x[i]-model.x[j])**2+(model.y[i]-model.y[j])**2 >=(model.R[i]+model.R[j])**2
    else:
        return Constraint.Skip;
model.eq1 = Constraint(model.i,model.j,rule=rule_eq1)
def rule_eq2(model,i):
    return (model.x[i]-model.Radius)**2 +(model.y[i]-0)**2<=(model.Radius-model.R[i])**2
model.eq2 = Constraint(model.i,rule=rule_eq2)
model.obj = Objective(expr=model.Radius, sense=minimize)


opt = SolverFactory('Ipopt')
instance = model.create_instance("EX33B.dat")
results = opt.solve(instance) 


fig = plt.figure(figsize=(6,6))
theta0=np.linspace(0,np.pi,100)
theta=np.linspace(0,2*np.pi,100)
for i in instance.i:
    plt.scatter( value(instance.x[i]),value(instance.y[i]),label=str(i),s=30)
    Xc=value(instance.x[i])+value(instance.R[i])*np.cos(theta)
    Yc=value(instance.y[i])+value(instance.R[i])*np.sin(theta)
    plt.plot(Xc,Yc)

Xc=value(instance.Radius)+value(instance.Radius)*np.cos(theta0)
Yc=+value(instance.Radius)*np.sin(theta0)
plt.plot(Xc,Yc)
plt.scatter( value(instance.Radius),0,color='black',label='Centre',s=30)
plt.title('Radius= ' + str("%5.2f"% value(instance.Radius)))
plt.legend(loc='right')
#plt.axis('off')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()


