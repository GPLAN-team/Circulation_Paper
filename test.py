# import networkx as nx
# import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *

# import package and making objects
import turtle


a = {0: [1,2], 1: [4,3], 2: [6,7]}

for x in list(a.keys()):
    y = a[x]
    a[x] = sorted(y)

print(a)

# sc=turtle.Screen()
# trtl=turtle.Turtle()

# # method to draw y-axis lines
# def drawy(val):
	
# 	# line
# 	trtl.forward(300)
	
# 	# set position
# 	trtl.up()
# 	trtl.setpos(val,300)
# 	trtl.down()
	
# 	# another line
# 	trtl.backward(300)
	
# 	# set position again
# 	trtl.up()
# 	trtl.setpos(val+10,0)
# 	trtl.down()
	
# # method to draw y-axis lines
# def drawx(val):
	
# 	# line
# 	trtl.forward(300)
	
# 	# set position
# 	trtl.up()
# 	trtl.setpos(300,val)
# 	trtl.down()
	
# 	# another line
# 	trtl.backward(300)
	
# 	# set position again
# 	trtl.up()
# 	trtl.setpos(0,val+10)
# 	trtl.down()
	
# # method to label the graph grid
# def lab():
	
# 	# set position
# 	trtl.penup()
# 	trtl.setpos(155,155)
# 	trtl.pendown()
	
# 	# write 0
# 	trtl.write(0,font=("Verdana", 12, "bold"))
	
# 	# set position again
# 	trtl.penup()
# 	trtl.setpos(290,155)
# 	trtl.pendown()
	
# 	# write x
# 	trtl.write("x",font=("Verdana", 12, "bold"))
	
# 	# set position again
# 	trtl.penup()
# 	trtl.setpos(155,290)
# 	trtl.pendown()
	
# 	# write y
# 	trtl.write("y",font=("Verdana", 12, "bold"))
	

# # Main Section
# # set screen
# sc.setup(800,800)

# # set turtle features
# trtl.speed(100)
# trtl.left(90)
# trtl.color('lightgreen')

# # y lines
# for i in range(30):
# 	drawy(10*(i+1))

# # set position for x lines
# trtl.right(90)
# trtl.up()
# trtl.setpos(0,0)
# trtl.down()

# # x lines
# for i in range(30):
# 	drawx(10*(i+1))

# # axis
# trtl.color('green')

# # set position for x axis
# trtl.up()
# trtl.setpos(0,150)
# trtl.down()

# # x-axis
# # trtl.forward(300)

# # set position for y axis
# trtl.left(90)
# trtl.up()
# trtl.setpos(150,0)
# trtl.down()

# # y-axis
# # trtl.forward(300)

# # labeling
# # lab()

# # hide the turtle
# trtl.hideturtle()

"""Sample code for scrollbar """
# root = Tk()
# root.title("Test GUI GPLAN")
# root.geometry("500x400")

# # Create a Main Frame
# main_frame = Frame(root)
# main_frame.pack(fill=BOTH, expand=1)

# # Create Canvas
# my_canvas = Canvas(main_frame)
# my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

# # Add Scrollbar to the canvas
# my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
# my_scrollbar.pack(side=RIGHT, fill=Y)

# # Configure the canvas
# my_canvas.configure(yscrollcommand=my_scrollbar.set)
# my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# # Create another frame inside the canvas
# second_frame = Frame(my_canvas)

# # Add that new frame to a window in the canvas
# my_canvas.create_window((0,0), window=second_frame, anchor="nw")

# corr_text = tk.Label(second_frame,text="Enter 1 if you want to remove corridor",justify=tk.CENTER).grid(row=1, column=2)
# for i in range(50):
#     Button(second_frame, text=f'Button {i}').grid(row=i, column=0, padx=10, pady=10)

# root.mainloop()

""" Sample code to use dropdowns """
# OZoneIzotopeSemiWhite = "#c0c4ca"
# buttonBackground = "#303336"
# buttonforeground = "#cdd0d7"
# BACKGROUND2 = "#1e1f21"

# class DropDownButton():
#     def __init__(self, parent, placement, opTions, **kw):
#         self.parent = parent
#         self.options = opTions

#         self.om_variable = tk.StringVar(self.parent)
#         self.om_variable.set(self.options[0])
#         self.om_variable.trace('w', self.option_select)

#         self.om = tk.OptionMenu(self.parent, self.om_variable, *self.options)
#         self.om["menu"].config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, borderwidth = 0)
#         self.om.config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, bd =0)
#         self.om.place(x = placement, y = 2)
#         self.om.bind("<Enter>", self.on_enter)
#         self.om.bind("<Leave>", self.on_leave)

#         self.om_variable1 = tk.StringVar(self.parent)
#         self.om_variable1.set(self.options[0])
#         self.om_variable1.trace('w', self.option_select1)

#         self.om1 = tk.OptionMenu(self.parent, self.om_variable1, *self.options)
#         self.om1["menu"].config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, borderwidth = 0)
#         self.om1.config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, bd =0)
#         self.om1.place(x = placement, y = 2)
#         self.om1.bind("<Enter>", self.on_enter1)
#         self.om1.bind("<Leave>", self.on_leave1)

#     def on_enter(self, event):
#         if self.om == self.options[0]:
#             print ("Floorplan generation")
#         elif self.om_variable.get() == self.options[1]:
#             print ("Rectangular")
#         else:
#             print("Irregular")

#     def on_leave(self, enter):
#         print ("leave")

#     def option_select(self, *args):
#         print (self.om_variable.get())
    
#     def on_enter1(self, event):
#         if self.om == self.options[0]:
#             print ("Circulation")
#         elif self.om_variable.get() == self.options[1]:
#             print ("Dimensioned")
#         else:
#             print("Add/Remove")

#     def on_leave1(self, enter):
#         print ("leave")

#     def option_select1(self, *args):
#         print (self.om_variable1.get())

# root = tk.Tk()
# DropDownButton(root, 55, ['Floorplan gen', 'Rectangular', 'Irregular'])
# DropDownButton(root, 200, ['Circulation', 'Dimensioned', 'Add/Remove'])
# root.mainloop()
