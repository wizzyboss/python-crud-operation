import tkinter as tk
from tkinter import messagebox

# FUNCTION
def add_stock():

    try:

        item = txtitem.get()
        amount = int(txtamount.get())
        quantity = int(txtquantity.get())

        total = amount * quantity

        stock_list.insert(
            tk.END,
            f"{item} | Amount: ₦{amount} | Qty: {quantity} | Total: ₦{total}"
        )

        lblstock.config(
            text=f"Stock Added Successfully"
        )

        txtitem.delete(0, tk.END)
        txtamount.delete(0, tk.END)
        txtquantity.delete(0, tk.END)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Enter numbers only"
        )

# WINDOW
root = tk.Tk()
root.title("Stock System")
root.geometry("600x500")

# TITLE
title = tk.Label(
    root,
    text="STOCK IN SYSTEM",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

# ITEM
tk.Label(root, text="Item Name").pack()

txtitem = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)

txtitem.pack(pady=5)

# AMOUNT
tk.Label(root, text="Amount").pack()

txtamount = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)

txtamount.pack(pady=5)

# QUANTITY
tk.Label(root, text="Quantity Added").pack()

txtquantity = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)

txtquantity.pack(pady=5)

# BUTTON
btnstock = tk.Button(
    root,
    text="Add Stock",
    font=("Arial", 12, "bold"),
    bg="blue",
    fg="white",
    command=add_stock
)

btnstock.pack(pady=10)

# LABEL
lblstock = tk.Label(
    root,
    text="No Stock Added",
    font=("Arial", 14, "bold"),
    fg="blue"
)

lblstock.pack(pady=10)

# STOCK LIST
stock_list = tk.Listbox(
    root,
    width=80,
    height=15,
    font=("Arial", 11)
)

stock_list.pack(pady=10)

# START
root.mainloop()