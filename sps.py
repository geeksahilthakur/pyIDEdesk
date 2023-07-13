import time
from tkinter import *

w = Tk()
w.geometry("1500x788")
w.title("Boot OS")
w.config(bg='white')
ic = PhotoImage(file="1.png")
w.iconphoto(False, ic)
w.attributes("-fullscreen", True)
# w.overrideredirect(1)

Frame(w, width=1500, height=788, bg="white").place(x=0, y=0)
photo = PhotoImage(file="lgcrp.png")
main_logo = Label(w, image=photo, bg="white")
main_logo.place(x=450, y=250)

photo_a = PhotoImage(file="b.png")
photo_b = PhotoImage(file="y.png")

loding_text = Label(w, text="from sahil Thakur", font=("", 14, ""), bg="white", fg="black").place(x=550, y=600)

for i in range(3):
    l1 = Label(w, image=photo_a, border=0, relief=SUNKEN).place(x=580, y=450)
    l2 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=620, y=450)
    l3 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=660, y=450)
    l4 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=700, y=450)
    w.update_idletasks()
    time.sleep(0.5)

    l1 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=580, y=450)
    l2 = Label(w, image=photo_a, border=0, relief=SUNKEN).place(x=620, y=450)
    l3 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=660, y=450)
    l4 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=700, y=450)
    w.update_idletasks()
    time.sleep(0.5)

    l1 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=580, y=450)
    l2 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=620, y=450)
    l3 = Label(w, image=photo_a, border=0, relief=SUNKEN).place(x=660, y=450)
    l4 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=700, y=450)
    w.update_idletasks()
    time.sleep(0.5)

    l1 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=580, y=450)
    l2 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=620, y=450)
    l3 = Label(w, image=photo_b, border=0, relief=SUNKEN).place(x=660, y=450)
    l4 = Label(w, image=photo_a, border=0, relief=SUNKEN).place(x=700, y=450)
    w.update_idletasks()
    time.sleep(0.5)
w.destroy()
import main
