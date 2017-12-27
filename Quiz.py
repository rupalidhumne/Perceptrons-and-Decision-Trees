global NumNodes
trains=[]
import csv
global CLASS_idx
testDS={}
trainDS={}
ds={}
import math
import random
global root
trainVals=set()
global headers
global headers2
totAccuracy=[]
nn=[]
#if I reach a question mark then count it as a no
class Node:
     def __init__(self, state,parent, children, soln,freq,path): #state is my category, path is what route I took to get here (yes or no), parent is previously visited category, solution is am I done or going yn...
        self.state=state #state is node or category
        self.parent=parent
        self.children=children
        self.soln=soln #republican or democrat
        self.freq=freq
        self.path=path
     def __str__(self, level=0):
        ret = "\t"*level+repr(self.state)+ repr(self.soln)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
     def __repr__(self):
        return '<tree node representation>'

        
def generateTrain(file):
     global CLASS_idx
     global headers
     with open(file) as csvfile:
          reader = csv.reader(csvfile)
          headers=next(reader)[1:] #this includes the last party column so might want to get rid
          for row in reader:
               trainDS.update({row[0]:row[1:]})
     csvfile.close()
     CLASS_idx=len(headers)-1 #number of categories
     
          
def generateTest(file):
     global headers2
     with open(file) as csvfile:
          reader = csv.reader(csvfile)
          headers2=next(reader)[1:] #this includes the last party column so might want to get rid
          for row in reader:
               testDS.update({row[0]:row[1:]})
     csvfile.close()
   
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
     
def predict(start):#for person, traverse through my tree to get the correct answer
     correct=0
     p=0
     incorrect=[]
     for key in testDS:
          person=testDS[key]
          path=traverseTree(start, person,[])
          if path==['A7', 'Sometimes', 'A1', 'Sometimes', 'A2', 'Never', 'A6']:
               p=p+1
          if soln is not "FAIL" and soln==person[len(person)-1]:
               correct=correct+1
          else:
               incorrect.append(person)
     print(len(incorrect))
     numQues(incorrect)
     print(p)
     return correct/len(testDS.keys())*100
#make a method that just returns the soln
def numQues(arr):
    n=0
    for row in arr:
        if '?' in row:
            n=n+1
    print(n)
def val_list(data,column):
     #print(data.values())
     return [val[column] for val in data.values()] #for list in data set return the last column so yes/no

def freq_dist(data_dict):
     vals=val_list(data_dict,CLASS_idx) #last column
     #print(vals)
     return{a: vals.count(a) for a in set(vals)} #numbers of yes versus number of no overall

def val_set(data,column): #set of the categories
     return set(val_list(data,column))
          
def freq_entropy(freq_dict):
     f=list(freq_dict.values())
     s=sum(f)
     p=[i/s for i in f]
     return (-sum([i * math.log(i,2) for i in p if i>0]))
     

def traverseTree(currNode, person,path):
     questionList=[]
     if currNode.soln is None:
          cat=currNode.state
          if cat in headers:
               path.append(cat)
               responseI=person[headers.index(cat)]
               for child in currNode.children:
                    if responseI=='?':
                         path.append(child)
                         prediction=traverseTree(child,person)
                         questionList.append(prediction)
                    elif child.state==responseI:
                         if child.soln is not None:
                              return child.soln
                         else:
                              path.append(child)
                              return traverseTree(child, person)
               if responseI=='?':
                    if questionList[0] != questionList[1]:
                         r=random.randint(0,1)
                         return questionList[r]
                    else:
                         return questionList[0]
                    
          else: 
               for child in currNode.children: #child of a subcategory is a category
                    if child.soln is None:
                         path.append(child)
                         return traverseTree(child,person)
                    else:
                         return currNode.soln
     else:
          return currNode.soln
                   
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

        
def make_tree(n,trainDS,level):
    global numNodes
    initial_h=freq_entropy(freq_dist(trainDS)) #dictionary entropy
    print(initial_h)
    best=max((initial_h-parameter_entropy(trainDS,i),i) for i in range(CLASS_idx))
    p=best[1]
    if level==0:
      n.state=headers[p]
    else: 
      catNode=Node("", None,  [],None,None,[])
      catNode.state=headers[p] #mainCategory
      catNode.parent=n
      n.children.append(catNode)
    #         currNode=catNode #WILL THIS CHANGE THE VALUES FOR N AS WELL
      numNodes=numNodes+1
    for v in val_set(trainDS,p):
      subCatNode=Node("", None, [],None,None,[])
      subCatNode.state=v
    #         subCatNode.parent=currNode
      if level==0:
           subCatNode.parent=n
           n.children.append(subCatNode)
      else:
           subCatNode.parent=catNode
           catNode.children.append(subCatNode)
    #         currNode.children.append(subCatNode)
      new_ds=extract(trainDS,p,v)
      freqs=freq_dist(new_ds) #node.set children each of these things
      subCatNode.freq=freqs
      if freq_entropy(freqs)<0.0000001:
           subCatNode.soln=getSoln(subCatNode,new_ds)
      else:
           make_tree(subCatNode, new_ds,level+1)
           numNodes=numNodes+1
    return numNodes
def getSoln(n,new_ds):
     #print(n.state)
     soln=""
     sCategory=n.state
     parent=n.parent
     for key in new_ds:
          data=new_ds[key]
          if data[headers.index(parent.state)]==sCategory: #if the data for that category matches the subcategory value (y/n)
               soln=data[len(data)-1]
               break
     return soln



fileTrain='quizA_train.csv'
fileTest='quizA_test.csv'
generateTrain(fileTrain)
generateTest(fileTest)
#testDS.update({0:['?', '?', 'Sometimes', 'Never', 'Never', 'Never', 'Sometimes', 'Sometimes','?', '?', 'Never', 'Sometimes', 'Never', 'Sometimes', 'Never', 'Sometimes', 'Never', 'Never', 'Sometimes']}) 
root=Node("", None, [],None,None,[])
numNodes=1
n=make_tree(root, trainDS, 0)
print(str(root))
acc=predict(root)
#openCSV(file)
"""
for i in range (0,20):
     numNodes=1
     generateTrain()
     generateTest()
     root=Node("", None, [],None,None) #path would be response of my parent before me
     n=make_tree(root, trainDS, 0)
     acc=predict(root)
     print(acc)
     #print(str(root))
     nn.append(n)
     tSize=tSize+10
"""
print(n)
#print(acc)
#print(totAccuracy)
#2 files, test train, 
