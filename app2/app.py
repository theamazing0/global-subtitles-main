import asyncio
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image  

# * Start The Proccess


def subtitle():
    print('subtitle loop started')
    subtitleWindow = tk.Tk()
    subtitleWindow.title('Global Subtitles')
    subtitleWindow.wait_visibility(subtitleWindow)
    subtitleWindow.attributes('-topmost', True, '-alpha', 0.3)
    subtitleLbl = tk.Label(master = startWindow, text = 'Listening For Audio...', font = ('Times New Roman', 48))
    subtitleLbl.pack()
    startWindow.destroy()  # subtitleWindow.mainloop()
    # import funcs
    # asyncio.run(funcs.send_receive())

# * Tkinter Implementation


startWindow = tk.Tk()
startWindow.title('Welcome')
startWindow.resizable(width=False, height=False)

titleFrame = tk.Frame(master=startWindow)
titleFrame.columnconfigure(0, minsize=500)

logo = Canvas(titleFrame, width = 500, height = 200)  
logo.pack()  
img = ImageTk.PhotoImage(Image.open("assets/logoBanner.png"))  
logo.create_image(100, 100, anchor=SW, image=img)

titleFrame.grid(row=0, column=0)
logo.grid(row=0, column=0)

# titleLbl = tk.Label(text='Global Subtitles', font=(
#     'Times New Roman', '48'), master=titleFrame)
# titleFrame.grid(row=0, column=0)
# titleLbl.grid(row=0, column=0)

buttonFrame = tk.Frame(master=startWindow)
buttonFrame.columnconfigure(2)
startBtn = tk.Button(master=buttonFrame, text='Start', font=(
    'Times New Roman', '30'), command=subtitle)

buttonFrame.grid(row=1, column=0)
startBtn.grid(row=0, column=0, padx=50)

# asyncio.run(send_receive())

startWindow.mainloop()

# * -------------------------
