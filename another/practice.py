#import matplotlib.pyplot as plt

#a = 'c:/Users/USER/OneDrive/DESKTOP/wait.txt'

#x = []  
#y = []  

#with open(a, 'r') as file:
 #      parts = line.split()   
  #      y.append(int(parts[1])) 
   #     x.append(parts[0])     

#plt.bar(x, y)
#plt.xlabel("Items")
#plt.ylabel("Values")
#plt.title("Visualization")
#plt.show()


#a = 'c:/Users/USER/OneDrive/DESKTOP/wait.txt'

#d = []

#with open(a, 'r') as file:
  #  for line in file:
 #       c = line.strip()
#        c=line.extend(line.split)

#print(c.join())


# import tkinter as tk
# from tkinter import messagebox

# def users():
#     try:
#         # Get user names
#         user_list = [
#             txtfirstuser.get(),  
#             txtseconduser.get(),
#             txtthirduser.get(),
#             txtfourthuser.get(),
#             txtfifthuser.get()
#         ]

#         # Get prices
#         price_list = [
#             int(txtfirstprice.get()),
#             int(txtsecondprice.get()),
#             int(txtthirdprice.get()),
#             int(txtfourthprice.get()),
#             int(txtfifthprice.get())
#         ]
    
#         # Combine into dictionary
#         data = {}
#         for i in range(5):
#             data[user_list[i]] = price_list[i]

#         print(data)
#         messagebox.showinfo("Result", str(data))

#     except ValueError:
#         messagebox.showerror("Error", "Please enter valid numbers for price")

# # ---------------- UI ----------------
# root = tk.Tk()
# root.title("Global Data")

# # First
# tk.Label(root, text="First user:").grid(row=0, column=0)
# txtfirstuser = tk.Entry(root)
# txtfirstuser.grid(row=0, column=1)

# tk.Label(root, text="First price:").grid(row=1, column=0)
# txtfirstprice = tk.Entry(root)
# txtfirstprice.grid(row=1, column=1)

# # Second
# tk.Label(root, text="Second user:").grid(row=2, column=0)
# txtseconduser = tk.Entry(root)
# txtseconduser.grid(row=2, column=1)

# tk.Label(root, text="Second price:").grid(row=3, column=0)
# txtsecondprice = tk.Entry(root)
# txtsecondprice. grid(row=3, column=1)

# # Third
# tk.Label(root, text="Third user:").grid(row=4, column=0)
# txtthirduser = tk.Entry(root)
# txtthirduser(row=4, column=1)

# tk.Label(root, text="Third price:").grid(row=5, column=0)
# txtthirdprice = tk.Entry(root)
# txtthirdprice.grid(row=5, column=1)

# # Fourth
# tk.Label(root, text="Fourth user:").grid(row=6, column=0)
# txtfourthuser = tk.Entry(root)
# txtfourthuser.grid(row=6, column=1)

# tk.Label(root, text="Fourth price:").grid(row=7, column=0)
# txtfourthprice = tk.Entry(root)
# txtfourthprice.grid(row=7, column=1)

# # Fifth
# tk.Label(root, text="Fifth user:").grid(row=8, column=0)
# txtfifthuser = tk.Entry(root)
# txtfifthuser.grid(row=8, column=1)

# tk.Label(root, text="Fifth price:").grid(row=9, column=0)
# txtfifthprice = tk.Entry(root)
# txtfifthprice.grid(row=9, column=1)

# # Button
# tk.Button(root, text="Submit", command=users).grid(row=10, column=0, columnspan=2)

# root.mainloop()

import tkinter as tk
from tkinter import messagebox
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",     # XAMPP default password is empty
    database="userdata"
)

cursor = db.cursor()

# ---------------- FUNCTION ----------------
def users():
    try:
        # Get names
        user_list = [
            txtfirstuser.get(),
            txtseconduser.get(),
            txtthirduser.get(),
            txtfourthuser.get(),
            txtfifthuser.get()
        ]

        # Get prices
        price_list = [
            int(txtfirstprice.get()),
            int(txtsecondprice.get()),
            int(txtthirdprice.get()),
            int(txtfourthprice.get()),
            int(txtfifthprice.get())
        ]

        # Insert into database
        for i in range(5):
            sql = "INSERT INTO users (username, price) VALUES (%s, %s)"
            values = (user_list[i], price_list[i])

            cursor.execute(sql, values)

        db.commit()

        messagebox.showinfo("Success", "Data saved to database")

    except ValueError:
        messagebox.showerror("Error", "Prices must be numbers")

# ---------------- UI ----------------
root = tk.Tk()
root.title("User Database")

# First
tk.Label(root, text="First user").grid(row=0, column=0)
txtfirstuser = tk.Entry(root)
txtfirstuser.grid(row=0, column=1)

tk.Label(root, text="First price").grid(row=1, column=0)
txtfirstprice = tk.Entry(root)
txtfirstprice.grid(row=1, column=1)

# Second
tk.Label(root, text="Second user").grid(row=2, column=0)
txtseconduser = tk.Entry(root)
txtseconduser.grid(row=2, column=1)

tk.Label(root, text="Second price").grid(row=3, column=0)
txtsecondprice = tk.Entry(root)
txtsecondprice.grid(row=3, column=1)

# Third
tk.Label(root, text="Third user").grid(row=4, column=0)
txtthirduser = tk.Entry(root)
txtthirduser.grid(row=4, column=1)

tk.Label(root, text="Third price").grid(row=5, column=0)
txtthirdprice = tk.Entry(root)
txtthirdprice.grid(row=5, column=1)

# Fourth
tk.Label(root, text="Fourth user").grid(row=6, column=0)
txtfourthuser = tk.Entry(root)
txtfourthuser.grid(row=6, column=1)

tk.Label(root, text="Fourth price").grid(row=7, column=0)
txtfourthprice = tk.Entry(root)
txtfourthprice.grid(row=7, column=1)

# Fifth
tk.Label(root, text="Fifth user").grid(row=8, column=0)
txtfifthuser = tk.Entry(root)
txtfifthuser.grid(row=8, column=1)

tk.Label(root, text="Fifth price").grid(row=9, column=0)
txtfifthprice = tk.Entry(root)
txtfifthprice.grid(row=9, column=1)

# Button
tk.Button(root, text="Submit", command=users).grid(row=10, column=0, columnspan=2)

root.mainloop()