from pyomo.environ import *
import matplotlib.pyplot as plt
import random 


model = AbstractModel()
model.N = Param(mutable=True)
model.i = RangeSet(1, model.N)
model.j = Set(initialize=model.i)
model.L=Param(initialize=1,mutable=True)
def initval(model,i):
    return random.uniform(0,1)

model.x = Var(model.i , bounds=(0,model.L), within=NonNegativeReals, initialize=initval)
model.y = Var(model.i ,bounds=(0,model.L) , within=NonNegativeReals, initialize=initval)
model.r = Var(within=NonNegativeReals)
def C1_rule(model,i,j):
    if i!=j:
        return (model.x[i]-model.x[j])**2+(model.y[i]-model.y[j])**2 >=model.r**2
    else:
        return Constraint.Skip
model.C   = Constraint(model.i,model.j, rule=C1_rule)
model.obj = Objective(expr=model.r, sense=maximize)
opt = SolverFactory('ipopt')



#instance = model.create_instance("EX11.dat")
model.N=100
instance = model.create_instance()
results = opt.solve(instance) # solves and updates instance


X=[value(instance.x[i]) for i in instance.i]
Y=[value(instance.y[i]) for i in instance.i]
plt.scatter( X,Y,s=25,color='blue')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Hostile brothers for N='+str(value(instance.N)))
print('Min distance is ',round(value(instance.r),3))
