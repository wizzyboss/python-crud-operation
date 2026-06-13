import tkinter as tk
import pymysql
from supabase import create_client

# SUPABASE
supabase = create_client(
    "https://jmhhuprhlzxugtthynzn.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImptaGh1cHJobHp4dWd0dGh5bnpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgzMTM5MTIsImV4cCI6MjA5Mzg4OTkxMn0.4u4hDD7ok0p8wxXla8Rlrugrznfk2E9WM_2dt8a_tX8"
)

# MYSQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="supermarket"
)

cursor = conn.cursor()

# ADD SALE
def add_sale():

    item = item_entry.get()
    price = float(price_entry.get())
    qty = int(qty_entry.get())

    total = price * qty

    # SAVE TO MYSQL
    cursor.execute(
        "INSERT INTO sales(item_name,quantity_sold,total) VALUES(%s,%s,%s)",
        (item, qty, total)
    )

    conn.commit()

    # SAVE TO SUPABASE
    supabase.table("sales").insert({
        "item_name": item,
        "quantity_sold": qty,
        "total": total
    }).execute()

    # SHOW IN LISTBOX
    listbox.insert(
        tk.END,
        f"{item} | Qty:{qty} | ₦{total}"
    )

    # SHOW TOTAL
    total_label.config(text=f"Total: ₦{total}")

    # CLEAR ENTRIES
    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)

# WINDOW
window = tk.Tk()
window.title("Sales System")
window.geometry("600x500")

# TITLE
title = tk.Label(
    window,
    text="SUPERMARKET SALES",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

# ITEM
tk.Label(window, text="Item Name").pack()

item_entry = tk.Entry(window, width=30, font=("Arial", 14))
item_entry.pack()

# PRICE
tk.Label(window, text="Price").pack()

price_entry = tk.Entry(window, width=30, font=("Arial", 14))
price_entry.pack()

# QUANTITY
tk.Label(window, text="Quantity").pack()

qty_entry = tk.Entry(window, width=30, font=("Arial", 14))
qty_entry.pack()

# BUTTON
add_button = tk.Button(
    window,
    text="Add Sale",
    font=("Arial", 14),
    bg="green",
    fg="white",
    command=add_sale
)

add_button.pack(pady=10)

# TOTAL
total_label = tk.Label(
    window,
    text="Total: ₦0",
    font=("Arial", 16, "bold"),
    fg="green"
)

total_label.pack(pady=10)

             # SALES LIST
listbox = tk.Listbox(
    window,
    width=70,
    height=15,
    font=("Arial", 12)
)

listbox.pack(pady=10)

window.mainloop()