import random
import numpy as np
import itertools
import math
xor="0110"
class Percept:
    def __init__(self,vector,threshold): 
        self.w=np.array(vector)
        self.t=threshold
    def set_inputs(self,arr):
        self.inputs=arr
    def evaluate(self):
        newArr=[]
        for i in self.inputs:
            newArr.append(i.evaluate())
        #print(newArr)
        x=np.dot(np.array(newArr),self.w)
        if x>=self.t:
            return 1
        else:
            return 0

class Input(Percept):
    def __init__(self):   
        self.value=0
    def set_value(self,v):
        self.value=v
    def evaluate(self):
        return self.value

def pyth(a,b):
    if (math.pow(a,2) + math.pow(b,2))<=1:
        return 1
    else:
        return 0


x1 = Input()
x2 = Input()
node_1=Percept([-1,0],-1) #101 but want it to be less than so -10-1
node_1.set_inputs([x1,x2]) 
node_2=Percept([1,0],-1) 
node_2.set_inputs([x1,x2]) 
node_3=Percept([0,-1],-1)
node_3.set_inputs([x1,x2]) 
node_4=Percept([0,1],-1)
node_4.set_inputs([x1,x2]) 
node_5=Percept([1,-1],-1*math.sqrt(2))
node_5.set_inputs([x1,x2]) 
node_6=Percept([-1,1],-1*math.sqrt(2))
node_6.set_inputs([x1,x2]) 
node_7=Percept([-1,-1],-1*math.sqrt(2))
node_7.set_inputs([x1,x2]) 
node_8=Percept([1,1],-1*math.sqrt(2))
node_8.set_inputs([x1,x2]) 
node_AND1=Percept([1,1],1.5)
node_AND1.set_inputs([node_1,node_2])
node_AND2=Percept([1,1],1.5)
node_AND2.set_inputs([node_3,node_4])
node_AND3=Percept([1,1],1.5)
node_AND3.set_inputs([node_5,node_6])
node_AND4=Percept([1,1],1.5)
node_AND4.set_inputs([node_7,node_8])
node_AND5=Percept([1,1],1.5)
node_AND5.set_inputs([node_AND1,node_AND2])
node_AND5=Percept([1,1],1.5)
node_AND5.set_inputs([node_AND1,node_AND2])
node_AND6=Percept([1,1],1.5)
node_AND6.set_inputs([node_AND3,node_AND4])
node_AND6=Percept([1,1],1.5)
node_AND6.set_inputs([node_AND3,node_AND4])
node_AND7=Percept([1,1],1.5)
node_AND7.set_inputs([node_AND5,node_AND6])
AND=node_AND7
accuracy=0
for i in range(10000):
    xcoord=random.uniform(-1.5,1.5)
    ycoord=random.uniform(-1.5,1.5)
    #print(str(xcoord)+ " " + str(ycoord))
    x1.set_value(xcoord)
    x2.set_value(ycoord)
    #print("in circle"+ str(AND.evaluate()))
    #print("actual circle" + str(pyth(xcoord,ycoord)))
    if AND.evaluate()==pyth(xcoord,ycoord):
        accuracy=accuracy+1
print(accuracy)
    
    


    
