
import tkinter as tk
from tkinter import messagebox
import pymysql
from supabase import create_client, Client
import socket
import threading
import time

# ---------------- SUPABASE ----------------
URL = "https://jmhhuprhlzxugtthynzn.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImptaGh1cHJobHp4dWd0dGh5bnpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgzMTM5MTIsImV4cCI6MjA5Mzg4OTkxMn0.4u4hDD7ok0p8wxXla8Rlrugrznfk2E9WM_2dt8a_tX8"

supabase: Client = create_client(URL, KEY)

# ---------------- INTERNET CHECK ----------------
def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# ---------------- SYNC WORKER ----------------
def sync_worker():

    while True:

        if is_online():

            try:
                conn = pymysql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="ass_db",
                    cursorclass=pymysql.cursors.DictCursor
                )

                with conn.cursor() as cursor:

                    cursor.execute("SELECT id, label, price FROM ass_db WHERE synced = 0")
                    rows = cursor.fetchall()

                    if rows:

                        print("Syncing:", len(rows))

                        data = [
                            {"label": r["label"], "price": float(r["price"])}
                            for r in rows
                        ]

                        supabase.table("ass_db").insert(data).execute()

                        ids = [r["id"] for r in rows]

                        query = f"""
                        UPDATE ass_db
                        SET synced = 1
                        WHERE id IN ({','.join(['%s'] * len(ids))})
                        """

                        cursor.execute(query, tuple(ids))
                        conn.commit()

                conn.close()

            except Exception as e:
                print("Sync error:", e)

        time.sleep(5)

# ---------------- SAVE TO MYSQL ----------------
def save_to_local():

    try:

        data = []

        for i in range(5):

            label = labels[i].get()
            price = prices[i].get()

            if label and price:
                data.append((label, float(price)))

        if not data:
            messagebox.showerror("Error", "Enter data first")
            return

        db = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="ass_db"
        )

        with db.cursor() as cur:

            cur.executemany(
                "INSERT INTO ass_db (label, price, synced) VALUES (%s, %s, 0)",
                data
            )

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Saved to xampp and supabase!")

        for e in labels + prices:
            e.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- UI ----------------
root = tk.Tk()
root.title("Ass DB Sync App")

labels = []
prices = []

for i in range(5):

    tk.Label(root, text="Item").grid(row=i, column=0)
    tk.Label(root, text="Price").grid(row=i, column=1)

    l = tk.Entry(root)
    l.grid(row=i, column=2)

    p = tk.Entry(root)
    p.grid(row=i, column=3)

    labels.append(l)
    prices.append(p)

tk.Button(
    root,
    text="SAVE",
    command=save_to_local,
    bg="blue",
    fg="white"
).grid(row=6, column=0, columnspan=4, pady=20)

# ---------------- START THREAD ----------------
threading.Thread(target=sync_worker, daemon=True).start()

root.mainloop()