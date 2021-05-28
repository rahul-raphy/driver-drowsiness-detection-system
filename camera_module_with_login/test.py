from tkinter import *
from forms import *
root = Tk()
width = 650
height = 400
root.geometry(str(width) + "x" + str(height)) 
# root.resizable(False, False)
frame = Frame(root)
# frame2 = Frame(root, width=150, height = 400, background="#b22222")

video = LoginFrame(frame,width,height)
# button = ButtonFrame(frame2,15)

frame.grid(row=0,column=0)

root.mainloop()