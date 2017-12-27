global numNodes
tSize=10
trains=[]
import csv
global CLASS_idx
correct=0
testDS={}
trainDS={}
ds={}
import math
import random
global root
trainVals=set()
global headers
totAccuracy=[]
nn=[]
used=[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
#if I reach a question mark then count it as a no
class Node:
     def __init__(self, state,children, soln,path): #state is my category, path is what route I took to get here (yes or no), parent is previously visited category, solution is am I done or going yn...
        self.state=state #state is node or category
        self.children=children
        self.soln=soln #republican or democrat
        self.path=path
     def __str__(self, level=0):
        ret = "\t"*level+repr(self.state)+ repr(self.soln)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
     def __repr__(self):
        return '<tree node representation>'

        
def generateTrain():
     while len(trainDS.keys())<tSize:
          n=random.randint(1,435)
          trainVals.add(n)
          key="P"+str(n)
          if '?' not in ds[key]:
               trainDS.update({key:ds[key]})
          
def generateTest():
     for i in range(1,436):
          if i not in trainVals and len(testDS.keys())<2:
               tKey="P"+str(i)
               testDS.update({tKey:ds[tKey]})

     
def openCSV(file): #will make test and tree
     global CLASS_idx
     global headers
     with open(file) as csvfile:
          reader = csv.reader(csvfile)
          headers=next(reader)[1:] #this includes the last party column so might want to get rid
          i=1
          for row in reader:
               if i<436:
                    ds.update({row[0]:row[1:]})
                    i=i+1
               else:
                    break
     csvfile.close()
     CLASS_idx=len(headers)-1 #number of categories
     
def predict():#for person, traverse through my tree to get the correct answer
    correct=0
    for key in testDS:
        person=testDS[key]
        traverseTree(root, person)

def val_list(data,column):
     #print(data.values())
     return [val[column] for val in data.values()] #for list in data set return the last column so dem/repub

def freq_dist(data_dict):
     vals=val_list(data_dict,CLASS_idx) #last column
     #print(vals)
     return{a: vals.count(a) for a in set(vals)} #numbers of yes versus number of no overall

def val_set(data,column): #set of the categories
     return set(val_list(data,column))
          
def freq_entropy(freq_dict):
     f=list(freq_dict.values())
     #print(f)
     s=sum(f)
     #print(s)
     p=[i/s for i in f]
     return (-sum([i * math.log(i,2) for i in p if i>0]))
     

def traverseTree(currNode, person):
    print("reached")
    print(currNode.state)
    if currNode.state is not 'answer':
        responseI=person[headers.index(currNode.state)]#either y or n for that category
        for child in currNode.children:
            if child.path==responseI: #path can either be y or n so if person is y or n check which one
                if child.state=='answer':
                    traverseTree(child, person)
    else:
        print('reached')
        print(currNode.soln)
        print(person[len(person)-1])
        if currNode.soln==person[len(person)-1]:
            correct=correct+1
          
                                  
def extract(data,column,value): #return rows with cat s (V15) for which sub cat =yes and then rows where in V15 the subcat is no
     return {a:data[a] for a in data if data[a][column]==value}    
     

def parameter_entropy(data,col):
     length=len(data)
     total=0
     for v in val_set(data,col):
        eds=extract(data,col,v)
        l=len(eds)
        e=freq_entropy(freq_dist(eds))
        total=total+ (l/length*e)
     return total    

        
def make_tree(value, n,level):
    global numNodes
    newNode=n
    initial_h=freq_entropy(freq_dist(trainDS)) #dictionary entropy
    best=max((initial_h-parameter_entropy(trainDS,i),i) for i in range(CLASS_idx))
    p=best[1]
    if level==0:
        n.state=headers[p]
    else:
        newNode=Node("", [],None,None)
        newNode.path=value
        newNode.state=headers[p]       
        numNodes=numNodes+1
        n.children.append(newNode)
    for v in val_set(trainDS,p):
        new_ds=extract(trainDS,p,v)
        freqs=freq_dist(new_ds)
        if freq_entropy(freqs)<0.001: #make a new node that doesn't have a state but just says republican
            solNode=Node('answer', [],None,None)
            solNode.path=v
            numNodes=numNodes+1
            solNode.soln=list(freqs.keys())[0] #ex. if yes all corresp to republican then only key should be
            if level==0:
                n.children.append(solNode)
            else:
                newNode.children.append(solNode)
        else:
            if level==0:
                make_tree(v,n,level+1)
            else:
                print(v)
                print(newNode.state)
                make_tree(v,newNode,level+1)
    return numNodes
file='house-votes-84.csv'
openCSV(file)
numNodes=1
generateTrain()
print(trainDS)
generateTest()
print(testDS)
root=Node("", [],None,None) #path would be response of my parent before me
n=make_tree(None, root,0)
print(str(root))
nn.append(n)
acc=(correct/len(testDS.keys()))*100
print(acc)
print(n)

