import asyncio
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
import subtitle

# * Start The Proccess


def apiloop():
    import funcs
    asyncio.run(funcs.send_receive())

def readFileUpdateSubtitle():
    print("from app.py:" + subtitle.subtitleVar)
    subtitleLbl["text"] = subtitle.subtitleVar
    subtitleWindow.after(1000, readFileUpdateSubtitle)

def subtitleFunc():
    global subtitleLbl
    global subtitleWindow
    print('subtitle loop started')
    subtitleWindow = tk.Tk()
    icon = PhotoImage(file = 'assets/icon.png')
    subtitleWindow.iconphoto(False, icon)
    subtitleWindow.title('Global Subtitles')
    subtitleWindow.wait_visibility(subtitleWindow)
    subtitleWindow.attributes('-topmost', True, '-alpha', 0.3)
    w = subtitleWindow.winfo_screenwidth() # width for the Tk root
    h = 25 # height for the Tk root
    # get screen width and height
    ws = subtitleWindow.winfo_screenwidth() # width of the screen
    hs = subtitleWindow.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = ws/2 - ws/2
    y = hs - 100
    # set the dimensions of the screen 
    # and where it is placed
    subtitleWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    # making subtitleLbl
    subtitleLbl = tk.Label(
        master=subtitleWindow, text='Listening For Audio...', font=('Times New Roman', 30), bg="yellow", fg="black")
    subtitleLbl.pack()
    startWindow.destroy()
    print("text:" + subtitleLbl["text"])
    # subtitleWindow.mainloop()
    import funcs
    apiloopthread = threading.Thread(target=apiloop)
    apiloopthread.start()
    subtitleWindow.after(1000, readFileUpdateSubtitle)
    # asyncio.run(funcs.send_receive())


def gui():
    # * Tkinter Implementation
    global startWindow
    startWindow = tk.Tk()
    startWindow.title('Welcome')
    guiicon = PhotoImage(file = 'assets/icon.png')
    startWindow.iconphoto(False, guiicon)
    startWindow.resizable(width=False, height=False)
    startWindow.configure(background='#0b0633')
    # logo = Canvas(startWindow, width = 400, height = 100)
    # logo.pack()
    img = ImageTk.PhotoImage(Image.open("assets/logoBanner.png"))
    imageLabel = tk.Label(startWindow, image=img)
    imageLabel.pack(side="top", fill="both", expand="yes")
    # logo.create_image(100, 100, anchor=S, image=img)
    # logo.pack()
    # titleLbl = tk.Label(text='Global Subtitles', font=(
    #     'Times New Roman', '48'), master=titleFrame)
    # titleFrame.grid(row=0, column=0)
    # titleLbl.grid(row=0, column=0)
    btnimg = ImageTk.PhotoImage(Image.open("assets/startButton.png"))
    startBtn = tk.Button(master=startWindow, image = btnimg, command=subtitleFunc)
    startBtn.pack()
    # asyncio.run(send_receive())
    startWindow.mainloop()


if __name__ == "__main__":
    gui()
