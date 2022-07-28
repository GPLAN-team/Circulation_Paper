import math
import tkinter as tk
import turtle 


class treenode:
    def __init__(self, roomNo, parent, left, right):
        self.roomNo = roomNo;
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
        self.activeFront = {'vertex': [] , 'v1': [] , 'v2' : []}

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
        initial_coord = (-200*self.scale,300*self.scale) #IMP
        self.pen.penup()
        self.pen.goto(initial_coord)
        self.pen.pendown()
        for i in range(5):
            self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units 
            self.pen.right(72) #Turning the turtle by 72 degree

    def createInitalRooms(self):
        initial_coord = (150*self.scale,300*self.scale)
        self.pen.penup()
        self.pen.goto(initial_coord)
        self.pen.pendown()

        self.pen.right(72) #Turning the turtle by 72 degree
        self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units
        self.pen.right(72) #Turning the turtle by 72 degree
        self.pen.forward(337*self.scale) #Assuming the side of a pentagon is 400 units

        
         
        initial_coord = (-150*self.scale,300*self.scale)
        self.pen.penup()
        self.pen.goto(initial_coord)
        self.pen.pendown()
        self.pen.left(144)

        self.pen.left(72) #Turning the turtle by 72 degree
        self.pen.backward(400*self.scale) #Assuming the side of a pentagon is 400 units 
        self.pen.left(72) #Turning the turtle by 72 degree
        self.pen.backward(368*self.scale) #Assuming the side of a pentagon is 400 units 
        


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
