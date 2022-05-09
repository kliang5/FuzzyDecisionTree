import sys
import csv
import random
import math
import statistics
 


  
#a method that cluster a one-dimension list into k clusters
#returns a tuple of means' list and cluster list
def cluster(datas,k):
  #print(k)
  dataList=sorted(datas.copy())
  #print(dataList) #print the input datalist
  #randomly select k datas as means
  meanNoSatisfied= True
  meanList=[]
  while meanNoSatisfied:
    meanList=random.sample(dataList,k)
    outsideTest=0
    for i in range(k):
      sample=meanList[i]
      insideTest=0
      for j in range(k):
        if i==j:
          insideTest +=1
        else:
          if sample==meanList[j]:
            meanNoSatisfied= True
          else:
            insideTest +=1
        #print(insideTest+ 10000)
      if insideTest==k :
        outsideTest+=1
    #print(outsideTest)
    if outsideTest==k:
      meanNoSatisfied=False
      
  #a nested list to hold lists of datas within each cluster
  clusterList=[]
  for i in range(k):
      clusterList.extend([[]])
  continueLoop=True
  loopNum=0
  while continueLoop:
    for data in dataList:
      distanceList=[]
      for mean in meanList:
          distance=data-mean
          distanceList=distanceList+[abs(distance)]
      mindistance=min(distanceList)
      minIndex=distanceList.index(mindistance)
      clusterList[minIndex].extend([data]) 
    close=0
    j=0
    for cluster in clusterList:
      newMean=statistics.mean(cluster)
      #tolerance is adjusted by the average of the database
      if math.isclose(meanList[j],newMean,abs_tol=0.000001):
        close=close+1
      meanList[j]=newMean
      j=j+1
    if [] in clusterList:
      break
    if close==k:
        continueLoop=False
    else:
        clusterList=[]
        for i in range(k):
          clusterList.extend([[]])
    #the max iteration is 300 times
    if loopNum==300:
      break
     
    loopNum=loopNum+1
  #since the order of meanList and clusterList are the same
  #use sorted directly could work
  #print(clusterList)
  return (sorted(meanList),sorted(clusterList))


#a  helper method in fuzzification that calculates the gain
#of a result k
def Gain(dict2,datas,k,clusterList):
  #print(clusterList)
  dataList=datas.copy()
  numData=len(dataList)#=n
  numClass=[]
 # classDegree=[]
  fuzzyEntropy=[]
  sumMember=[]
  #v= no.1

  #loop for v
  for v in range(k):
    classDegree=[]
    summember=0
    #loop for c 
    for c in range(k):
      sumClass=0
      sumAll=0
      #loop  for  x
      for x in range(numData):
        dataNow=dataList[x]
        #print(dict2[x][v])
        sumAll += dict2[x][v]
        #get the total sum of all membership funcs
        summember += dict2[x][v]
        #print(dataNow in clusterList[c])
        if dataNow in clusterList[c]:
          sumClass += dict2[x][v]
          #print(dict2[x][v])
      classDegree.extend([(sumClass/sumAll)])
      #print(sumClass,sumAll,(sumClass/sumAll))
      #get number of each class
      numClass.extend([len(clusterList[c])])
    fe=0
    for cd in classDegree:
      #print (cd)
      if cd==0:
        fe+=0
      else:
        fe += cd*math.log(float(cd),2.0)
    fuzzyEntropy.extend([-fe])
    sumMember.extend([summember])
  totalSum=0
  for  summary in sumMember:
    totalSum  += summary
  classPart=0
  #print(numClass)
  for num in numClass:
    #print (num)
    classPart += -float(num/numData)*math.log(float(num/numData),2.0)
  vPart=0
  for i in  range(k):
    vPart += ((sumMember[i]/totalSum)*fuzzyEntropy[i])
  gain=classPart-vPart
  return gain
  
  
  
