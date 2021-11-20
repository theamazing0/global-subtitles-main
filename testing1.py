import tkinter as tk
from random import seed, choice
from string import ascii_letters

seed(42)

colors = ('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')
def do_stuff():
    s = ''.join([choice(ascii_letters) for i in range(10)])
    color = choice(colors)
    l.config(text=s, fg=color)
    root.after(100, do_stuff)

root = tk.Tk()
root.wm_overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.bind("<Button-1>", lambda evt: root.destroy())

l = tk.Label(text='', font=("Helvetica", 60))
l.pack(expand=True)

do_stuff()
root.mainloop()