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
        x=np.dot(np.array(newArr),self.w)
        if x>self.t:
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

with open("weights.txt") as f:
    content=f.read().splitlines()
arr=[]
for s in content:
    arr.append(s.split(", "))
#print(arr)
x1 = Input()
x2 = Input()
for a in arr:
    if arr.index(a)!=6 and arr.index(a)!=9:
        node_3 = Percept([float(a[0]),float(a[1])],float(a[2])*-1)
        node_3.set_inputs([x1,x2]) 
        for b in arr:
            if arr.index(b)!=6 and arr.index(b)!=9:            
                node_4 = Percept([float(b[0]),float(b[1])],float(b[2])*-1)
                node_4.set_inputs([x1,x2])
                for c in arr:
                    if arr.index(c)!=6 and arr.index(c)!=9:                    
                        node_5 = Percept([float(c[0]),float(c[1])],float(c[2])*-1)
                        node_5.set_inputs([node_3, node_4])
                        xor = node_5
                        soln=[]
                        s=""
                        for i in range(2):
                            for j in range(2):
                                x1.set_value(i) 
                                x2.set_value(j)
                                soln.append([i,j,xor.evaluate()])
                        for l in soln:
                            s=s+str(l[len(l)-1])
                        if s=="0110":
                            print(str(arr.index(a))+ " " + str(arr.index(b))+ " " + str(arr.index(c)))

    
