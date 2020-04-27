import tkinter as tk
from tkinter.ttk import Progressbar
from PIL import Image

class App():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Study Checklist')
        self.win.geometry('1080x720')

        self.topFrame = tk.Frame(self.win)
        self.topFrame.pack(side=tk.TOP)

        self.bottomFrame = tk.Frame(self.win)
        self.bottomFrame.pack(side=tk.BOTTOM)

        self.leftFrame = tk.Frame(self.win)
        self.leftFrame.pack(side=tk.LEFT)

        self.rightFrame = tk.Frame(self.win)
        self.rightFrame.pack(side=tk.RIGHT)

    def add_course(self, lbox, course):
        pass


app = App()
logo = tk.PhotoImage(file='data/images/unswlogo.png')
lbllogo = tk.Label(app.win, image=logo)
lbllogo.pack()

tk.Label(app.leftFrame, text='Full Courses', font=('Aerial', 30)).pack()

listcourse = tk.Listbox(app.leftFrame, width=50, height=20)
listcourse.pack()

tk.Label(app.rightFrame, text='Finished Courses', font=('Aerial', 30)).pack()

listfinished = tk.Listbox(app.rightFrame, width=50, height=20)
listfinished.pack()

txtcourse = tk.Entry(app.win, width=50, borderwidth=5, font=('Aerial', 20))
txtcourse.pack()



app.win.mainloop()

