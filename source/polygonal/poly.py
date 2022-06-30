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

    def __init__(self,pen):
        self.pen = pen
        self.scale = 0.3
        rootnode = treenode(None, None, None, None) 
        self.displayTurtle()

    def displayTurtle(self):
#  UNCOMMENT TO WORK INDIVIDUALLY
        # top = tk.Tk()   
        # self.c = tk.Canvas(top,bg = "white",height = "800",width= "800")  
        # self.c.pack(side=tk.LEFT)
        # screen = turtle.TurtleScreen(self.c)
        # self.pen = turtle.RawTurtle(screen)
# 
        # self.canvas = screen.getcanvas()

        # button = tk.Button(canvas.master, text="Press me", command=press)
        # button.pack()
        

        # canvas.create_window(-200, -200, window=button)
        
        # Test Cases
        # self.hline(0,100,0)
        # self.lshape([-100,0],[100,-200])
        self.createPentagon()
        self.createInitalRooms()

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
        
    
# def do_stuff():
#     for color in ["red", "yellow", "green"]:
#         my_lovely_turtle.color(color)
#         my_lovely_turtle.right(120)


# def press():
#     do_stuff()


if __name__ == '__main__':
   dissected()
