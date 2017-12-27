import random
import numpy as np
import math
k=3
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
        return (1/(1+math.exp(-k*(x-self.t))))


class Input(Percept):
    def __init__(self):   
        self.value=0
    def set_value(self,v):
        self.value=v
    def evaluate(self):
        return self.value

    





def err(w):
    acc=0
    i=0
    arr=[0,1,1,0]
    x1=Input()
    x2=Input()
    for i in range(2):
        for j in range(2):
            x1.set_value(i) 
            x2.set_value(j)           
            node_1=Percept([float(w[0]),float(w[1])],float(w[2]))
            node_1.set_inputs([x1,x2])
            node_2=Percept([float(w[3]),float(w[4])],float(w[5]))
            node_2.set_inputs([x1,x2])
            node_3=Percept([float(w[5]),float(w[6])],float(w[7]))
            node_3.set_inputs([node_1, node_2])
            xor=node_3
            v=xor.evaluate()
            acc=acc+abs(arr[i]-v)
            i+1
    return acc/4
            


def hillclimb(Lambda):
    c=0
    w=np.array([random.uniform(-1,1) for i in range(9)])
    while err(w)>0.0001:
        c=c+1
        if c==3000:
            break
        delta = [random.uniform(-Lambda, Lambda) for i in range(9)]
        if err(w+delta)<err(w):
            w=w+delta
    return (w,c)




for L in range(1,26):
    a=0
    for i in range(0,10):
        h=hillclimb(L)
        a=a+h[1]
    print(a/10)
    
    
        
        
    