#input is a list of datas under one attribute  
def fuzzification(datas,T0):
  #follow the steps in essay9
  #get number of data, maxData and minData

  #dataList keeps the order of the data
  dataList=datas.copy()
  membershipList=[]
  #dict saves the membership funs of each data for different k
  dict={}
  gain={}
  minData=min(dataList)
  maxData=max(dataList)
  num=len(dataList)
  k=2  #k=2 initial
  #To???
  T=T0
  loopSatisfied=True
  #print(dataList)
  while loopSatisfied:
    clusterResults=cluster(dataList,k)
    #print(clusterResults)
    meanList=clusterResults[0]
    clusterList=clusterResults[1]
    #step 3
    #dict2 is the nested-dict
    #keys are the datas and values are their membership funs'lists
    dict2={}
    dict[k]=dict2
    #loop to get membership funs for each data in this k
    for i in range(num):
      #initial the value of dict2 under the key (data i) is a list of mem funs
      dict2[i]=[]
      for j in range(k):
        dict2[i].extend([0])
      t=0
      while t<k:
        if t==0:
          dataNow=dataList[i]
          if dataNow>=minData and dataNow <= meanList[0]:
            member1=1-((((dataNow-meanList[0])/(minData-meanList[0]))*0.5))
            dict2[i][t]=member1
            #print('a')
          elif dataNow >= meanList[0] and dataNow<= meanList[1]:
            member1=1-((dataNow-meanList[0])/(meanList[1]-meanList[0]))
            dict2[i][t]=member1
            #print('b')
          else:
            member1=0
            dict2[i][t]=member1
        elif t==(k-1):
          dataNow=dataList[i]
          if dataNow >= meanList[k-2] and dataNow <=  meanList[k-1]:
            memberk=1-((dataNow-meanList[k-1])/(meanList[k-2]-meanList[k-1]))
            dict2[i][t]=memberk
            #print('c')
            #print(dataNow,meanList[k-1],meanList[k-2])
          elif dataNow >= meanList[k-1] and dataNow <= maxData:
            memberk=1-((((dataNow-meanList[k-1])/(maxData-meanList[k-1]))*0.5))
            dict2[i][t]=memberk
            #print('d')
          else:
            memberk=0
            dict2[i][t]=memberk
            #print('e')
        else:
          dataNow=dataList[i]
          if dataNow> meanList[t-2] and dataNow<meanList[t-1]:
            membert=1-((dataNow-meanList[t-1])/(meanList[t-2]-meanList[t-1]))
            dict2[i][t]=membert
            #print('f')
          elif dataNow>meanList[t-1] and dataNow<= meanList[t]:
            membert=1-((dataNow-meanList[t-1])/(meanList[t]-meanList[t-1]))
            dict2[i][t]=membert
            #print('g')
          else:
            membert=0
            dict2[i][t]=membert
        #print(dict2[i][t])
        t=t+1
      #loop to next data
      i=i+1
    #now we get a full dict2
    #step 4:calculate Gain
    #print(clusterList)
    gainNow=Gain(dict2,datas,k,clusterList)
    gain[k]=gainNow
    gainLast=0
    if k>2:
      gainLast=gain[k-1]
    differenceGain=gainNow-gainLast
    if k==2 or abs(differenceGain) >T0:
      k+=1
      loopSatisfied=True
    else:
      k=k-1
      loopSatisfied=False
    #print(k)
  return (dict[k],k)
    
        
    
 






def processData(filename,numCond,className,T0):
  #open the read and wite files
  with open(filename)as csvfile:
    readFile=csv.reader(csvfile,delimiter=',')    
  #read data in a row as a list of strings
  #wb = xrld.open_workbook(filename) 
  #sheet = wb.sheet_by_index(0)
  #sheet.cell_value(0, 0)
  
    firstRow=1
    listOfAttriList=[]
    for i in range(numCond):
      listOfAttriList.extend([[]])
    listOfObjList=[]
    numObject=1
    for line in readFile:
      #jump off the first line
      if  firstRow==0:
        firstRow=firstRow+1
        continue


      #for the real datas
      else:
        numObject +=1
        #change the list of data into a list of floats
        #and write the result data  into a new csv file
        dataList=[]
        #listOfAttriList=[[],[]]
         
        listNum=0
        #creating a list of attributes list
        #each element of big list  is a list of  conditional attributes
        #like the first object's second conditional attribute is at
        #listOfAttriList[1](--second attribute)[0](--first object)
        for data in line[:numCond]:
          listOfAttriList[listNum].extend([float(data)])
          #if listOfAttriList[listNum]in listOfAttriList:
          #  listOfAttriList[listNum]=listOfAttri[listNum]+[float(data)]
          #else:
          #  listOfAttriList[listNum]=[float(data)]
          listNum=listNum+1
  
  csvfile.close()
  #fuuzify the data
  #listOfObjList=[[],[]]
  #for loop to fuzzify each conditional attribute
  attributeNum=0
  dict={}
  for i in range(numObject):
      listOfObjList.extend([[]])
  print("k numbers are:")
  #print(listOfAttriList)

  for attributeList in listOfAttriList:
    #print(attributeList)
    #get result of a list of object datas of one attribute
    Resulttuple=(fuzzification(attributeList,T0))
    dict2=Resulttuple[0]
    k=Resulttuple[1]
    resultList=list(dict2.values())
    print(k)
    #print(resultList)
    attributeLen= len(resultList)    
    #k=len(resultList[0])
    dict[attributeNum]=k
    for i in range(attributeLen):
      #print(resultList[i])
      for data in resultList[i]:
        listOfObjList[i].extend([data])
    attributeNum+=1
  

         
  writeFile=open(className,mode='w')
  writer=csv.writer(writeFile) 
  #write the result data with the order of objects
  for objectList in listOfObjList:
    writer.writerow(objectList)
  writeFile.close()
           


  
 
def main():
  #read the data
  args =sys.argv[1:]
  if not args:
    print ('usage: filename numberOfConditionalAttributes ClassName rowNum')
    sys.exit(1)
    
  filename=args[0]
  numCond=int(args[1])
  className=args[2]
  T0=6
 # print(filename,numCond)
  processData(filename,numCond,className,T0)

if __name__ == '__main__':
  main()
