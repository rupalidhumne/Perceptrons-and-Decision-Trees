import math
import csv

data=[]
categories=[]
lookedAt={}
mainCats=['Outlook','Temp', 'Humidity', 'Wind']
def entropy(freqList):
    #print(str(freqList))
    denom=sum(freqList)
    entropy=0
    for val in freqList:
        #print(str(val))
        #print(str(denom))
        if val==0:
            entropy= 0
        else:
            entropy=entropy+(val/denom)*(math.log2(val/denom))
    return entropy*-1

def averageE(LL):
    denom=0
    aentropy=0
    for l in LL:
        denom=denom+sum(l)
    for l in LL:
        val=sum(l)           
        aentropy=aentropy+(val/denom)*entropy(l)
    return aentropy

def best_col(ds): #constraints are categories so like sunny Temp or just Outlook etc
    LE=[] #average entropy per category
    if ds==None:
        i=0
        for option in categories:
            #if lookedAt[option[0]]==False:
            YN={}
            for row in data:
                sc=row[i]
                answer=row[len(row)-1]
                if sc not in YN:
                    YN.update({sc:[0,0]}) #subcat and then tuple of yes and no
                tup=YN[sc]
                if answer=='Yes':
                    tup[0]=tup[0]+1
                else:
                    tup[1]=tup[1]+1
            entropyCat=[]
            for key in YN: #for each subcategory
                smallE=[YN[key][0],YN[key][1]] #yes and nos
                entropyCat.append(smallE)
            ae=averageE(entropyCat)
            LE.append(ae)
            i=i+1
    else:
        i=0
        for option in categories:
            #if lookedAt[option[0]]==False:
            YN={}
            for row in data:
                rowWorks=False #only use the row if it satisfies the constraints i.e. looking at temps on sunny days
                for constraint in ds:
                    if constraint not in row:
                        rowWorks=False
                    else:
                        rowWorks=True
                if rowWorks==True:
                    sc=row[i]
                    answer=row[len(row)-1]
                    if sc not in YN:
                        YN.update({sc:[0,0]}) #subcat and then tuple of yes and no
                    tup=YN[sc]
                    if answer=='Yes':
                        tup[0]=tup[0]+1
                    else:
                        tup[1]=tup[1]+1
            entropyCat=[]
            for key in YN: #for each subcategory
                smallE=[YN[key][0],YN[key][1]] #yes and nos
                entropyCat.append(smallE)
            ae=averageE(entropyCat)
            LE.append(ae)
            #print("reached")
            i=i+1
            #else:
 #               print("reached")
 #               i=i+1
    #print(LE)
    print(min(LE))
    m=LE.index(min(LE)) #index of smallest average entropy
    return m
               
def extract(ds,sc):
    constraints=[]
    constraints.append(sc)
    YN={'Yes':0, 'No':0}
    if ds==None:
        for row in data:
            if sc in row:
                answer=row[len(row)-1]
                YN[answer]=YN[answer]+1
    else:
        for row in data:
            rowWorks=False
            for c in ds:
                if c not in row and sc in row:
                    rowWorks=False
                if c in row and sc in row:
                    rowWorks=True
            if rowWorks==True:
                answer=row[len(row)-1]
                YN[answer]=YN[answer]+1
    LYN=[YN['Yes'], YN['No']]
    if entropy(LYN)==0:
        for row in data:
            if sc in row:
                answer=row[len(row)-1]
        return (constraints,answer)
    else:
        return (constraints,None)
       
    
def make_tree(ds):
    keys=[]
    for l in categories:
        keys.append(l[0])
    col=best_col(ds)
    print("--- " + str(keys[col]) + "?")
 #   lookedAt[keys[col]]=True #that category has been used
    subcats=[]
    catRow=categories[col]
    for i in range(1,len(catRow)):
        subcats.append(catRow[i]) #all subcats for a category
    for sc in subcats:
        new_ds=extract(ds, sc)
        if new_ds[1]!=None:
            print("--->" + str(sc) + " " + new_ds[1])
        else:
            print("--->"+ str(sc) + "..." )
            make_tree(new_ds[0])

              
def openCSV(): 
    with open('tennis_tree.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        i=0
        for row in reader:
            if i==0: #categories
                for v in range(1,5):
                    categories.append([row[v]])
                    lookedAt[row[v]]=False
            else:
                data.append(row[1:len(row)]) #append all data as a new list
                s=1
                for option in categories:
                    subcat=row[s] #actual value of subcategory
                    if subcat not in option:
                       option.append(subcat)
                    s=s+1
            i=i+1
    
                        
                    
            
openCSV()
#print(str(categories))
make_tree(None)


