import sys
import csv
import random
import math
import statistics
from fuzzyConditional import *
from anytree import Node, RenderTree








def processData(filename,numCond,className,T0):
  #open the read and wite files
  with open(filename)as csvfile:
    readFile=csv.reader(csvfile,delimiter=',')    
    #read data in a row as a list of strings
    firstRow=0
    dictTotal={} #for all attributes key=its k, value = its list of fuzzy
    listOfAttriList=[]
    listOfObjList=[]
    kList=[]
    titleAttrList=[]
    titleFuzzyList=[]
    numObject=0
    for line in readFile:
      #jump off the first line
      if  firstRow==0:
        for k in line:
            kList.extend(int(k))
        firstRow=firstRow+1
        
      elif firstRow==1:
          titleAttrList=line
          print(titleAttrList)
          firstRow=firstRow+1
          
      elif firstRow==2:
          titleFuzzyList=line
          print(titleFuzzyList)
          firstRow=firstRow+1

      #for the real datas
      else:
        numObject +=1
        #change the list of data into a list of floats
        #and write the result data  into a new csv file
        dataList=[]
        #listOfAttriList=[[],[]]
        for i in range(numCond):
          listOfAttriList.extend([[]])
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








def main():
  #read the data
  args =sys.argv[1:]
  if not args:
    print ('usage: filename numOfCondition')
    #first line of file should be k for each attribute
    #second line should be attribute names
    #third line should be each fuzzy set title within each attribute
    sys.exit(1)
    
  filename=args[0]
  numCond=int(args[1])
  className=args[2]
  T0=0.5
 # print(filename,numCond)
  processData(filename,numCond,className,T0)

if __name__ == '__main__':
  main()
