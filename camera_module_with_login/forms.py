from tkinter import *
import cv2
from PIL import ImageTk, Image
from core import *
import winsound
from tkinter import messagebox
import requests

global start
start = False
login_id = None
class LoginFrame(Frame):
	def __init__(self,master,width,height):
		super().__init__(master)
		self.master = master
		self.width = width
		self.height = height
		login_f = Frame(master)
		head = Label(login_f,text="Login",font=("Courier", 20))
		label_username = Label(login_f,text="Username")
		label_password = Label(login_f,text="Password")
		self.entry_username = Entry(login_f)
		self.entry_password = Entry(login_f)
		button_login = Button(login_f,text="Login",command=lambda: self.login_command(login_f))

		head.grid(row=0,column=0,columnspan=2)
		label_username.grid(row=1,column=0)
		label_password.grid(row=2,column=0)
		self.entry_username.grid(row=1,column=1)
		self.entry_password.grid(row=2,column=1)
		button_login.grid(row=3,column=1,sticky=W+E)
		login_f.grid(row=0,column=0)
	def login_command(self,form):
		# print("Clicked")
		username = self.entry_username.get()
		password = self.entry_password.get()
		try:
			obj = requests.get('http://127.0.0.1:5000/api/login/?username=%s&password=%s' % (username,password)).json()
			if obj['status'] == 'success':
				global login_id
				login_id = obj['data'][0]['login_id']
				form.destroy()
				MainFrame(self.master,self.width,self.height)
			else:
				messagebox.showinfo("Failed", "Login failed. Try again")
		except Exception as e:

			messagebox.showinfo("Failed", "Login failed. Try again")
class MainFrame(Frame):
	"""docstring for MainFrame"""
	def __init__(self, master,width,height):
		super().__init__(master)
		self.master = master 
		button_frame = Frame(master,width=int(width/4),height=height,bg="#F00")
		button_frame.pack_propagate(False)
		video_frame = Frame(master,width = (width-int(width/4)),height=height,bg="#CCC")
		video_frame.pack_propagate(False)
		# print(button_frame['width'])
		ButtonFrame(button_frame)
		VideoStream(video_frame)

		button_frame.pack(side=LEFT)
		video_frame.pack(side=LEFT)


class VideoStream(Frame):
	"""docstring for ClassName"""

	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.frame_count = 0
		self.cap = cv2.VideoCapture(0)
		self.lmain = Label(master)
		self.lmain.pack(fill="x")
		self.video_stream()
		master.pack()

	def video_stream(self):
		_, frame = self.cap.read()
		cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		cv2image = cv2.resize(cv2image, (self.master['width'],self.master['height']))
		if start:
			eye_status,distraction = process_frame(cv2image)
			if eye_status == 'closed' or distraction == 'distraction':
				self.frame_count += 1
				if self.frame_count > 10:
					# requests.get('http://127.0.0.1:5000/api/detect_drowssiness/?login_id=' % (login_id))
					frequency = 2500
					winsound.Beep(frequency, 200)
			else:
				self.frame_count  = 0
		img = Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(image=img)
		self.lmain.imgtk = imgtk
		self.lmain.configure(image=imgtk)
		self.lmain.after(1, self.video_stream) 


class ButtonFrame(Frame):
	"""docstring for Button"""
	def __init__(self, master):
		super().__init__(master)
		self.start = Button(master,text="Start",command=self.start_button)
		self.start.pack(fill="x")
		self.stop = Button(master,text="Stop",command=self.stop_button)
		self.stop.pack(fill="x")
		master.pack()
	def start_button(self):
		global start 
		start = True
		print("start" + str(start))
	def stop_button(self):
		global start 
		start = False
		print("start" + str(start))

		