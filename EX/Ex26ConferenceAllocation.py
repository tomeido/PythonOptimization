from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np
import random 


model = AbstractModel()
model.N =Param(mutable=True) 
model.Nc =Param(mutable=True) 

model.i = RangeSet(1,model.N)
model.j = Set(initialize=model.i)

model.U = Var(model.i,within=Binary)
model.link = Var(model.i,model.j,within=Binary)

model.OF = Var(within=NonNegativeReals, initialize=5)
def initval(model,i):
    return random.uniform(0,1)
model.Xloc=Param(model.i,  within=NonNegativeReals, initialize=initval,mutable=True)
model.Yloc=Param(model.i,  within=NonNegativeReals, initialize=initval, mutable=True)


def Ncenters_rule(model):
    return sum(model.U[i] for i in model.i)==model.Nc
model.eq1=Constraint(rule=Ncenters_rule)

def eq2_rule(model,i):
    return sum(model.link[i,j] if i!=j else 0 for j in model.j)==1
model.eq2=Constraint(model.i,rule=eq2_rule)

def eq3_rule(model,i,j):
    if i!=j:
        return model.link[i,j] <= model.U[j]+model.U[i]
    else:
        return Constraint.Skip
model.eq3=Constraint(model.i,model.j,rule=eq3_rule)

def rule_OF(model):
    return model.OF==sum(model.link[i,j]*((model.Xloc[i]-model.Xloc[j])**2+(model.Yloc[i]-model.Yloc[j])**2) if i!=j else 0 for i in model.i for j in model.j)
model.C   = Constraint(rule=rule_OF)

model.obj1 = Objective(expr=model.OF, sense=minimize)
opt = SolverFactory('glpk')
#instance.display()


model.N=20
model.Nc=3


#instance = model.create_instance("/Users/alirezasoroudi/Dropbox/pythonfiles save/ex16data.dat")
instance = model.create_instance()
results = opt.solve(instance) # solves and updates instance
print('OF= ',value(instance.obj1))


fig = plt.figure(figsize=(7,7))
Xc=np.linspace(0,1,100);
for i in instance.i:
    plt.scatter(value(instance.Xloc[i]),value(instance.Yloc[i]),label=str(i)) 
    plt.text(value(instance.Xloc[i]),0.01+value(instance.Yloc[i]),str(i))
    if value(instance.U[i])>=0.99:
        plt.scatter(value(instance.Xloc[i]),value(instance.Yloc[i]),color='black', s=100) 

for i in instance.i:
    for j in instance.j:
        if i!=j:
            if value(instance.link[i,j])>0.99:
               # print(i,j)
                startP=[value(instance.Xloc[i]),value(instance.Xloc[j])]
                endP=[value(instance.Yloc[i]),value(instance.Yloc[j])]
                plt.plot(startP,endP,lw=0.5) 
#plt.legend()
#plt.xlim(0,1)
#plt.ylim(0,1)


fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(12,12))
Ncvec=[2,4,6,8]

for counter in range(0,len(Ncvec)):
    plt.subplot(2, 2, counter+1)
    instance.Nc=Ncvec[counter]
    results = opt.solve(instance) # solves and updates instance
    OF=round(value(instance.obj1),3)
    plt.title('N= '+str(value(instance.N)) +',  $N_c=$' + str(Ncvec[counter])+ ' OF= '+ str(OF))
    print('OF= ',value(instance.obj1))

    for i in instance.i:
        plt.scatter(value(instance.Xloc[i]),value(instance.Yloc[i]),label=str(i)) 
        plt.text(value(instance.Xloc[i]),0.01+value(instance.Yloc[i]),str(i))
        if value(instance.U[i])>=0.99:
            plt.scatter(value(instance.Xloc[i]),value(instance.Yloc[i]),color='black', s=50) 

    for i in instance.i:
        for j in instance.j:
            if i!=j:
                if value(instance.link[i,j])>0.99:
                    startP=[value(instance.Xloc[i]),value(instance.Xloc[j])]
                    endP=[value(instance.Yloc[i]),value(instance.Yloc[j])]
                    plt.plot(startP,endP,lw=0.5) 
                    
                    
instance.eq2.pprint()
