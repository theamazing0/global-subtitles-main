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
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL.ImageQt import ImageQt
# from PyQt5 import QtCore
import settings
from qt_material import apply_stylesheet
import tkinter as tk
from tkinter import *
import threading
# from PIL import ImageTk, Image
from translate import Translator
import configure
from pathlib import Path
from os.path import exists
import os

# * Create Variables

#  repeatCount = 0
quickstart = False
homeDirectoryPath = os.path.expanduser('~')

# * Start The Proccess


def tkinterCloseToPyQt():
    print("----<Subtitle Window Closing To Tray>----")
    subtitleWindow.destroy()
    settings.running = False


def quickstartfunc():
    global quickstart
    quickstart = True
    settings.running = True
    print("I just set settings.running to: " + str(settings.running))
    subtitleFunc()


def show_application():
    settings.running = True
    window.show()


def on_closing():
    settings.running = False
    sys.exit()


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
    # if code == "hi":
    #     translator = Translator(provider='libre', from_lang="en", to_lang=code,
    #                             secret_access_key=None, base_url="https://translate.astian.org/")
    # else:
    #     translator = Translator(
    #         provider='deepl', to_lang=code, secret_access_key=configure.deepl_key)
    translator = Translator(
        provider='deepl', to_lang=code, secret_access_key=configure.deepl_key)
    return translator.translate(translateThis)


def apiloop():
    import funcs
    print("apiloop has started in app.py")
    asyncio.run(funcs.send_receive())


def readFileUpdateSubtitle():
    global timedate
    global homeDirectoryPath
    # global repeatCount
    # repeatCount += 1
    # print("from app.py:" + settings.subtitleVar)
    rawSubtitle = settings.subtitleVar
    # if settings.transcriptionEnabled == "Enabled":
    #     fileName = homeDirectoryPath + \
    #         "/globalsubtitles_transcription_" + str(timedate)
    #     file = open(fileName, "a")
    #     file.write(rawSubtitle + "\n")
    #     file.close()
    if settings.translateTo != "English (American)":
        print("Detected Language Alternate Settings")
        subtitleLbl["text"] = translateSubtitle(
            settings.translateTo, rawSubtitle)
    else:
        subtitleLbl["text"] = rawSubtitle
    if settings.running == True:
        subtitleWindow.after(100, readFileUpdateSubtitle)
    else:
        quit


def subtitleFunc():
    global subtitleLbl
    global subtitleWindow
    global apiloopthread
    global quickstart
    if quickstart == False:
        settings.transcriptionEnabled = transcriptioncombo.currentText()
        print(settings.transcriptionEnabled)
        settings.translateTo = translationcombo.currentText()
        print(settings.translateTo)
        settings.opacity = opacitycombo.currentText()
        settings.wordcount = wordcountSpin.value()
        print(settings.wordcount)
        file_exists = exists(homeDirectoryPath+"/.globalsubtitles")
        if file_exists == False:
            dotfile = open(homeDirectoryPath+"/.globalsubtitles", "w")
            dotfile.write("F for showWindow")
            dotfile.close()
        elif file_exists == True:
            dotfile = open(homeDirectoryPath+"/.globalsubtitles", "w")
            if showWindowOnStartupCombo.currentText() == 'Enabled':
                dotfile.write("T for showWindow")
                dotfile.close()
            elif showWindowOnStartupCombo.currentText() == 'Disabled':
                dotfile.write("F for showWindow")
                dotfile.close()
    elif quickstart == True:
        quickstart == False
    print('----<Subtitle Window Opening>----')
    subtitleWindow = tk.Tk()
    # icon = PhotoImage(file='assets/icon.png')
    # subtitleWindow.iconphoto(False, icon)
    subtitleWindow.title('Global Subtitles')
    subtitleWindow.wait_visibility(subtitleWindow)
    if settings.opacity == "Semi-Transparent":
        subtitleWindow.attributes('-topmost', True, '-alpha', 0.3)
    elif settings.opacity == "Solid Background":
        subtitleWindow.attributes('-topmost')
    w = subtitleWindow.winfo_screenwidth()  # width for the Tk root
    h = 30  # 25  # height for the Tk root #! Change Window Height
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
    # closebutton = tk.Button(text='✖')
    # closebutton.pack(side=RIGHT)
    # subtitleLbl.grid(column=0, row=0)
    # closebutton.grid(column=1, row=0)
    print("text:" + subtitleLbl["text"])
    import funcs
    apiloopthread = threading.Thread(target=apiloop)
    apiloopthread.daemon = True
    apiloopthread.start()
    subtitleWindow.after(100, readFileUpdateSubtitle)
    window.close()
    subtitleWindow.protocol("WM_DELETE_WINDOW", tkinterCloseToPyQt)
    subtitleWindow.mainloop()
    # asyncio.run(funcs.send_receive())


