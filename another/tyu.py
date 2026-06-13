#import time


#minutes = int(input("Enter number: "))
#while minutes > 0:
 #           if minutes == 3:
  #              print("⚠️ Warning: time is almost up")
#
 #           print("Time left:", minutes)
  #          time.sleep(1)
   #         minutes -= 1
#print(" Stop")

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Sound (Windows)
try:
    import winsound
    def beep():
        winsound.Beep(1000, 500)
except:
    def beep():
        print("\a")


def start():
    try:
        t = int(entry.get())
        if t == 0:
            messagebox.showerror("Error", "0 is not allowed")
            return

        root.attributes("-fullscreen", True)
        entry.pack_forget()
        btn.pack_forget()

        run(t)

    except ValueError:
        messagebox.showerror("Error", "Enter a number")


def run(t):
    if t > 0:
        if t <= 10:
            label.config(text=f"⚠ time is almost up: {t}", fg="red")
        else:
            label.config(text=str(t), fg="black")

        root.configure(bg="black")
        label.configure(bg="black")

        root.after(1000, run, t - 1)

    else:
        for _ in range(3):
            beep()

        root.configure(bg="red")
        label.pack_forget()
        img_label.pack(expand=True)

        # ⏳ Wait 5 seconds, then reset
        root.after(5000, reset_app)


def reset_app():
    # Exit fullscreen
    root.attributes("-fullscreen", False)

    # Hide image
    img_label.pack_forget()

    # Clear entry
    entry.delete(0, tk.END)

    # Reset background
    root.configure(bg="SystemButtonFace")

    # Show UI again
    entry.pack(pady=20)
    btn.pack()
    label.config(text="", bg="SystemButtonFace")
    label.pack(expand=True)


# UI
root = tk.Tk()
root.title("Timer")

entry = tk.Entry(root, font=("Arial", 20), justify="center")
entry.pack(pady=20)

btn = tk.Button(root, text="Start", font=("Arial", 14), command=start)
btn.pack()

label = tk.Label(root, font=("Arial", 80))
label.pack(expand=True)

# Load image
img = Image.open("c:/Users/USER/OneDrive/DESKTOP/stop.png")
img = img.resize((1400,1400))
img = ImageTk.PhotoImage(img)

img_label = tk.Label(root, image=img, bg="red")

root.mainloop()