import tkinter as tk
from tkinter.ttk import Progressbar
from PIL import Image
import json


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

    def add_course(self, lbox, course, finish):
        if course == '':
            return
        print(course)
        course = course.lower()
        edited = False

        with open('list.json', 'r+') as fread:
            courses = json.load(fread)

        for index, cinfo in enumerate(courses):
            if course == cinfo[0]:
                courses[index] = (course, finish)
                edited = True
        if not edited:
            courses.append((course, False))
        courses = sorted(courses, key= lambda x: x[0])
        with open('list.json', 'w+') as fwrite:
            json.dump(courses, fwrite)
        self.list_courses(lbox, finish)


    def remove_finished_course(self, lbox, course):
        with open('list.json', 'r+') as fread:
            courses = json.load(fread)
        course = course.lower()
        for index, item in enumerate(courses):
            if course == item[0]:
                courses[index][1] = False
        with open('list.json', 'w') as f:
            json.dump(courses, f)
        self.list_courses(lbox, True)

    def list_courses(self, lbox, finished = False):
        lbox.delete(0, 'end')
        with open('list.json', 'r+') as fread:
            data = json.load(fread)
        for course in data:
            if finished:
                if course[1]:
                    lbox.insert(tk.END, course[0])
            else:
                lbox.insert(tk.END, course[0])

    def list_courses_left(self, lbox):
        lbox.delete(0, 'end')
        with open('list.json', 'r') as f:
            courses = json.load(f)
        for course in courses:
            if not course[1]:
                lbox.insert(tk.END, course[0])

    def update_progess(self, prog):
        with open('list.json', 'r') as f:
            courses = json.load(f)
        
        finished = len(list(filter(lambda x: x[1], courses)))
        total = len(courses)
        prog['value'] = int(finished * 100 / total)

def clear_text(txt):
    txt.delete(0, tk.END)


app = App()
logo = tk.PhotoImage(file='data/images/unswlogo.png')
lbllogo = tk.Label(app.win, image=logo)
lbllogo.pack()

tk.Label(app.leftFrame, text='Full Courses', font=('Aerial', 30)).pack()

listcourse = tk.Listbox(app.leftFrame, width=50, height=20)
listcourse.pack()
app.list_courses(listcourse)

tk.Label(app.rightFrame, text='Finished Courses', font=('Aerial', 30)).pack()

listfinished = tk.Listbox(app.rightFrame, width=50, height=20)
listfinished.pack()
app.list_courses(listfinished, True)

txtcourse = tk.Entry(app.win, width=50, borderwidth=5, font=('Aerial', 20))
txtcourse.pack()

progress = Progressbar(app.win, length=100)
app.update_progess(progress)
progress.pack()

btnaddcourse = tk.Button(app.win, text='Add Course', command= lambda: [app.add_course(listcourse, txtcourse.get(), False), clear_text(txtcourse)])
btnaddcourse.pack()

tk.Label(app.win, text='Courses Left', font=('Aerial', 30)).pack()
listleft = tk.Listbox(app.win, width=50, height=20)
listleft.pack()

app.list_courses_left(listleft)





app.win.bind('<Return>', lambda e: [app.add_course(listcourse, txtcourse.get(), False), clear_text(txtcourse), app.update_progess(progress), app.list_courses_left(listleft)])
listcourse.bind('<Double-1>', lambda e: [app.add_course(listfinished, listcourse.get(listcourse.curselection()[0]), True), app.update_progess(progress), app.list_courses_left(listleft)])
listfinished.bind('<Double-1>', lambda e: [app.remove_finished_course(listfinished, listfinished.get(listfinished.curselection()[0])), app.update_progess(progress), app.list_courses_left(listleft)])
listleft.bind('<Double-1>', lambda e: [app.add_course(listfinished, listleft.get(listleft.curselection()[0]), True), app.update_progess(progress), app.list_courses_left(listleft)])
app.win.mainloop()