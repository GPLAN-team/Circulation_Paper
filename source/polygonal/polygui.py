import math
import tkinter as tk
import turtle

class PolyGUI:
    def __init__(self,pen,graph_data,rooms):
        self.pen = pen
        self.graph_data = graph_data
        self.noOfNodes = len(self.graph_data['iteration'])
        # self.correctCanonicalOrder = self.graph_data['currentCanonicalOrder'][self.noOfNodes-1]
        self.scale = 0.5*self.noOfNodes/10 #MODIFY SCALE
        self.rooms = rooms
        # self.startDisection()
        
    # def startDisection(self):
        # self.canvas = screen.getcanvas()

        # button = tk.Button(canvas.master, text="Press me", command=press)
        # button.pack()
        
        # canvas.create_window(-200, -200, window=button)
        
        # Test Cases
        # self.hline(0,100,0)
        # self.lshape([-100,0],[100,-200])
        # self.createPentagon()
        # self.createInitalRooms()

        # self.pen.hideturtle()

    def createPentagon(self,coordinatepoints):
        initial_coord = (-200*self.scale,300*self.scale) #IMP this is the initial starting coordinate of the dissection
        self.pen.penup()
        self.pen.goto(initial_coord)
        
        self.pen.pendown()
        for i in range(5):
            CoordA = self.pen.pos()
            coordinatepoints[i+1] = CoordA #this sets the values of the coordinates of the polygon's vertices
            self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units 
            self.pen.right(72) #Turning the turtle by 72 degree

    def createInitalRooms(self,coordinatepoints):
        
        initial_coord = (-150*self.scale,300*self.scale) #now starting the second side 
        self.pen.penup()

        self.pen.goto(initial_coord)
        self.pen.setheading(0)
        coordinatepoints[6] = self.pen.pos()
        self.pen.pendown()
        self.pen.right(108)

        # self.pen.left(72) #Turning the turtle by 72 degree
        self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units 
        coordinatepoints[7] = self.pen.pos()
        self.pen.left(72) #Turning the turtle by 72 degree
        length = 400 - 50*math.cos(math.pi/5) + 50*(math.sin(math.pi/5)/math.tan(2*math.pi/5))
        self.pen.forward(length*self.scale) #Assuming the side of a pentagon is 400 units
        coordinatepoints[8] = self.pen.pos() 
 
 
        initial_coord = (150*self.scale,300*self.scale) #coordinate number 6
        self.pen.penup()
        self.pen.goto(initial_coord)
        self.pen.setheading(0)
        coordinatepoints[9] = self.pen.pos() #the value is stored in the dictionary
        self.pen.pendown()

        self.pen.right(72) #Turning the turtle by 72 degree
        self.pen.forward(400*self.scale) #Assuming the side of a pentagon is 400 units
        coordinatepoints[10] = self.pen.pos()
        self.pen.right(72) #Turning the turtle by 72 degree
        length = 400 - 50*math.cos(math.pi/5) - 25/math.cos(math.pi/5) + 50*(math.sin(math.pi/5)/math.tan(2*math.pi/5))
        print(length)
        self.pen.forward(length*self.scale) #Assuming the side of a pentagon is 400 units
        coordinatepoints[11] = self.pen.pos()
        
         
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
    PolyGUI(pen,{},{})
