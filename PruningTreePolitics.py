global numNodes #question, 10,20,30 good but as it goes up accuracy goes down but tree ok for 10-30 even when nodes not just 3
tSize=10 #what else can I do to test
global size
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
global acc1
global acc2
totAccuracy=[]
TA=[]
nn=[]
#if I reach a question mark then count it as a no
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

        
def generateTrain():

     while len(trainDS.keys())<tSize:
          n=random.randint(1,435)
          trainVals.add(n)
          key="P"+str(n)
          if '?' not in ds[key]:
               trainDS.update({key:ds[key]})
     """
     global headers
     with open(file) as csvfile:
          reader = csv.reader(csvfile)
          headers2=next(reader)[1:] #this includes the last party column so might want to get rid
          for row in reader:
               ds.update({row[0]:row[1:]})
     csvfile.close()
     """    
          
def generateTest():

     for i in range(1,436):
          if i not in trainVals:
               tKey="P"+str(i)
               testDS.update({tKey:ds[tKey]})
     """
     global CLASS_idx
     global headers
     with open(file) as csvfile:
          reader = csv.reader(csvfile)
          headers=next(reader)[1:] #this includes the last party column so might want to get rid
          for row in reader:
               ds.update({row[0]:row[1:]})
     csvfile.close()
     CLASS_idx=len(headers)-1 #number of categories
     """
     

     
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
     for key in testDS:
          person=testDS[key]
          soln=traverseTree(start, person)
          if soln is not "FAIL" and soln==person[len(person)-1]:
               correct=correct+1
     return correct/len(testDS.keys())*100
#make a method that just returns the soln
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
     

def traverseTree(currNode, person):
     questionList=[]
     if currNode.soln is None:
          cat=currNode.state
          if cat in headers:
               responseI=person[headers.index(cat)]
               for child in currNode.children:
                    if responseI=='?':
                         prediction=traverseTree(child,person)
                         questionList.append(prediction)
                    elif child.state==responseI:
                         if child.soln is not None:
                              return child.soln
                         else:
                              return traverseTree(child, person)
               if responseI=='?':
                    if questionList[0]==questionList[1]:
                         r=random.randint(0,1)
                         return questionList[r]
                    
          else: 
               for child in currNode.children: #child of a subcategory is a category
                    if child.soln is None:
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

def pruning(n): #set as soln, check accuracy of new tree, if new tree is in interval accuracy keep going else set soln back to none#pop a node, check frequency and if frequecy okay than getSolution, make new tree and check accuracy to old tree
     nodes=addtoQueue(n)
     #print(nodes)
     for vertex in nodes:
          freqDict=vertex.freq
          oldSoln=vertex.soln
          if freqDict is not None:
               maxVal=max(freqDict.values())
               for key in freqDict:
                    if freqDict[key]==maxVal:
                         vertex.soln=key
               if compareAccuracy(nodes[0])==False:
                    vertex.soln=oldSoln              
     return nodes[0]
def compareAccuracy(newTree):
     acc2=predict(newTree)
     if abs(acc1-acc2)<=0.5:
          #print(acc1)
          #print(acc2)
          return True
     return False
     
def addtoQueue(node): #add copies of the node to the queue to make a fake tree
    allNodes=[]
    queue=[]
    queue.append(node)
    while queue:
        vertex=queue.pop(0)
        if vertex not in allNodes:
            allNodes.append(vertex)#FIGURE OUT HOW TO ADD COPY OF NOE
            for child in vertex.children:
                queue.append(child)
    return allNodes
       
def make_tree(n,trainDS,level):
     global numNodes
 #    currNode=n
     initial_h=freq_entropy(freq_dist(trainDS)) #dictionary entropy
     best=max((initial_h-parameter_entropy(trainDS,i),i) for i in range(CLASS_idx))
     p=best[1]
     if level==0:
          n.state=headers[p]
     else: 
          catNode=Node("", None,  [],None,None)
          catNode.state=headers[p] #mainCategory
          catNode.parent=n
          n.children.append(catNode)
 #         currNode=catNode #WILL THIS CHANGE THE VALUES FOR N AS WELL
          numNodes=numNodes+1
     for v in val_set(trainDS,p):
          subCatNode=Node("", None, [],None,None)
          subCatNode.state=v
 #         subCatNode.parent=currNode
          if level==0:
               subCatNode.parent=n
               n.children.append(subCatNode)
          else:
               subCatNode.parent=catNode
               catNode.children.append(subCatNode)
          new_ds=extract(trainDS,p,v) #extract all data where col = yes or no
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

def treeSize(node,allNodes):
     global size
     end=True
     for child in node.children:
          if child.soln is None:
               end=False
     if end==False:
          for child in node.children:
               if child.soln is None:
                    size=size+1
                    return treeSize(child,allNodes)
     return size                                       
               
     
     

file='house-votes-84.csv'
openCSV(file)
for i in range (0,20): #after you get the accuracy for the old tree, you prune the new tree & then you compare accuracies for test a
     global acc1
     global acc2
     numNodes=1 #do you essentially run through the test for old tree and new tree and compare, or just run 1st test for new tree and 
     generateTrain() #decide whether to keep or remove
     generateTest()
     root=Node("", None, [],None,None) #path would be response of my parent before me
     n=make_tree(root, trainDS, 0)
     acc1=predict(root)
     #print(str(root))
     TA.append(acc1)
     newTree=pruning(root)
     #print(str(newTree))
     acc2=predict(newTree)
     totAccuracy.append(acc2)
     size=1
     nodes=addtoQueue(newTree)
     size=treeSize(newTree,nodes)
     nn.append(size)
     tSize=tSize+10
print(nn)
print(totAccuracy)
