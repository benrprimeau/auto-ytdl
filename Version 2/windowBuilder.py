from collectionBuilder import collection
from PIL import Image, ImageTk
from io import BytesIO
import tkinter
import requests


class window:
	def __init__(self, master=tkinter.Tk()):
		self.master = master
		self.master.title("title")

	def grid(self,collection,x,y):
		for i in range(y):
			self.master.rowconfigure(i, weight=1, minsize=75)
			
			for j in range(x):
				self.master.columnconfigure(j, weight=1, minsize=50)
				f = tkinter.Frame()

				if (x*i)+j > collection.getLength()-1:
					imgRef = Image.open("img.png")
					name = "none"


				else:
					imgData = requests.get(collection.getItem((x*i)+j).getImage()).content
					imgRef = Image.open(BytesIO(imgData))
					name = collection.getItem((x*i)+j).getName()

				img = ImageTk.PhotoImage(imgRef)

				l = tkinter.Label(master=f,image=img)
				l2 = tkinter.Label(master=f,text=name)
				l.image = img				
				l.pack()
				l2.pack()

				f.grid(row=i, column=j)


	def run(self):
		self.master.update()
		self.master.minsize(self.master.winfo_width(), self.master.winfo_height())
		self.master.mainloop()