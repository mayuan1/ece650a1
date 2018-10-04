import sys
import re
import tempfile
import itertools
import numpy
import math

# YOUR CODE GOES HERE
print("Please enter street name and action")
# use dictionary to store data
StreetList={}
StreetNameList=[]
InputVexList={}
g=globals()
EdgeList={}
ResultEdgeList={}
RawVertex={}
ResultVertexList={}

def main():
    while True:
          
        CmdInput=sys.stdin.readline()

        regadd=re.compile(r'\s*[a]\s+\"\w+(\s*\w+\s*)*\"(\s*\(\s*-?\d+\s*\,\s*-?\d+\s*\))+$')
        regcha=re.compile(r'\s*[c]\s+\"\w+(\s*\w+\s*)*\"(\s*\(\s*-?\d+\s*\,\s*-?\d+\s*\))+$')
        regrem=re.compile(r'\s*[r]\s+\"\w+(\s*\w+\s*)*\"\s*$')
        reggo=re.compile(r'\s*[g]$')
        regexit=re.compile(r'\n')


        #if Cmd == 'a':
        if regadd.match(CmdInput):
            # check existing streets name
            # add street name in db
            if CheckBracket(CmdInput):
                CmdInput=CmdInput.replace('\n','')
                StreetDetail=re.split("\"", CmdInput.split(" ", 1)[1])
                StreetName=StreetDetail[1].replace(" ","")
                StreetCoor=StreetDetail[2].replace(" ","")
                InputCoor=re.findall(r"\((.*?)\)",StreetCoor)
                # check if street name alread exists
                if not StreetList:
                    StreetNameList.append(StreetName)
                    CList=[]
                    for InputIdx in range(0,(len(InputCoor)-1)):
                        #create street object
                        EndPoints=[]
                        EndPoints.append(InputCoor[InputIdx])
                        EndPoints.append(InputCoor[(InputIdx+1)])
                        NewStreet=StreetName+str(InputIdx)
                        #Line=GetLine(EndPoints)
                        g[NewStreet]=Street(StreetName,EndPoints,InputIdx)
                        CList.append(NewStreet)
                    StreetList[StreetName]=CList
                    #print ("New street "+StreetName+" is added.")
                else:
                    for SN in StreetNameList:
                        if StreetName==SN:
                            print("Error: Street name already exists. Please use c to change street details.")
                            break
                    else:
                        StreetNameList.append(StreetName)
                        CList=[]
                        for InputIdx in range(0,(len(InputCoor)-1)):
                            EndPoints=[]
                            EndPoints.append(InputCoor[InputIdx])
                            EndPoints.append(InputCoor[(InputIdx+1)])
                            NewStreet=StreetName+str(InputIdx)
                            #Line=GetLine(EndPoints)
                            g[NewStreet]=Street(StreetName,EndPoints,InputIdx)
                            CList.append(NewStreet)
                        StreetList[StreetName]=CList
                        #print ("New street "+StreetName +" is added.")
            else:
                print("Error: missing brackets for streets coordinates")
        elif regcha.match(CmdInput):
        #elif Cmd == 'c':
            # check existing street name, then change it
            if CheckBracket(CmdInput):
                CmdInput=CmdInput.replace('\n','')
                StreetDetail=re.split("\"", CmdInput.split(" ", 1)[1])
                StreetName=StreetDetail[1].replace(" ","")
                StreetCoor=StreetDetail[2].replace(" ","")
                InputCoor=re.findall(r"\((.*?)\)",StreetCoor)
                # check if street name alread exists
                if not StreetList:
                    print ("Error: No street detail exists. Please add them first.")
                else:
                    for SN in StreetList:
                        if StreetName == SN:
                            #print("Find street: " + SN + ". Start to change coordinate")
                            CList=[]
                            for InputIdx in range(0,(len(InputCoor)-1)):
                                #create street object
                                EndPoints=[]
                                EndPoints.append(InputCoor[InputIdx])
                                EndPoints.append(InputCoor[(InputIdx+1)])
                                NewStreet=StreetName+str(InputIdx)
                                #Line=GetLine(EndPoints)
                                g[NewStreet]=Street(StreetName,EndPoints,InputIdx)
                                CList.append(NewStreet)
                            StreetList[StreetName]=CList
                            break
                    else:
                        print ("Error: change action for a street that does not exist.")
            else:
                print("Error: missing brackets for streets coordinates")
        elif regrem.match(CmdInput):
        #elif Cmd == 'r':
            #check existing street name, then remove it
            CmdInput=CmdInput.replace('\n','')
            StreetDetail=re.split("\"", CmdInput.split(" ", 1)[1])
            StreetName=StreetDetail[1].replace(" ","")
            if not StreetList:
                print ("Error: No street exists. Please add streets.")
            else:
                for SN in StreetList:
                        if StreetName == SN:
                            #print("Find street: " + SN + ". Start to remove street.")
                            # remove street instances
                            StreetBranch=StreetList[SN]
                            for  SB in StreetBranch:
                                del g[SB]
                            del StreetList[StreetName]
                            StreetNameList.remove(StreetName)
                            break
                else:
                    print ("Error: remove action for a street that does not exist.")
        elif reggo.match(CmdInput):
            # check db, genertate graph
            # get intersection points by looping through two street
            #print 'StreetList: ',StreetList
            #print 'StreetNameList: ',StreetNameList
            CmdInput=CmdInput.replace('\n','')
            for i in range(0,(len(StreetNameList)-1)) :
                for j in range(i+1,len(StreetNameList)):
                    SN1=StreetNameList[i]
                    SN2=StreetNameList[j]
                    List1=StreetList[SN1]
                    List2=StreetList[SN2]
                    for w in List1:
                        for k in List2:
                            EP1=g[w].EndPoint
                            EP1A=EP1[0]
                            EP1B=EP1[1]
                            EP2=g[k].EndPoint
                            EP2A=EP2[0]
                            EP2B=EP2[1]
                            Line1=[[0 for _ in range(2)] for _ in range(2)]
                            Line2=[[0 for _ in range(2)] for _ in range(2)]
                            Line1[0][0]=int(EP1A.split(",", 1)[0])
                            Line1[0][1]=int(EP1A.split(",", 1)[1])
                            Line1[1][0]=int(EP1B.split(",", 1)[0])
                            Line1[1][1]=int(EP1B.split(",", 1)[1])

                            Line2[0][0]=int(EP2A.split(",", 1)[0])
                            Line2[0][1]=int(EP2A.split(",", 1)[1])
                            Line2[1][0]=int(EP2B.split(",", 1)[0])
                            Line2[1][1]=int(EP2B.split(",", 1)[1])

                            try:
                                CPoint=line_intersection(Line1,Line2)
                            except Exception:
                                continue
                            if CPoint:
                                if not g[w].GetIntPoint():
                                    g[w].SetIntPoint(CPoint)
                                else:
                                    for points in g[w].GetIntPoint():
                                        if points == CPoint:
                                            break
                                    else:
                                        g[w].SetIntPoint(CPoint)
                                
                                if not g[k].GetIntPoint():
                                    g[k].SetIntPoint(CPoint)
                                else:
                                    for points in g[k].GetIntPoint():
                                        if points == CPoint:
                                            break
                                    else:
                                        g[k].SetIntPoint(CPoint)
                            else:
                                continue
            # generate vertex graph from class instances
            if not RawVertex:
                i = 1
            else:
                i = len(RawVertex) + 1
            j = 1
            for SN in StreetNameList:
                StreetBranch=StreetList[SN]
                for  SB in StreetBranch:
                    #print (g[SB].StreetName + str(g[SB].Index) + " GetIntPoint " + str(g[SB].GetIntPoint()))
                    if not g[SB].GetIntPoint():
                        #print ("ignored street name:", g[SB].StreetName + str(g[SB].Index))
                        continue
                    else:
                        PointList=[]
                        for endpoints in g[SB].EndPoint:
                            if endpoints in g[SB].GetIntPoint():
                                g[SB].DelIntPoint(endpoints)
                            if endpoints not in RawVertex.values():
                                RawVertex[i] = endpoints
                                PointList.append(i)
                                ResultVertexList[i] = endpoints
                                i += 1
                            else:
                                lKey = [key for key, value in RawVertex.iteritems() if value == endpoints][0]
                                PointList.append(lKey)
                                ResultVertexList[lKey] = endpoints
                        for points in g[SB].GetIntPoint():
                            if points not in RawVertex.values():
                                RawVertex[i] = points
                                PointList.append(i)
                                ResultVertexList[i] = points
                                i += 1
                            else:
                                lKey = [key for key, value in RawVertex.iteritems() if value == points][0]
                                PointList.append(lKey)
                                ResultVertexList[lKey] = points
                        
                        #print (g[SB].StreetName + str(g[SB].Index) + " PointList " + str(PointList))
                        # genertate edge list
                        StartPoint = PointList[0]
                        PointList.remove(StartPoint)
                        while len(PointList) > 0:
                            ShortestDist = float()
                            for EndPoint in range(0,len(PointList)):
                                point1=RawVertex[StartPoint]
                                point2=RawVertex[PointList[EndPoint]]
                                x1=float(point1.split(",", 1)[0])
                                y1=float(point1.split(",", 1)[1])
                                x2=float(point2.split(",", 1)[0])
                                y2=float(point2.split(",", 1)[1])
                                dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                                if not ShortestDist:
                                    ShortestDist = dist
                                    EdgeList[j] = str(StartPoint) + ","+ str(PointList[EndPoint])
                                    NextStartPoint = PointList[EndPoint]
                                elif ShortestDist > dist:
                                    ShortestDist = dist
                                    EdgeList[j] = str(StartPoint) + "," + str(PointList[EndPoint])
                                    NextStartPoint = PointList[EndPoint]
                                else:
                                    continue
                            StartPoint = NextStartPoint
                            PointList.remove(StartPoint)
                            j += 1
            # print result
            print 'V = {'
            for key, value in ResultVertexList.iteritems():
                print (str(key)+": ("+str(value)+")")
            print '}'

            # remove duplicate items for edges
            #for key,value in EdgeList.items():
            #    if value not in ResultEdgeList.values():
            #        ResultEdgeList[key] = value

            for key,value in EdgeList.items():
                valuelist = value.split(",")
                for _,value2 in ResultEdgeList.items():
                    value2list = value2.split(",")
                    if set(value2list) == set(valuelist):
                        break
                else:
                    ResultEdgeList[key] = value

            print 'E = {'
            for key, value in ResultEdgeList.iteritems():
                print ("<"+str(value)+">,")
            print '}'

        elif regexit.match(CmdInput):
            print ("Exit from program.")
            sys.exit(0)
        else:
            print ("Error: Invalid input command " + CmdInput)
        #print 'Finished reading input'
        #RawVertex.clear()
        ResultVertexList.clear()
        EdgeList.clear()
        ResultEdgeList.clear()
        for SN in StreetNameList:
            StreetBranch=StreetList[SN]
            for  SB in StreetBranch:
                #print (g[SB].StreetName + str(g[SB].Index) + " intersection: " + str(g[SB].GetIntPoint()))
                g[SB].IniIntPoint()

    ### YOUR MAIN CODE GOES HERE

