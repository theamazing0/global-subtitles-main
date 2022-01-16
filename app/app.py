import asyncio
# from fnmatch import translate
#import os
# from os import spawnl
import threading
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSpinBox
# from PyQt5 import QtCore
import settings
from qt_material import apply_stylesheet
import tkinter as tk
from tkinter import *
import threading
from PIL import ImageTk, Image
from translate import Translator
import configure

# * Create Variables

repeatCount = 0

# * Start The Proccess


def translateSubtitle(lang, translateThis):
    if lang == "Bulgarian":
        code = "BG"
    elif lang == "Czech":
        code = "CS"
    elif lang == "Danish":
        code = "DA"
    elif lang == "German":
        code = "DE"
    elif lang == "Greek":
        code = "EL"
    elif lang == "English (British)":
        code = "EN-GB"
    elif lang == "English (American)":
        code = "EN-US"
    elif lang == "Spanish":
        code = "ES"
    elif lang == "Estonian":
        code = "ET"
    elif lang == "Finnish":
        code = "FI"
    elif lang == "French":
        code = "FR"
    elif lang == "Hungarian":
        code = "HU"
    elif lang == "Hindi":
        code = "hi"
    elif lang == "Italian":
        code = "IT"
    elif lang == "Japanese":
        code = "JA"
    elif lang == "Lithuanian":
        code = "LT"
    elif lang == "Latvian":
        code = "LV"
    elif lang == "Dutch":
        code = "NL"
    elif lang == "Polish":
        code = "PL"
    elif lang == "Portuguese (Brazilian)":
        code = "PT-BR"
    elif lang == "Portguese (European)":
        code = "PT-PT"
    elif lang == "Romanian":
        code = "RO"
    elif lang == "Russian":
        code = "RU"
    elif lang == "Slovak":
        code = "SK"
    elif lang == "Slovenian":
        code = "SL"
    elif lang == "Swedish":
        code = "SV"
    elif lang == "Chinese":
        code = "ZH"
    if code == "hi":
        translator = Translator(provide='LibreTranslate', to_lang=code, secret_access_key=None, base_url='https://translate.astian.org/')
    else:
        translator = Translator(provider='deepl', to_lang=code, secret_access_key=configure.deepl_key)
    return translator.translate(translateThis)


def apiloop():
    import funcs
    asyncio.run(funcs.send_receive())

def readFileUpdateSubtitle():
    global timedate
    global homeDirectoryPath
    # global repeatCount
    # repeatCount += 1
    print("from app.py:" + settings.subtitleVar)
    rawSubtitle = settings.subtitleVar
    # if settings.transcriptionEnabled == "Enabled":
    #     fileName = homeDirectoryPath + \
    #         "/globalsubtitles_transcription_" + str(timedate)
    #     file = open(fileName, "a")
    #     file.write(rawSubtitle + "\n")
    #     file.close()
    if settings.translateTo != "English":
        subtitleLbl["text"] = translateSubtitle(
            settings.translateTo, rawSubtitle)
    else:
        subtitleLbl["text"] = rawSubtitle
    subtitleWindow.after(100, readFileUpdateSubtitle)


def subtitleFunc():
    global subtitleLbl
    global subtitleWindow
    settings.transcriptionEnabled = transcriptioncombo.currentText()
    print(settings.transcriptionEnabled)
    settings.translateTo = translationcombo.currentText()
    settings.opacity = opacitycombo.currentText()
    settings.wordcount = wordcountSpin.value()
    print(settings.wordcount)
    print('subtitle loop started')
    subtitleWindow = tk.Tk()
    icon = PhotoImage(file='assets/icon.png')
    # subtitleWindow.iconphoto(False, icon)
    subtitleWindow.title('Global Subtitles')
    subtitleWindow.wait_visibility(subtitleWindow)
    if settings.opacity == "Semi-Transparent":
        subtitleWindow.attributes('-topmost', True, '-alpha', 0.3)
    elif settings.opacity == "Solid Background":
        subtitleWindow.attributes('-topmost')
    w = subtitleWindow.winfo_screenwidth()  # width for the Tk root
    h = 25  # height for the Tk root
    # get screen width and height
    ws = subtitleWindow.winfo_screenwidth()  # width of the screen
    hs = subtitleWindow.winfo_screenheight()  # height of the screen
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
    global opacitycombo
    global wordcountSpin
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
    transcriptiondetails = QLabel(
        '<p>After Transcription, Output Can Be Found In Your Home Directory</p>', parent=window)
    # Translation
    transalationtoMsg = QLabel('<h4>Transalate To</h4>', parent=window)
    translationcombo = QComboBox()
    translationcombo.addItem("Bulgarian")
    translationcombo.addItem("Czech")
    translationcombo.addItem("Danish")
    translationcombo.addItem("German")
    translationcombo.addItem("Greek")
    translationcombo.addItem("English (American)")
    translationcombo.addItem("English (British)")
    translationcombo.addItem("Spanish")
    translationcombo.addItem("Estonian")
    translationcombo.addItem("Finnish")
    translationcombo.addItem("French")
    translationcombo.addItem("Hungarian")
    translationcombo.addItem("Hindi")
    translationcombo.addItem("Italian")
    translationcombo.addItem("Japanese")
    translationcombo.addItem("Lithuanian")
    translationcombo.addItem("Latvian")
    translationcombo.addItem("Dutch")
    translationcombo.addItem("Polish")
    translationcombo.addItem("Portguese (Brazilian)")
    translationcombo.addItem("Portguese (European)")
    translationcombo.addItem("Romanian")
    translationcombo.addItem("Russian")
    translationcombo.addItem("Slovak")
    translationcombo.addItem("Swedish")
    translationcombo.addItem("Chinese")
    translationcombo.setCurrentText("English (American)")
    opacityMsg = QLabel('<h4>Window Opacity</h4>', parent=window)
    opacitycombo = QComboBox()
    opacitycombo.addItem("Semi-Transparent")
    opacitycombo.addItem("Solid Background")
    opacitycombo.setCurrentText("Semi-Transparent")
    wordcountMsg = QLabel('<h4>Words Shown</h4>', parent=window)
    wordcountSpin = QSpinBox()
    wordcountSpin.setValue(8)
    wordcountinfo = QLabel(
        '<p>Configures Max Words To Show On Screen At Time</p>', parent=window)
    okButton = QPushButton(window)
    okButton.setText("Start Global Subtitles")
    okButton.clicked.connect(subtitleFunc)
    layout = QFormLayout()
    layout.addRow(titleImgDisplay, titleMsg)
    layout.addRow(transalationtoMsg, translationcombo)
    layout.addRow(opacityMsg, opacitycombo)
    layout.addRow(transcriptionMsg, transcriptioncombo)
    layout.addRow(transcriptiondetails)
    layout.addRow(wordcountMsg, wordcountSpin)
    layout.addRow(wordcountinfo)
    layout.addRow(okButton)
    window.setGeometry(0, 0, 500, 500)
    window.setLayout(layout)
    apply_stylesheet(sapp, theme='dark_blue.xml')
    window.show()
    sys.exit(sapp.exec_())


if __name__ == "__main__":
    gui()
