#import time

#minutes = int(input("Enter number: "))

#while minutes > 0:
 #   if minutes == 3:
  #      print("Warning: time is almost up")

   # print("Time left:", minutes)
    #time.sleep(1)   # wait 1 second
    #minutes -= 1

#print("Stop")

#try:
 #   a = int(input("Enter value: "))
  #  b = 10/a
   # print(b)

#except ZeroDivisionError:
 #   print("0 is not allowed")

#except ValueError:
 #   print("Invalid input! Please enter a number.")
 
#except Exception:
 #   print("something went wrong")
#import os
#print(os.path.exists("c:/Users/USER/OneDrive/DESKTOP/stop.png"))

#a=[1,2,3,4,5,6]
#b=a[0] , a[3]
#print(*b)

#a=[1,2,3,4,5,6]
#for b in a:
  #  a[2]
 #   b=a[2]
#print (b)
#a=[1,2,3,4,5]
#b=(a[2],a[3])
#print(*b)
#a=[1,2,3,4,5]
#a[:4]
#print(*a[:4])
#a=[1,2,3,4,5]
#a[2::]
#a=[1,2,3,4,5]
#a[2:]
#print(*a[2:])




#n=["bola","ahmed","dele","richard"]
#v=[0],n[2]
#print (*v)

#n=["bola","ahmed","dele","richard"]
#for b in n:
  # n[2]
   #b=n[2]
#print(*b)

#n=["bola","ahmed","dele","richard"]
#b=n[1] ,n[3]
#print(*b)

#n=["bola","ahmed","dele","richard"]
#n[:2]
#print(*n[:2])

#n=["bola","ahmed","dele","richard"]
#n[2:]
#print(*n[2:])

#n = ["bola","ahmed","dele","richard"]
#n[::]
#print(*n[::])

#n = ["bola","ahmed","dele","richard"]
#n[2::]
#print(*n[2::])

#n = ["bola","ahmed","dele","richard"]
#n[::2]
#print(*n[::2])
#names = []
#prices = []
#a = {}

#for i in range(5):
  #  item = input("Enter item: ")
   # price = int(input("Enter the price: "))
    
    #names.append(item)
    #prices.append(price)
    #a[item] = price  

#print(a)

import tkinter as tk
from tkinter import messagebox

# FUNCTION
def add_sale():

    try:

        item = txtitem.get()
        price = int(txtprice.get())
        quantity = int(txtquantity.get())

        total = price * quantity

        sales_list.insert(
            tk.END,
            f"{item}  |  Qty:{quantity}  |  ₦{total}"
        )

        lbltotal.config(text=f"Last Sale: ₦{total}")

        txtitem.delete(0, tk.END)
        txtprice.delete(0, tk.END)
        txtquantity.delete(0, tk.END)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Enter numbers only in price and quantity"
        )

# WINDOW
root = tk.Tk()
root.title("Supermarket Sales")
root.geometry("500x500")

# TITLE
title = tk.Label(
    root,
    text="SUPERMARKET SALES SYSTEM",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

# ITEM
tk.Label(root, text="Item Name").pack()

txtitem = tk.Entry(root, width=30, font=("Arial", 12))
txtitem.pack(pady=5)

# PRICE
tk.Label(root, text="Price").pack()

txtprice = tk.Entry(root, width=30, font=("Arial", 12))
txtprice.pack(pady=5)

# QUANTITY
tk.Label(root, text="Quantity").pack()

txtquantity = tk.Entry(root, width=30, font=("Arial", 12))
txtquantity.pack(pady=5)

# BUTTON
btnsale = tk.Button(
    root,
    text="Add Sale",
    font=( "Arial", 13, "bold"),
    bg="green",
    fg="white",
    command=add_sale
)

btnsale.pack(pady=10)

# TOTAL
lbltotal = tk.Label(
    root,
    text="Last Sale: ₦0",
    font=("Arial", 10, "bold"),
    fg="green"
)

lbltotal.pack(pady=10)

# SALES LIST
sales_list = tk.Listbox(
    root,
    width=60,
    height=12,
    font=("Arial", 17)
)

sales_list.pack(pady=10)

# START
root.mainloop()