def CheckBracket(str):
    if "(" not in str:
        return False
    stack = []
    pushChars, popChars = "<({[", ">)}]"
    for c in str :
      if c in pushChars :
        stack.append(c)
      elif c in popChars :
       if not len(stack) :
            return False
       else :
            stackTop = stack.pop()
            balancingBracket = pushChars[popChars.index(c)]
            if stackTop != balancingBracket :
              return False
    return not len(stack)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')
       #return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff)*1.0 / div
    y = det(d, ydiff)*1.0 / div
    if x.is_integer():
        x = int(x)
    else:
        x = round (x,2)
    if y.is_integer():
        y = int(y)
    else:
        y = round (y,2)

    if not (min(line1[0][0],line1[1][0])<=x<=max(line1[0][0],line1[1][0]) and min(line2[0][0],line2[1][0])<=x<=max(line2[0][0],line2[1][0])):
        raise Exception('lines do not intersect')
    elif not (min(line1[0][1],line1[1][1])<=y<=max(line1[0][1],line1[1][1]) and min(line2[0][1],line2[1][1])<=y<=max(line2[0][1],line2[1][1])):
        raise Exception('lines do not intersect')
    else:
        Point = str(x) + "," + str(y)
        return Point

class Street():
    def __init__(self, StreetName, EndPoint, Index):
        self.StreetName=StreetName
        self.EndPoint=EndPoint
        #self.Line=Line
        self.Index=Index
        self.IntPoint=[]
    def SetIntPoint(self, Point):
        self.IntPoint.append(Point)
    def GetIntPoint(self):
        return self.IntPoint
    def IniIntPoint(self):
        del self.IntPoint[:]
    def DelIntPoint(self, Value):
        self.IntPoint.remove(Value)



if __name__ == '__main__':
    main()