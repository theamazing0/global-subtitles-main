import asyncio
from fnmatch import translate
from os import spawnl
import threading
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import settings
from qt_material import apply_stylesheet
import tkinter as tk
from tkinter import *
import threading
from PIL import ImageTk, Image
from translate import Translator

# * Start The Proccess

def translateSubtitle(lang, translateThis):
    if lang == "Spanish":
        code = "es"
    elif lang == "Hindi":
        code = "hi"
    elif lang == "French":
        code = "fr"
    elif lang == "Telugu":
        code = "te"
    elif lang == "Chinese Simplified":
        code = "zh"
    elif lang == "Korean":
        code = "ko"
    elif lang == "Tamil":
        code = "ta"
    elif lang == "Gujarati":
        code = "gu"
    elif lang == "Punjabi":
        code = "pa"
    elif lang == "Bengali":
        code = "bn"
    translator= Translator(to_lang=code)
    return translator.translate(translateThis)

def apiloop(): 
    import funcs
    asyncio.run(funcs.send_receive())

def readFileUpdateSubtitle():
    print("from app.py:" + settings.subtitleVar)
    rawSubtitle = settings.subtitleVar
    if settings.translateTo != "English":
        subtitleLbl["text"] = translateSubtitle(settings.translateTo, rawSubtitle)
    else:
        subtitleLbl["text"] = rawSubtitle
    subtitleWindow.after(100, readFileUpdateSubtitle)

def subtitleFunc():
    global subtitleLbl
    global subtitleWindow
    settings.transcriptionEnabled = transcriptioncombo.currentText()
    print(settings.transcriptionEnabled)
    settings.translateTo = translationcombo.currentText()
    print('subtitle loop started')
    subtitleWindow = tk.Tk()
    icon = PhotoImage(file = 'assets/icon.png')
    # subtitleWindow.iconphoto(False, icon)
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
    print("text:" + subtitleLbl["text"])
    import funcs
    apiloopthread = threading.Thread(target=apiloop)
    apiloopthread.start()
    subtitleWindow.after(100, readFileUpdateSubtitle)
    window.close()
    subtitleWindow.mainloop()
    # asyncio.run(funcs.send_receive())

def gui():
    global window
    global translationcombo
    global transcriptioncombo
    sapp = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Global Subtitles')
    titleImg = QPixmap('assets/icon2.png')
    titleImgDisplay = QLabel()
    titleImgDisplay.setPixmap(titleImg)
    titleMsg = QLabel('<h2>Global Subtitles</h2>', parent=window)
    # Transcription
    transcriptionMsg = QLabel('<h4>Transcription</h4>', parent=window)
    transcriptioncombo = QComboBox()
    transcriptioncombo.addItem("Enabled")
    transcriptioncombo.addItem("Disabled")
    transcriptioncombo.setCurrentText("Disabled")
    transcriptiondetails = QLabel('<p>After Transcription, Output Can Be Found In Your Home Directory</p>', parent=window)
    # Translation
    transalationtoMsg = QLabel('<h4>Transalate To</h4>', parent=window)
    translationcombo = QComboBox()
    translationcombo.addItem("Spanish")
    translationcombo.addItem("English")
    translationcombo.addItem("French")
    translationcombo.addItem("Hindi")
    translationcombo.addItem("Telugu")
    translationcombo.addItem("Chinese Simplified")
    translationcombo.addItem("Korean")
    translationcombo.addItem("Tamil")
    translationcombo.addItem("Gujarati")
    translationcombo.addItem("Punjabi")
    translationcombo.addItem("Bengali")
    translationcombo.setCurrentText("English")
    okButton = QPushButton(window)
    okButton.setText("Start Global Subtitles")
    okButton.clicked.connect(subtitleFunc)
    layout = QFormLayout()
    layout.addRow(titleImgDisplay, titleMsg)
    layout.addRow(transcriptionMsg, transcriptioncombo)
    layout.addRow(transcriptiondetails)
    layout.addRow(transalationtoMsg, translationcombo)
    layout.addRow(okButton)
    window.setGeometry(0, 0, 500, 500)
    window.setLayout(layout)
    apply_stylesheet(sapp, theme='dark_blue.xml')
    window.show()
    sys.exit(sapp.exec_())


if __name__ == "__main__":
    gui()
