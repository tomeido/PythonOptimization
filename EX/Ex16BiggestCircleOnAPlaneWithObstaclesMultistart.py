from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 
#sasa


model = AbstractModel()
model.N =Param(mutable=True) 
model.i = RangeSet(1,model.N)
def initval(model,i):
    return random.uniform(0,1)
model.Xloc=Param(model.i,  within=NonNegativeReals, initialize=initval,mutable=True)
model.Yloc=Param(model.i,  within=NonNegativeReals, initialize=initval, mutable=True)
model.x = Var(bounds=(0,1), within=NonNegativeReals, initialize=random.uniform(0,1))
model.y = Var(bounds=(0,1), within=NonNegativeReals, initialize=random.uniform(0,1))
model.r = Var(bounds=(0,1), within=NonNegativeReals, initialize=random.uniform(0,1))
model.area = Var(bounds=(0,1), within=NonNegativeReals, initialize=0)

def rule_C2(model,i):
    return (model.x-model.Xloc[i])**2+(model.y-model.Yloc[i])**2>=model.r**2
model.C2   = Constraint(model.i,rule=rule_C2)

def rule_C3(model):
    return model.x>=model.r
model.C3   = Constraint(rule=rule_C3)

def rule_C4(model):
    return model.y>=model.r
model.C4   = Constraint(rule=rule_C4)

def rule_C5(model):
    return model.y<=1-model.r
model.C5   = Constraint(rule=rule_C5)

def rule_C6(model):
    return model.x<=1-model.r
model.C6   = Constraint(rule=rule_C6)

def rule_obj(model):
    return model.area==np.pi*model.r**2 
model.C7   = Constraint(rule=rule_obj)

model.obj1 = Objective(expr=model.area , sense=maximize)
opt = SolverFactory('ipopt')


model.N=10
instance = model.create_instance()


fig = plt.figure(figsize=(6,6))
for i in instance.i:
    plt.scatter(value(instance.Xloc[i]),value(instance.Yloc[i]),s=50)
    
#results = opt.solve(instance) # solves and updates instance
results =SolverFactory('multistart').solve(instance)  

print('r=  ','%5.4f'% value(instance.r))
print('x=  ','%5.4f'% value(instance.x))
print('y=  ','%5.4f'% value(instance.y))

theta=np.linspace(0,2*np.pi,100)
Xc=value(instance.x)+value(instance.r)*np.cos(theta)
Yc=value(instance.y)+value(instance.r)*np.sin(theta)
plt.plot(Xc,Yc,'--',lw=3)
plt.scatter(value(instance.x),value(instance.y),color='black',s=50)
plt.xlabel('X')
plt.ylabel('Y')
plt.xlim(0,1)
plt.ylim(0,1)
plt.show()
