import random
import numpy as np
import itertools
import math
famda=0.1
accuracy=0
total_set=[]
test_set=[]
train_set=[]
training_set=[]
headers=[0,1,2,3,4,5,6,7,8,9]
n=2
train_size=200
class Node:
     def __init__(self, state,parent, children, soln,freq): #state is my category, path is what route I took to get here (yes or no), parent is previously visited category, solution is am I done or going yn...
        self.state=state #state is node or category
        self.parent=parent
        self.children=children
        self.soln=soln #republican or democrat
        self.freq=freq
     def __str__(self, level=0):
        ret = "\t"*level+repr(self.state)+ repr(self.soln)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
     def __repr__(self):
        return '<tree node representation>'
    
def A(x):
    if x>0:
        return 1
    else:
        return 0
def perceptron_learn(ts):
    s=0
    w=np.random.rand(n+1)
    for i in range(100):
        for point in ts:
            xi=point[0]
            fbar=A(np.dot(xi,w))
            fxi=point[1]
            w=w+(famda*(fxi-fbar))*xi              
    accuracy=1-(aggregate(ts,w)/len(ts))
    return (w,accuracy)

def perceptron_test(w,ts):
    dots=[] #set of 0s and 1s based on xi*w to see if it matches point[1] for each of them
    for point in ts:
        xi=point[0]
        fbar=A(np.dot(xi,w))
        dots.append(fbar)
    return dots

def check(w,vector):
    fbar=A(np.dot(vector[0],w))
    return fbar
    
def aggregate(ts,w):
    s=0
    for point in ts:
        s=s+abs(point[1]-A(np.dot(point[0],w)))
    return s
def generateMajority(l):
    num0=0
    num1=0
    for val in l:
        if val==0:
            num0=num0+1
        else:
            num1=num1+1
    if num0>num1:
        return 0
    else:
        return 1
    
def generateData():
     lst=list(map(list,itertools.product([0,1], repeat=int(math.pow(2,n)))))
     combList=list(map(list, itertools.product([0, 1], repeat=n)))
     #print(lst)
     for l in combList:
        l.append(1)
     for l in lst:
        for i in range(len(l)):
            ans=l[i]
            comb=np.array(combList[i])
            tup=(comb,ans)
            training_set.append(tup)
     #print(training_set)
     """
     for l in combList:
        majority=generateMajority(l)
        comb=np.array(l)
        tup=(comb,majority)
        total_set.append(tup)
     """
            
def checkAccuracy(ts,test):
    works=1
    for i in range(len(ts)):
        if ts[i][1]!=test[i]:
            works=0
    return works

def worked(test,vector):
    if test==vector[1]:
        return 1
    return 0

            
def generateTT():
    nums=[]
    while len(nums)<train_size:
        i=random.randint(0,(math.pow(2,n))-1)
        if i not in nums:
            nums.append(i)
    for val in nums:
        train_set.append(total_set[val])
    for t in range(len(total_set)):
        if t not in nums:
            test_set.append(total_set[t])
          
def perceptrons():
    acc=0
    #print("reached")
    generateData() #training size =100 vectors
   # print("reached")
    generateTT()
    #print(train_set)
    for vector in test_set:
        tup=perceptron_learn(train_set)
        test=check(tup[0],vector)
        acc=acc+worked(test,vector)
    return (acc/len(test_set))*100
    
def decisionTree():
    ta=0
    generateData() #training size =100 vectors
    generateTT()
    numNodes=1
    root=Node("", None, [],None,None)
    n=make_tree(root,train_set, 0)
    acc=predict(root)
    print(acc)

def freq_entropy(freq_dict):
     f=list(freq_dict.values()) #how many 0s and how many 1s are in the answer list
     s=sum(f)
     p=[i/s for i in f]
     return (-sum([i * math.log(i,2) for i in p if i>0]))

def freq_dist(data_dict):
     vals=val_list(data_dict) 
     return{a: vals.count(a) for a in set(vals)} 
    
def parameter_entropy(data,col):
     length=len(data)
     total=0
     for v in val_set(data): #set of all possible answers 0 or 1
        eds=extract(data,v)
        l=len(eds)
        e=freq_entropy(freq_dist(eds))
        total=total+ (l/length*e)
     return total

def extract(data,value):
     return [tup for tup in data if tup[1]==value]
    
def val_set(data): #set of the categories
     return set(val_list(data))

def val_list(data):
     return [tup[1] for tup in data] 
    
def make_tree(n,trainDS,level):
     global numNodes
     initial_h=freq_entropy(freq_dist(trainDS)) #dictionary entropy
     best=max((initial_h-parameter_entropy(trainDS,i),i) for i in range(len(headers)))
     p=best[1]
     if level==0:
          n.state=headers[p]
     else: 
          catNode=Node("", None,  [],None,None)
          catNode.state=headers[p] #mainCategory
          catNode.parent=n
          n.children.append(catNode)
          numNodes=numNodes+1
     for v in val_set(trainDS):
          subCatNode=Node("", None, [],None,None)
          subCatNode.state=v
          if level==0:
               subCatNode.parent=n
               n.children.append(subCatNode)
          else:
               subCatNode.parent=catNode
               catNode.children.append(subCatNode)
          new_array=extract(trainDS,v)
          freqs=freq_dist(new_array) #node.set children each of these things
          subCatNode.freq=freqs
          if freq_entropy(freqs)<0.0000001:
               subCatNode.soln=getSoln(subCatNode,new_array)
          else:
               make_tree(subCatNode, new_array,level+1)
               numNodes=numNodes+1
     return numNodes


def getSoln(n,new_array):
     soln=""
     sCategory=n.state
     parent=n.parent
     for point in new_array:
          data=point[0]
          if data[headers.index(parent.state)]==sCategory: #if the data for that category matches the subcategory value (y/n)
               soln=point[1]
               break
     return soln

def predict(start):#for person, traverse through my tree to get the correct answer
     correct=0
     for point in test_set:
          person=point[0]
          soln=traverseTree(start, person)
          if soln is not "FAIL" and soln==point[1]:
               correct=correct+1
     return correct/len(test_set)*100

def traverseTree(currNode, person):
     questionList=[]
     if currNode.soln is None:
          cat=currNode.state
          if cat in headers:
               responseI=person[headers.index(cat)]
               for child in currNode.children:
                    if child.state==responseI:
                         if child.soln is not None:
                              return child.soln
                         else:
                              return traverseTree(child, person)                    
          else: 
               for child in currNode.children: #child of a subcategory is a category
                    if child.soln is None:
                         return traverseTree(child,person)
                    else:
                         return currNode.soln
     else:
          return currNode.soln

t=0
#
generateData()
print(training_set)
step=int(math.pow(2,n))
#print(step)
acc=0
for x in range(int(math.pow(2,math.pow(2,n)))):
     newts=[]
     for y in range(t,t+step):
          newts.append(training_set[y])
     tup=perceptron_learn(newts)
     print(tup[0])
     test=perceptron_test(tup[0],newts)
     print(test)
     t=t+step
     acc=acc+checkAccuracy(newts,test)
     #print(acc)
#print(acc)

"""
numNodes=1
#print(acc/math.pow(2,math.pow(2,n)))
#acc=[]
#decisionTree()
acc=perceptrons()
print(acc)
#acc.append(a)
#print(acc)
"""
    
   
#TEST FOR ALL TRAINING SETS AND COMPUTE ACCURACY AND STUFFS