def gui():
    global window
    global translationcombo
    global transcriptioncombo
    global opacitycombo
    global wordcountSpin
    global homeDirectoryPath
    global showWindowOnStartupCombo
    sapp = QApplication(sys.argv)
    sapp.setQuitOnLastWindowClosed(False)
    titleImg = QPixmap(str(Path(__file__).parent / 'assets/icon2.png'))
    icon = QIcon(str(Path(__file__).parent / "assets/icon2.png"))
    # icon = QImage('assets/icon2.png')
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    menu = QMenu()
    option1 = QAction("Show Application")
    option2 = QAction("Quick Start")
    quit = QAction("Quit")
    quit.triggered.connect(on_closing)
    option1.triggered.connect(show_application)
    option2.triggered.connect(quickstartfunc)
    menu.addAction(quit)
    menu.addAction(option1)
    menu.addAction(option2)
    tray.setContextMenu(menu)
    window = QWidget()
    window.setWindowTitle('Global Subtitles')
    # titleImg = QPixmap('assets/icon2.png')
    titleImgDisplay = QLabel()
    titleImgDisplay.setPixmap(titleImg)
    titleMsg = QLabel('<h2>Global Subtitles</h2>', parent=window)
    # Transcription
    transcriptionMsg = QLabel('<h4>Transcription</h4>', parent=window)
    transcriptioncombo = QComboBox()
    transcriptioncombo.addItem("Enabled")
    transcriptioncombo.addItem("Disabled")
    transcriptioncombo.setCurrentText(settings.transcriptionEnabled)
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
    translationcombo.setCurrentText(settings.translateTo)
    opacityMsg = QLabel('<h4>Window Opacity</h4>', parent=window)
    opacitycombo = QComboBox()
    opacitycombo.addItem("Semi-Transparent")
    opacitycombo.addItem("Solid Background")
    opacitycombo.setCurrentText(settings.opacity)
    wordcountMsg = QLabel('<h4>Words Shown</h4>', parent=window)
    wordcountSpin = QSpinBox()
    wordcountSpin.setValue(settings.wordcount)
    wordcountinfo = QLabel(
        '<p>Configures Max Words To Show On Screen At Time</p>', parent=window)
    showWindowOnStartupMsg = QLabel('<h4>Show Window on Startup</h4>', parent=window)
    showWindowOnStartupCombo = QComboBox()
    showWindowOnStartupCombo.addItem("Enabled")
    showWindowOnStartupCombo.addItem("Disabled")
    file_exists = exists(homeDirectoryPath+"/.globalsubtitles")
    if file_exists == False:
        dotfile = open(homeDirectoryPath+"/.globalsubtitles", "w")
        dotfile.write("F for showWindow")
        showWindowSetting = "Disabled"
        # dotfile.close()
    elif file_exists == True:
        dotfile = open(homeDirectoryPath+"/.globalsubtitles", "r")
        configfilevalue = dotfile.read(1)
        if configfilevalue == 'T':
            showWindowSetting = "Enabled"
            #window.show()
        elif configfilevalue == 'F':
            showWindowSetting = "Disabled"
    showWindowOnStartupCombo.setCurrentText(showWindowSetting)
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
    layout.addRow(showWindowOnStartupMsg, showWindowOnStartupCombo)
    layout.addRow(okButton)
    window.setGeometry(0, 0, 500, 500)
    window.setLayout(layout)
    apply_stylesheet(sapp, theme='dark_blue.xml')
    dotfile.close()
    print("Just Closed Dot File, showWindowSettings is equal to: " + showWindowSetting)
    if showWindowSetting == "Enabled":
        print("showWindowSetting is True")
        window.show()
    sys.exit(sapp.exec_())


if __name__ == "__main__":
    gui()
