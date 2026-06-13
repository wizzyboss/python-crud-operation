from tkinter import*
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

def connection_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="supermarket_db"
    )
def marketkit():
    try:
     id=txtid.get()
     item=txtitem.get()
     price=float(txtprice.get())
    except ValueError:
       #messagebox.showerror("Error","please enter a valid input")
     conn=connection_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM supermarket_table WHERE id=%s", (id,))
    result=cursor.fetchone()
    if result:
     txtitem.delete(0, END)
    txtprice.delete(0, END)

    txtitem.insert(0, result[1])   # item column
    txtprice.insert(0, result[2])  # price column

    messagebox.showinfo("Success", "Data found successfully")
    conn.commit()
    conn.close()
    cursor.close()
root=Tk()
root.title("supermarket")
root.geometry("400x300")
id=Label(root,text="ID",font=("Arial",15))
id.grid(row=0,column=0,padx=10,pady=10)
txtid=Entry(root)
txtid.grid(row=0,column=1,padx=10,pady=10)
item=Label(root,text="Item",font=("Arial",15))
item.grid(row=1,column=0,padx=10,pady=10)
txtitem=Entry(root)
txtitem.grid(row=1,column=1,padx=10,pady=10)
price=Label(root,text="Price",font=("Arial",15))
price.grid(row=2,column=0,padx=10,pady=10)
txtprice=Entry(root)
txtprice.grid(row=2,column=1,padx=10,pady=10)
btn=Button(root,text="Search Market",command= marketkit,bg="blue",fg="white",relief=RAISED,font=("Arial",10))
btn.grid(row=3,column=0,columnspan=2,pady=10)
root.mainloop()