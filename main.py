#-*-coding: utf-8-*-
from tkinter import *
from time import sleep, strftime
from winsound import PlaySound, SND_ASYNC
from json import loads, dumps
import operator
PI = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548"

def playsound(file):
	PlaySound(file, SND_ASYNC)

class Pier:
	def __init__(self, pi, root, feed, counter):
		self.pi = pi
		self.feed = feed
		self.pindex = 0
		self.fontsize = 20
		self.root = root
		self.counter = counter
		self.counter["text"] = "Counter: {}".format(self.pindex)
		self.record, self.ranking= self.get_record()


	def load_rank(self, file):
		try:
			with open(file, "r") as f:
				content = loads(f.read())
		except:
			content = {}
		
		finally:
			return content

	def get_record(self):
		with open("source\\ranking.json", "r") as f:
			content = loads(f.read())
		if len(content) == 0:
			record = 0
		else:
			record = max(content, key=operator.itemgetter(-1))

		return (record, content)

	def update_raning(self):
		self.ranking[strftime("%D - %H:%M:%S")] = self.pindex
		with open("source\\ranking.json", "w") as f:
			f.write(dumps(self.ranking, indent=4))

	def check_rank(self, file="source\\ranking.json"):
		if self.pindex > self.ranking[self.record]:
			self.record = self.pindex
			self.update_ranking()



	def right(self, entry):
		number = entry.get()
		entry.delete(0, 'end')

		if not len(number):
			return 0
		else:
			number = number[0]
			if number == ",":
				number = "."
			elif not number.isnumeric() and number not in [".", ","]:
				return 0
		
		if number == PI[self.pindex]:
			self.pi["text"] = self.pi["text"] + PI[self.pindex]
			self.pindex += 1
			if (self.pindex % 20) == 0:
				self.fontsize -= 1	
				self.pi.config(font = ("Courier",self.fontsize))
			playsound("source\\correct.wav")

			self.pi.config(bg="#66E874")
			self.root.update()
			sleep(0.1)
			self.pi.config(bg="#FF9760")
			
		else:
			self.check_rank()
			self.feed["text"] = "Last number: {}".format(PI[self.pindex])
			self.pindex = 0
			self.pi["text"] = ""
			self.fontsize = 20
			self.pi.config(bg="#FF9760")
			self.pi.config(font=("Courier", self.fontsize))
			playsound("source\\wrong.wav")
			self.pi.config(bg="#FF1C0F")
			self.root.update()
			sleep(0.1)
			self.pi.config(bg="#FF9760")
			
		self.counter["text"] = "Counter: {}".format(self.pindex)

class Write:
	def __init__(self):
		pass

	def check(self, inpt, root):
		text = inpt.get('1.0', 'end-1c').strip()
		inpt.delete('1.0', END)
		inpt.insert(END, text)
		if len(text) > len(PI):
			text = text[:len(PI)]
		if text == PI[0:len(text)]:
			playsound("source\\correct.wav")
			inpt.config(bg="#66E874")
		else:
			playsound("source\\wrong.wav")
			inpt.config(bg="#FF1C0F")
		root.update()
		sleep(0.1)
		inpt.config(bg="white")

		


def write_pi():
	w = Write()
	root = Tk()
	root.geometry("800x450")
	root.title("Pi Game")
	mframe = Frame(root, bg="white")
	mframe.place(relx=0, rely=0, relwidth=1, relheight=1)
	title = Label(mframe, text="Write Pi", font="Helvetica 18 bold", bg="white", fg="black")
	title.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.1)
	inpt = Text(mframe, bg="white", fg="black", font="Helvetica 14",  borderwidth=2, relief="solid")
	inpt.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.4)
	root.bind("<Return>", lambda *args, **kwargs: w.check(inpt, root))
	check = Button(mframe, bg="#FF9760", fg="black", text="Check!", font="Helvetica 16 bold", command=lambda:w.check(inpt, root))
	check.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)
	root.mainloop()

def ask_pi():
	root = Tk()
	root.geometry("800x450")
	root.title("Pi Game")
	mframe = Frame(root, bg="white")
	mframe.place(relx=0, rely=0, relwidth=1, relheight=1)
	title = Label(mframe, bg="white", font='Helvetica 18 bold', fg="black", text="Memorize PI")
	title.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.1)
	pi = Label(mframe, bg="#FF9760", font=("Courier", 11), text="")
	pi.place(relx=0, rely=0.3, relwidth=1, relheight=0.05)
	feed = Label(mframe, bg="white", font=("Courier", 20), fg="#FF1C0F")
	feed.place(relx=0.35, rely=0.75, relwidth=0.35, relheight=0.1)
	counter = Label(mframe, bg="white", font=("Courier", 20), fg="#FF1C0F")
	counter.place(relx=0.35,rely=0.6, relwidth=0.35, relheight=0.1)
	pier = Pier(pi, root, feed, counter)
	digit = Entry(mframe, borderwidth=2, relief="solid", font=("Courier", 18))
	digit.place(relx=0.35, rely=0.5, relwidth=0.15, relheight=0.1)
	check = Button(mframe, bg="#FF9760", fg="black", font='Helvetica 18',text="Check!", command=lambda:pier.right(digit))
	check.place(relx=0.55, rely=0.5, relwidth=0.15, relheight=0.1)
	root.bind('<Return>', lambda *args,**kargs:pier.right(digit))
	root.mainloop()

class Menu:
	def __init__(self):
		self.closed = False

	def select_mode(self):
		root = Tk()
		root.geometry("800x450")
		root.title("PI")
		root.protocol("WM_DELETE_WINDOW", lambda *args, **kwargs:self.__on_close(root))
		mframe = Frame(root, bg="white")
		mframe.place(relx=0, rely=0, relwidth=1, relheight=1)
		title = Label(mframe, bg="white", font='Helvetica 18 bold', fg="black", text="Main Menu")
		title.place(relx = 0.3, rely=0.1, relwidth=0.4, relheight=0.1)
		blitz = Button(mframe, text="Blitz", bg="#FF9760",font="Helvetica 14 bold", fg="black", command=lambda: self.start(ask_pi, root))
		blitz.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
		write = Button(mframe, text="Write", bg="#FF9760", font="Helvetica 14 bold", fg="black", command=lambda: self.start(write_pi, root))		
		write.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)
		root.mainloop()

	def start(self, mode, root):
		root.destroy()
		mode()


	def __on_close(self, root):
		root.destroy()
		self.closed = True



if __name__ == '__main__':
	main = Menu()
	while not main.closed:
		main.select_mode()
	