import math
from ssl import create_default_context
import tkinter as tk
import turtle 

class Room:
    def __init__(self):
        self.coords = []
        self.leftDisecDone = False
        self.rightDisecDone = False
        self.disecAllowed = True
        self.noOfSides = 0


class treenode:
    def __init__(self, roomNo, parent, left, right):
        self.roomNo = roomNo
        self.parent = parent
        self.left = left
        self.right = right
        self.nofOfSides = 0
        self.listOfCorners = []

class dissected:

    def __init__(self,graph_data,pen):
        self.pen = pen
        self.rootnode = treenode(None, None, None, None) 
        self.graph_data = graph_data
        self.noOfNodes = len(self.graph_data['iteration'])
        self.scale = 0.5*self.noOfNodes/10
        self.correctCanonicalOrder = self.graph_data['currentCanonicalOrder'][self.noOfNodes-1]
        self.activeFront = {'vertex': [] , 'v1': [] , 'v2' : []} #this might not be the active front, why are we even storing this
        self.coordinatepoints  = {} #This is the dictionary which will hold the initial coordinates of the figure when they are being constructed
        self.rooms = []  #this is the list of the rooms data structure, please please please remember!
        self.outerPath = [0,2,1] #this stores the path of the outer surface -> used for finding the leftmost and righnmost neighbors in the canonical order 
        self.side_data = {}
        self.startDisection()
        
    def startDisection(self):
        print(400*self.scale*(1))
        print(400*self.scale*(0.5/math.tan(36*math.pi/180)))
        print(400*self.scale*(0.5/math.sin(36*math.pi/180)))

        print(400*self.scale*(1-0.5/math.tan(36*math.pi/180)-0.5/math.sin(36*math.pi/180)))
        self.side_data[0] = {'leftedges': [((-200*self.scale,300*self.scale),(0,self.scale*(300-400*0.5/math.tan(36*math.pi/180)-400*0.5/math.sin(36*math.pi/180))))], 'rightedges': [((-150*self.scale,300*self.scale),(0,self.scale*(300-400*0.5/math.tan(36*math.pi/180)-400*0.5/math.sin(36*math.pi/180))))], 'rightLateralLength': 0.0, 'leftLateralLength': 0.0}
        self.side_data[1] = {'leftedges': [((-150*self.scale,300*self.scale),(0,self.scale*(300-400*0.5/math.tan(36*math.pi/180)-400*0.5/math.sin(36*math.pi/180))))], 'rightedges': [((+200*self.scale,300*self.scale),(0,self.scale*(300-400*0.5/math.tan(36*math.pi/180)-400*0.5/math.sin(36*math.pi/180))))], 'rightLateralLength': 0.0, 'leftLateralLength': 0.0}
        self.setRightLateralLength(0)
        self.setRightLateralLength(1)
        self.setLeftLateralLength(0)
        self.setLeftLateralLength(1)

        # self.canvas = screen.getcanvas()

        # button = tk.Button(canvas.master, text="Press me", command=press)
        # button.pack()
        

        # canvas.create_window(-200, -200, window=button)
        
        # Test Cases
        # self.hline(0,100,0)
        # self.lshape([-100,0],[100,-200])
        self.createPentagon()
        self.createInitalRooms()
        self.activeFront['vertex'].append(2)
        self.activeFront['v1'].append([-150*self.scale,300*self.scale])
        self.activeFront['v2'].append([150*self.scale,300*self.scale])


        for i in range(self.noOfNodes-4,self.noOfNodes-5,-1): #make -1
            print(self.graph_data['iteration'][i+2])
            temp = self.graph_data['neighbors'][i] 
            neighbors = []
            for j in range(len(temp)):
                if(self.correctCanonicalOrder[temp[j]]<self.noOfNodes - i -1):
                    neighbors.append(self.correctCanonicalOrder[temp[j]])
            print(neighbors)
            if(len(neighbors)==2):
                self.degreeis2(neighbors,i)
            else:
                self.degreenot2(neighbors,i)

        self.pen.hideturtle()

        # top.mainloop()

    def createPentagon(self):
        initial_coord = (-200*self.scale,300*self.scale) #IMP this is the initial starting coordinate of the dissection
        self.pen.penup()
        self.pen.goto(initial_coord)
        
        self.pen.pendown()
        for i in range(5):
            CoordA = self.pen.pos()
            self.coordinatepoints[i+1] = CoordA #this sets the values of the coordinates of the polygon's vertices
            self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units 
            self.pen.right(72) #Turning the turtle by 72 degree

    def createInitalRooms(self):
        
        initial_coord = (-150*self.scale,300*self.scale) #now starting the second side 
        self.pen.penup()
        self.pen.goto(initial_coord)
        self.coordinatepoints[6] = self.pen.pos()
        self.pen.pendown()
        self.pen.left(144)

        self.pen.left(72) #Turning the turtle by 72 degree
        self.pen.backward(400*self.scale) #Assuming the side of a pentagon is 400 units 
        self.coordinatepoints[7] = self.pen.pos()
        self.pen.left(72) #Turning the turtle by 72 degree
        length = 400 - 50*math.cos(math.pi/5) + 50*(math.sin(math.pi/5)/math.tan(2*math.pi/5))
        self.pen.backward(length*self.scale) #Assuming the side of a pentagon is 400 units
        self.coordinatepoints[8] = self.pen.pos() 
 
        
        
        initial_coord = (150*self.scale,300*self.scale) #coordinate number 6
        self.pen.penup()
        self.pen.goto(initial_coord)
        self.coordinatepoints[9] = self.pen.pos() #the value is stored in the dictionary
        self.pen.pendown()

        self.pen.right(72) #Turning the turtle by 72 degree
        self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units
        self.coordinatepoints[10] = self.pen.pos()
        self.pen.right(72) #Turning the turtle by 72 degree
        length = 400 - 50*math.cos(math.pi/5) - 25*math.sec(math.pi/5) + 50*(math.sin(math.pi/5)/math.tan(2*math.pi/5))
        print(length)
        self.pen.forward(length*self.scale) #Assuming the side of a pentagon is 400 units
        self.coordinatepoints[11] = self.pen.pos()
        
         
               #created the initial rooms and also put their coordinates in the self function
        #now will use these to initialise the rooms in the datastructure which stores the room coordinates
        


    def hline(self, x1, x2 ,height):    #To create Horizontal Line
    #     self.c.create_line(x1,height,x2,height, fill="black", width=3)
        x = (x1, height)
        y = (x2, height)

        self.pen.penup()
        self.pen.goto(x)
        self.pen.pendown()
        self.pen.goto(y)


    def vline(self, y1, y2 ,width): #To create Vertical Line
        # self.c.create_line(width,y1,width,y2, fill="black", width=3)
        x = (width, y1)
        y = (width, y2)

        self.pen.penup()
        self.pen.goto(x)
        self.pen.pendown()
        self.pen.goto(y)

    def lshape(self, top, end): #To create L Shaped Line

        self.vline(top[1],end[1],top[0])
        self.hline(top[0],end[0],end[1])

    def degreeis2(self,neighbors,index):
        firstDissectionVertex = -1
        index = -1
        for i in range(0,len(self.activeFront['vertex'])):
            for j in neighbors:
                if(self.activeFront['vertex'][i] == j):
                    firstDissectionVertex = j
                    index =i
                    break
            if(firstDissectionVertex!=-1):
                break
        self.lshape([(self.activeFront['v1'][index][0]+self.activeFront['v2'][index][0])/2,self.activeFront['v1'][index][1]],[self.findxCoord(index),300*self.scale-self.side_data[0]['leftLateralLength']])
        # print(400*self.scale-self.side_data[0]['leftLateralLength'])



                
        # self.activeFront['vertex'].append(2)
        # self.activeFront['v1'].append((-150*self.scale,300*self.scale))
        # self.activeFront['v2'].append((150*self.scale,300*self.scale))


    def degreenot2(self,neighbors,index):
        print('degree>2')

    def setRightLateralLength(self,index):
        length =0
        for i in range (0,len(self.side_data[index]['rightedges'])):
            length+=(abs(self.side_data[index]['rightedges'][i][0][1]) + abs(self.side_data[index]['rightedges'][i][1][1]))/2
        self.side_data[index]['rightLateralLength'] = length

    def setLeftLateralLength(self,index):
        length =0
        for i in range (0,len(self.side_data[index]['leftedges'])):
            length+=(abs(self.side_data[index]['leftedges'][i][0][1]) + abs(self.side_data[index]['leftedges'][i][1][1]))/2
        self.side_data[index]['leftLateralLength'] = length

    def findxCoord(self,index):
        
        return 10

    def createDefaultDisections(self):
        #first we initialise the rooms 1,2,3, which will always exist
        Room1 = Room()
        Room1.coords.append(self.coordinatepoints[1])
        Room1.coords.append(self.coordinatepoints[6])
        Room1.coords.append(self.coordinatepoints[7])
        Room1.coords.append(self.coordinatepoints[8])
        Room1.coords.append(self.coordinatepoints[4])
        Room1.coords.append(self.coordinatepoints[5])
        Room1.DisecAllowed = False
        self.rooms.append(Room1)
        Room2 = Room()
        Room2.coords.append(self.coordinatepoints[9])
        Room2.coords.append(self.coordinatepoints[2])
        Room2.coords.append(self.coordinatepoints[3])
        Room2.coords.append(self.coordinatepoints[8])
        Room2.coords.append(self.coordinatepoints[11])
        Room2.coords.append(self.coordinatepoints[10])
        Room2.DisecAllowed = False
        self.rooms.append(Room2)
        Room3 = Room()
        Room3.coords.append(self.coordinatepoints[6])
        Room3.coords.append(self.coordinatepoints[9])
        Room3.coords.append(self.coordinatepoints[10])
        Room3.coords.append(self.coordinatepoints[11])
        Room3.coords.append(self.coordinatepoints[7])
        self.rooms.append(Room3)
    
    def mainDisectionFunction(self):
        self.createDefaultDisections()
        #now 0,1,2 are already made, we need to make the rooms for all the others from 3 to n-1 
        #this function is responsible for determining the coordinates and storing with each disection of each room!
        
        for i in range(3, self.noOfNodes, 1):
            #determine the number of neighbors of i-> to determine which operation to perform 
            neighborNum = len(self.graph_data['neighbor'][i])
            neighborListIndex = self.graph_data['neighbor'][i] #consists of indexes in original input Graph
            neighborListCanOrd = [] 
            indexInPathArray = []                            #consists of the indexes of the neighbors in the canonically ordered graph
            for j in neighborListIndex:
                neighborListCanOrd.append(self.correctCanonicalOrder[j])
            #now we have to update the path from 1 to 2 as well, to be used in other iterations
            for j in neighborListCanOrd:
                indexInPathArray.append(self.outerPath.index(j))

            l = min(indexInPathArray)
            r = max(indexInPathArray)            
            newPath =[]
            for j in range(0,l+1,1):
                newPath.append(self.outerPath[j])
            self.outerPath.append(i)
            for j in range(r,len(self.outerPath),1):
                newPath.append(self.outerPath[j])
            
            leftCanOrd = self.outerPath[l]
            rightCanOrd = self.outerPath[r]
            self.outerPath = newPath

            if neighborNum == 2:
                print("Vertex {} has 2 neighbors.".format(i))
                # now since we know it has 2 neighbors, we need to make a disection in either of the two
                # before that we need to determine which neighbor is present on the left and which on the right
                # Important to our logic!
                # Remember, the first two
            
                Room0 = self.rooms[neighborListCanOrd[0]] 
                Room1 = self.rooms[neighborListCanOrd[1]] 
                Room0Active0 = Room0.coords[0]
                Room0Active1 = Room0.coords[1]
                Room1Active0 = Room1.coords[0]
                Room1Active1 = Room1.coords[1]
                if(Room0Active1 == Room1Active0):
                    leftRoom = Room0
                    rightRoom = Room1
                else:
                    leftRoom = Room1
                    rightRoom = Room0
                
                #now we have determined the left and the right room and we will now go to do the dissection on the basis of the conditions
                #now we can do 2 things : either do a right dissection in left room or do a left dissection in right room
                # we will decide which to do in the following if statement

                if (leftRoom.disecAllowed==True and leftRoom.rightDisecDone == False):
                    print("The dissection will be done in the left room.")
                    activeFront0 = leftRoom.coords[0]
                    activeFront1 = leftRoom.coords[1]
                    newActivePoint = ((activeFront0[0]+activeFront1[0])/2,activeFront0[1])
                    #now we will determine the y coordinate - slightly complicated process
                    initYCoord = activeFront0[1]
                    first0  = initYCoord
                    first1 = initYCoord
                    last = initYCoord
                    for j in range(1,len(leftRoom.coords),1):
                        last = leftRoom.coords[j][1]
                        if(last>=first0):
                            break
                        else:
                            first0 = last
                    
                    for j in range(len(rightRoom.coords)-1,0, -1):
                        last = rightRoom.coords[j][1]
                        if(last>=first1):
                            break
                        else:
                            first1 = last
                    finalYCoord = max(first0, first1)
                    newYCoord = (initYCoord+finalYCoord)/2

                    newCoordtoConsider = 1; 
                    for j in range(1,len(leftRoom.coords),1):
                        if(leftRoom.coords[j][1]<newYCoord):
                            newCoordtoConsider = j
                            break
                    newPointXCoord = ((leftRoom.coords[newCoordtoConsider][0]- leftRoom.coords[newCoordtoConsider-1][0])/(leftRoom.coords[newCoordtoConsider][1]- leftRoom.coords[newCoordtoConsider-1][1]))(newYCoord - leftRoom.coords[newCoordtoConsider][1]) + leftRoom.coords[newCoordtoConsider][0]
                    Point1 = (newActivePoint[0], newYCoord)
                    Point2 = (newPointXCoord, newYCoord)
                    newcoordList=[]
                    newcoordList.append(activeFront0)
                    newcoordList.append(newActivePoint)
                    newcoordList.append(Point1)
                    newcoordList.append(Point2)
                    for j in range(newCoordtoConsider,len(leftRoom.coords),1):
                        newcoordList.append(leftRoom.coords[j])
                    #Making and apending new room
                    newRoom = Room()
                    newRoom.coords.append(newActivePoint)
                    for j in range(1,newCoordtoConsider,1):
                        newRoom.coords.append(leftRoom.coords[j])
                    newRoom.coords.append(Point2)
                    newRoom.coords.append(Point1)
                    self.rooms.append(newRoom)
                    leftRoom.coords = newcoordList
                    leftRoom.rightDisecDone = True
                    
                else:
                    #we will do the left dissection of the right room 
                    print("The dissection will be done in the right room.")
                    activeFront0 = rightRoom.coords[0]
                    activeFront1 = rightRoom.coords[1]
                    newActivePoint = ((activeFront0[0]+activeFront1[0])/2,activeFront0[1])
                    #now we will determine the y coordinate - slightly complicated process
                    initYCoord = activeFront0[1]
                    first0  = initYCoord #least y coordinate of left room
                    first1 = initYCoord #least y coordinate of right room
                    last = initYCoord
                    for j in range(1,len(leftRoom.coords),1):
                        last = leftRoom.coords[j][1]
                        if(last>=first0):
                            break
                        else:
                            first0 = last
                    
                    for j in range(len(rightRoom.coords)-1,-1, -1):
                        last = rightRoom.coords[j][1]
                        if(last>=first1):
                            break
                        else:
                            first1 = last
                    finalYCoord = max(first0, first1)
                    newYCoord = (initYCoord+finalYCoord)/2

                    newCoordtoConsider = len(rightRoom.coords)-1; 
                    for j in range(len(rightRoom.coords)-1,-1, -1):
                        if(rightRoom.coords[j][1]<newYCoord):
                            newCoordtoConsider = j
                            break
                    
                    newPointXCoord = ((rightRoom.coords[newCoordtoConsider][0]- rightRoom.coords[newCoordtoConsider+1][0])/(rightRoom.coords[newCoordtoConsider][1]- rightRoom.coords[newCoordtoConsider+1][1]))(newYCoord - rightRoom.coords[newCoordtoConsider][1]) + rightRoom.coords[newCoordtoConsider][0]
                    Point1 = (newActivePoint[0], newYCoord)
                    Point2 = (newPointXCoord, newYCoord)
                    newcoordList=[]
                    newcoordList.append(newActivePoint)
                    newcoordList.append(activeFront1)
                    
                    for j in range(2,newCoordtoConsider+1,1):
                        newcoordList.append(rightRoom.coords[j])
                    newcoordList.append(Point2)
                    newcoordList.append(Point1)
                    
                    #Making and apending new room
                    newRoom = Room()
                    newRoom.coords.append(activeFront0)
                    newRoom.coords.append(newActivePoint)
                    newRoom.coords.append(Point1)
                    newRoom.coords.append(Point2)
                    for j in range(newCoordtoConsider+1,len(rightRoom.coords),1 ):
                        newRoom.coords.append(rightRoom.coords[j])
                    self.rooms.append(newRoom)
                    rightRoom.coords = newcoordList
                    rightRoom.leftDisecDone = True
                                
            else:
                print("Vertex {} has {} neighbors".format(i,neighborNum))
                # just need to find the new y coordinate and we will be done with this work
                
                upperY = self.rooms[leftCanOrd].coords[0][1]
                lowerY = float('-inf')
                for j in neighborListCanOrd:
                    
                    last = upperY
                    for k in range(1,len(self.rooms[j].coords),1):
                        if(self.rooms[j].coords[k][1]>= last):
                            break
                        else:
                            last = self.rooms[j].coords[k][1]
                    lowerY = max(lowerY, last)

                newYCoord = (upperY+lowerY)/2
                for j in neighborListCanOrd:
                    if(j != leftCanOrd and j!= rightCanOrd):

                        newCoordtoConsider1 = 0    
                        for k in range(1, len(self.rooms[j].coords),1):
                            if(self.rooms[j].coords[k][1]<newYCoord):
                                newCoordtoConsider1 = k
                                break
                        
                        newXCoordright = ((self.rooms[j].coords[newCoordtoConsider1][0]- self.rooms[j].coords[newCoordtoConsider1-1][0])/(self.rooms[j].coords[newCoordtoConsider1][1]- self.rooms[j].coords[newCoordtoConsider1-1][1]))(newYCoord - self.rooms[j].coords[newCoordtoConsider1][1]) + self.rooms[j].coords[newCoordtoConsider1][0]

                        for k in range(len(self.rooms[j].coords)-1, -1,-1):
                            if(self.rooms[j].coords[k][1]<newYCoord):
                                newCoordtoConsider2 = k
                                break
                        newXCoordleft = ((self.rooms[j].coords[newCoordtoConsider2][0]- self.rooms[j].coords[newCoordtoConsider2+1][0])/(self.rooms[j].coords[newCoordtoConsider2][1]- self.rooms[j].coords[newCoordtoConsider2+1][1]))(newYCoord - self.rooms[j].coords[newCoordtoConsider2][1]) + self.rooms[j].coords[newCoordtoConsider2][0]
            
                        newcoordlist = []
                        newcoordlist.append((newXCoordleft, newYCoord))
                        newcoordlist.append((newXCoordright, newYCoord))
                        for k in (newCoordtoConsider1, newCoordtoConsider2+1, 1) :
                            newcoordlist.append(self.rooms[j].coords[k])
                        self.rooms[j].coords = newcoordlist
                
                newRoom = Room()
                leftTop = self.rooms[leftCanOrd].coords[1]
                rightTop = self.rooms[rightCanOrd].coords[0]
                newRoom.coords.append(leftTop)
                newRoom.coords.append(rightTop)

                newCoordtoConsider1 = 0
                for j in range(len(self.rooms[rightCanOrd].coords)-1,0,-1 ):
                    if(self.rooms[rightCanOrd].coords[j][1]<newYCoord):
                        newCoordtoConsider1 = j
                        break

                newCoordtoConsider2 = 0
                for j in range(1, len(self.rooms[leftCanOrd].coords)-1,1 ):
                    if(self.rooms[leftCanOrd].coords[j][1]<newYCoord):
                        newCoordtoConsider2 = j
                        break
        
                
                #make changes as discussed 
                rightBotX = ((self.rooms[rightCanOrd].coords[newCoordtoConsider1][0]- self.rooms[rightCanOrd].coords[newCoordtoConsider1+1][0])/(self.rooms[rightCanOrd].coords[newCoordtoConsider1][1]- self.rooms[rightCanOrd].coords[newCoordtoConsider1+1][1]))(newYCoord - self.rooms[rightCanOrd].coords[newCoordtoConsider1][1]) + self.rooms[rightCanOrd].coords[newCoordtoConsider1][0]
                leftBotX = ((self.rooms[leftCanOrd].coords[newCoordtoConsider2][0]- self.rooms[leftCanOrd].coords[newCoordtoConsider2-1][0])/(self.rooms[leftCanOrd].coords[newCoordtoConsider2][1]- self.rooms[leftCanOrd].coords[newCoordtoConsider2-1][1]))(newYCoord - self.rooms[leftCanOrd].coords[newCoordtoConsider2][1]) + self.rooms[leftCanOrd].coords[newCoordtoConsider2][0]
                rightBot = (rightBotX, newYCoord)
                leftBot = (leftBotX,newYCoord)
                for k in range(len(self.rooms[rightCanOrd].coords)-1,newCoordtoConsider1,-1):
                    newRoom.coords.append(self.rooms[rightCanOrd].coords[k])
                
                newRoom.coords.append(rightBot)
                newRoom.coords.append(leftBot)
        
                for k in range(newCoordtoConsider2-1,1, -1):    
                    newRoom.coords.append(self.rooms[leftCanOrd].coords[k])
                        
                        
                self.rooms.append(newRoom)
                
















        
    
# def do_stuff():
#     for color in ["red", "yellow", "green"]:
#         my_lovely_turtle.color(color)
#         my_lovely_turtle.right(120)


# def press():
#     do_stuff()





if __name__ == '__main__':
    top = tk.Tk()   
    c = tk.Canvas(top,bg = "white",height = "800",width= "800")  
    c.pack(side=tk.LEFT)
    screen = turtle.TurtleScreen(c)
    pen = turtle.RawTurtle(screen)
    dissected({},pen)
