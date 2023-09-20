from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W,E,N,S, END
from tkinter import ttk
from tkinter import messagebox
from sqlserver_config import dbConfig
import pypyodbc as pyo 

conn = pyo.connect(**dbConfig)
print(conn) 

class Bookdb:
    def __init__(self) :
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("You have established a connection ...")
        print(self.con)

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows
    
    def insert(self,title,author,isbn):
        sql=("INSERT INTO books (title,author,isbn) VALUES (?,?,?)") 
        values = [ title,author,isbn]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="New book added to the Book Table of mybooks DATABASE")
   
    def update(self,id, title,author,isbn):
        update_sql=("UPDATE books SET title=?, author=?, isbn =? WHERE id =?")
        self.cursor.execute(update_sql, [title, author, isbn, id ])
        self.con.commit()
        messagebox.showinfo(title="mybooks Database", message="Book table updated")
   
    def delete(self,id ):
        delete_sql=("DELETE from books where id =?")
        self.cursor.execute(delete_sql,[id])
        self.con.commit()
        messagebox.showinfo(title="mybooks Database", message=" row deleted ")


def get_selected_row(event):
	global selected_tuple
	index = list_box.curselection()[0]
	selected_tuple = list_box.get(index)
	title_entry.delete(0,'end') # clears the input after inserting
	title_entry.insert('end', selected_tuple[1])
	author_entry.delete(0,'end')
	author_entry.insert('end',selected_tuple[2])
	isbn_entry.delete(0, 'end')
	isbn_entry.insert('end',selected_tuple[3])    

db = Bookdb()  #  Bookdb is the class created to access 

def view_records():
    list_box.delete(0,'end')
    for row in db.view():
        list_box.insert('end',row) 

def add_book():
    db.insert(title_text.get(), author_text.get(), isbn_text.get() )
    list_box.delete(0, 'end')
    list_box.insert ('end',(title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0,'end')
    conn.commit()

def delete_records():
    db.delete(selected_tuple[0])
    conn.commit() 


def clear_screen():
        list_box.delete(0,'end')
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')

def update_records():
        db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')

    
def on_closing():
        dd=db
        if messagebox.askokcancel("Quit","Do you want to quit?"):
            root.destroy()
            del dd


root=Tk() 

root.title("My Books Database Application")
root.configure(background="light green")
#  -- Geometry() method is used to set the dimensions of the tkinter application window. 
root.geometry("850x500") #, width, height,
root.resizable(width=False,height=False)


title_label = ttk.Label(root, text="Title",background="Light green", font=("TkDefaultFont",16))
title_label.grid(row=0, column =0, sticky=W)

title_text= StringVar()
title_entry= ttk.Entry(root, width=24, textvariable=title_text)
title_entry.grid(row=0,column=1,sticky=W)


author_label = ttk.Label(root, text="Author",background="Light green", font=("TkDefaultFont",16))
author_label.grid(row=0, column =2, sticky=W)

author_text= StringVar()
author_entry= ttk.Entry(root, width=24, textvariable=author_text)
author_entry.grid(row=0,column=3,sticky=W)

isbn_label = ttk.Label(root, text="ISBN",background="Light green", font=("TkDefaultFont",16))
isbn_label.grid(row=0, column =4, sticky=W)

isbn_text= StringVar()
isbn_entry= ttk.Entry(root, width=24, textvariable=isbn_text)
isbn_entry.grid(row=0,column=5,sticky=W)

add_btn = Button(root, text="Add Book", bg="blue",fg="white",font="helvetica 10 bold", command=add_book)
add_btn.grid(row=0, column=6, sticky=W) 

list_box = Listbox(root, height=16, width=40, font="helvetica 13", bg="light blue")
list_box.grid(row=3, column=1, columnspan=14, sticky=W + E, pady=40, padx=15) 
list_box.bind('<<ListboxSelect>>',get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)


modifyButton = Button(root, text="Modify Record", bg='purple', fg='white',font='helvetica 10 bold', command=update_records)
modifyButton.grid(row=15, column=4)

deleteButton = Button(root, text="Delete Record", bg='red', fg='white',font='helvetica 10 bold', command=delete_records)
deleteButton.grid(row=15, column=5)

viewButton = Button(root, text="View all Records", bg='black', fg='white',font='helvetica 10 bold', command=view_records)
viewButton.grid(row=15, column=1)

clearButton = Button(root, text="Clear Screen", bg='maroon', fg='white',font='helvetica 10 bold', command=clear_screen)
clearButton.grid(row=15, column=2)

exitButton = Button(root, text="Exit Application", bg='blue', fg='white',font='helvetica 10 bold', command=root.destroy)
exitButton.grid(row=15, column=3)


root.mainloop() 

