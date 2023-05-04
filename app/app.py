'''

 ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     
██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     
██║  ███╗██║     ██║   ██║██████╔╝███████║██║     
██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     
╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗
 ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

███████╗██╗   ██╗██████╗ ████████╗██╗████████╗██╗     ███████╗███████╗
██╔════╝██║   ██║██╔══██╗╚══██╔══╝██║╚══██╔══╝██║     ██╔════╝██╔════╝
███████╗██║   ██║██████╔╝   ██║   ██║   ██║   ██║     █████╗  ███████╗
╚════██║██║   ██║██╔══██╗   ██║   ██║   ██║   ██║     ██╔══╝  ╚════██║
███████║╚██████╔╝██████╔╝   ██║   ██║   ██║   ███████╗███████╗███████║
╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝

!!! Make Sure You Have Specified API Keys In app/configure.py Before Running !!!
!!! Make Sure You Have Installed All Dependencies In requirements.txt !!!
Read the LICENSE file for License
Read README.md for information about the project
Run app/app.py with Python 3.10.1 to Start Applet

'''

# * Imports Required Dependencies
# Make Sure You Have Installed These from requirements.txt

import asyncio
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
import settings
from qt_material import apply_stylesheet
import tkinter as tk
from tkinter import *
import threading
from translate import Translator
import configure
from pathlib import Path
from os.path import exists
import os

# * Create Variables

# Sets Application Default Mode To normal
quickstart = False
# Gets Home Directory Path To Be Used Later On
homeDirectoryPath = os.path.expanduser('~')

# * Functions

# Run When System Close Occurs To Correctly Close Subtitle Window


def tkinterCloseToPyQt():
    # Information Log Statement
    print("     INFO: Subtitle Window Closing To Tray")
    # Remove Subtitle Window
    subtitleWindow.destroy()
    # Send Signal To Stop To All Other Running Loops
    settings.running = False

# Run When "Quick Start" Button Clicked In The System Tray


def quickstartfunc():
    global quickstart
    # Information Log Statement
    print("     INFO: Application Opening In Quickstart Mode")
    # Sets Application Mode To "quickstart"
    quickstart = True
    # Tells Proccesses That May Have Been Quit In An Earlier Close That It's Safe To Start
    settings.running = True
    # Open Subtitle Window
    subtitleFunc()

# Run When "Show Application" Button Clicked In The System Tray


def show_application():
    # Information Log Statement
    print("     INFO: Settings / Welcome Window Opened")
    # Tells Proccesses That May Have Been Quit In An Earlier Close That It's Safe To Start
    settings.running = True
    # Shows PyQt5 Window
    window.show()

# Run When "Quit" Button Clicked In The System Tray


def on_closing():
    # Information Log Statement
    print("     INFO: Application Terminating")
    # Send Signal To Stop To All Running Loops
    settings.running = False
    # Terminate Python Application Proccess
    sys.exit()

# Used Internally For Transalating Text


def translateSubtitle(lang, translateThis):
    # Define The ISO Codes For Each Supported Language For API Requests
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
    # Define DeepL Transalation Configuration With Key From app/config.py and the Language Code
    # You Need A DeepL API Key In app/config.py for translation to work
    translator = Translator(
        provider='deepl', to_lang=code, secret_access_key=configure.deepl_key)
    # Return Translated Text To Wherever Function Was Called
    return translator.translate(translateThis)

# Used Internally To Start The Speech To Text Conversion Loop


def apiloop():
    # Information Log Statement
    print("     INFO: Subtitle Loop Started")
    # Run Initialization For Conversion and Import Functions From app/funcs.py
    import funcs
    # Run Conversion Loop With Asyncio
    asyncio.run(funcs.send_receive())

# Used Internally To Update Subtitle Text On The Subtitle Window


def readFileUpdateSubtitle():
    # Get Access To Global Variables
    global timedate
    global homeDirectoryPath
    # Get New Subtitle From app/settings.py
    rawSubtitle = settings.subtitleVar
    # Finds If Translation Is Required Or Not
    # If Translation Is Requried
    if settings.translateTo != "English (American)":
        # Set Subtitle Label Text To Subtitle
        subtitleLbl["text"] = translateSubtitle(  # Call translateSubtitle Function To Convert Text
            settings.translateTo, rawSubtitle)
    else:  # If Translation Is Not Required
        # Set Subtitle Label Text To Subtitle
        subtitleLbl["text"] = rawSubtitle
        # Checks If Application Is Still Running
    if settings.running == True:  # If Application Is Still Running
        # Schedules Time To Reiterate Function
        subtitleWindow.after(100, readFileUpdateSubtitle)
    else:  # If Application Is Closing
        quit  # Stop Loop

# Run Whenever The Subtitle Window Is Opened


def subtitleFunc():
    # Makes Global Variables Avaible
    global subtitleLbl
    global subtitleWindow
    global apiloopthread
    global quickstart
    # Checks If quickstart Application Mode Is Enabled
    if quickstart == False:  # If quickstart Is Disabled
        # Sets Transciption Enabled Setting To The One Set By User In PyQt5 Window
        settings.transcriptionEnabled = transcriptioncombo.currentText()
        # Sets Translate To Setting To The One Set By User In PyQt5 Window
        settings.translateTo = translationcombo.currentText()
        # Sets Opacity Setting To The One Set By User In PyQt5 Window
        settings.opacity = opacitycombo.currentText()
        # Sets Word Count Setting To The One Set By User In PyQt5 Window
        settings.wordcount = wordcountSpin.value()
        # Finds If Config Dotfile Exits
        file_exists = exists(homeDirectoryPath+"/.globalsubtitles")
        if file_exists == False:  # If Dotfile Is Not Found
            # Create Dotfile
            dotfile = open(homeDirectoryPath+"/.globalsubtitles", "w")
            # Add Default Configuration
            dotfile.write("F for showWindow")
            # Close Connection
            dotfile.close()
        elif file_exists == True:  # If Dotfile Found
            # Open Dotfile
            dotfile = open(homeDirectoryPath+"/.globalsubtitles", "w")
            # Checks What The User Chose For Show Window On Startup
            if showWindowOnStartupCombo.currentText() == 'Enabled':  # If Enabled
                # Write Configuration
                dotfile.write("T for showWindow")
                # Close Connection
                dotfile.close()
            elif showWindowOnStartupCombo.currentText() == 'Disabled':  # If Disabled
                # Write Configuration
                dotfile.write("F for showWindow")
                # Close Connection
                dotfile.close()
    elif quickstart == True:  # If quickstart Application Mode Is Enabled
        # Disable It For Next Application Start
        quickstart == False
    # Information Log Statement
    print('     INFO: Subtitle Window Opened')
    # Create Subtitle Window
    subtitleWindow = tk.Tk()
    # Assign Window Manager Title
    subtitleWindow.title('Global Subtitles')
    # Wait Visibility
    subtitleWindow.wait_visibility(subtitleWindow)
    # Checks If Window Should Be Semi-Transparent or Solid
    if settings.opacity == "Semi-Transparent":  # If Semi-Transparent
        # Set Window To Topmost and Semi-Transparent
        subtitleWindow.attributes('-topmost', True, '-alpha', 0.3)
    elif settings.opacity == "Solid Background":
        # Set Window To Topmost
        subtitleWindow.attributes('-topmost')
    # Define Window Height And Width
    w = subtitleWindow.winfo_screenwidth()
    h = 30  # ! Change Window Height If You Wish (Default 30)
    # TODO Add Settings Configuration Option For Window Height
    # Get Screen Width & Height
    ws = subtitleWindow.winfo_screenwidth()
    hs = subtitleWindow.winfo_screenheight()
    # Calculate Location On The Screen
    x = ws/2 - ws/2  # In The Center
    y = hs - 100  # 100px From The Bottom
    # Set Dimensions Of Window And Where It Is Places
    subtitleWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    # Create Label For Subtitles
    subtitleLbl = tk.Label(
        master=subtitleWindow, text='Listening For Audio...', font=('Times New Roman', 30), bg="yellow", fg="black")
    # Add Subtitle Label To Window
    subtitleLbl.pack()
    # Define Thread For Speech To Text API Loop
    apiloopthread = threading.Thread(target=apiloop)
    apiloopthread.daemon = True
    # Start Text For Speech To Text API Loop
    apiloopthread.start()
    # Start Loop To Update Subtite Label's Text To Subtitle From API
    subtitleWindow.after(100, readFileUpdateSubtitle)
    # Close PyQt5 Settings / Welcome GUI
    window.close()
    # Set subtitleWindow System Close Protocol To Custom Function
    subtitleWindow.protocol("WM_DELETE_WINDOW", tkinterCloseToPyQt)
    # Show Subtitle Window
    subtitleWindow.mainloop()

# Run On Application Startup


def gui():
    # Gets Access To Global Variables
    global window
    global translationcombo
    global transcriptioncombo
    global opacitycombo
    global wordcountSpin
    global homeDirectoryPath
    global showWindowOnStartupCombo
    # Defines PyQt5 App
    sapp = QApplication(sys.argv)
    # Configures Application To Not Quit When The |X| Button Is Clicked
    sapp.setQuitOnLastWindowClosed(False)
    # Defines Pixmap Version of the Logo Asset app/assets/icon2.png
    titleImg = QPixmap(str(Path(__file__).parent / 'assets/icon2.png'))
    # Defines Icon Version of the Logo Asset app/assets/icon2.png
    icon = QIcon(str(Path(__file__).parent / "assets/icon2.png"))
    # Creates System Tray Icon
    tray = QSystemTrayIcon()
    # Sets System Tray Icon To app/assets/icon2.png
    tray.setIcon(icon)
    # Show The Tray Icon
    tray.setVisible(True)
    # Creates Menu For System Tray
    menu = QMenu()
    # Creates Option To Show The PyQt5 GUI
    option1 = QAction("Show Application")
    # Creates Option To Directly Start The Subtitle Loop
    option2 = QAction("Quick Start")
    # Creates Option To Terminate Application Proccess
    quit = QAction("Quit")
    # Assigns "Quit" To Custom Termination Function
    quit.triggered.connect(on_closing)
    # Assigns "Show Application" To Run Function
    option1.triggered.connect(show_application)
    # Assigns "Quick Start" To Run Function
    option2.triggered.connect(quickstartfunc)
    # Show Show Application Button
    menu.addAction(option1)
    # Show Quick Start Button
    menu.addAction(option2)
    # Show Quit Button
    menu.addAction(quit)
    # Set Tray Menu To Created Menu
    tray.setContextMenu(menu)
    # Creates PyQt5 Settings / Welcome GUI
    window = QWidget()
    # Sets Window Title for Window Manager
    window.setWindowTitle('Global Subtitles')
    # Creates Label To Display Logo
    titleImgDisplay = QLabel()
    # Sets Label To Logo
    titleImgDisplay.setPixmap(titleImg)
    # Creates Label With Title Text
    titleMsg = QLabel('<h2>Global Subtitles</h2>', parent=window)
    #! Transcription Configuration Options
    # Creates Label To Describe Transcription Option
    transcriptionMsg = QLabel('<h4>Transcription</h4>', parent=window)
    # Creates ComboBox To Configure Transcription
    transcriptioncombo = QComboBox()
    # Creates Enabled Option
    transcriptioncombo.addItem("Enabled")
    # Creates Disabled Option
    transcriptioncombo.addItem("Disabled")
    # Sets ComboBox Default Option
    transcriptioncombo.setCurrentText(settings.transcriptionEnabled)
    # Creates Label To Give More Description About Transcription
    transcriptiondetails = QLabel(
        '<p>After Transcription, Output Can Be Found In Your Home Directory</p>', parent=window)
    #! Translation Configuration Options
    # Creates Label To Describe Translation Option
    transalationtoMsg = QLabel('<h4>Transalate To</h4>', parent=window)
    # Creates ComboBox To Choose Translation Language
    translationcombo = QComboBox()
    # Adds Translation Language Options To ComboBox
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
    # Sets ComboBox Default Option
    translationcombo.setCurrentText(settings.translateTo)
    #! Opacity Configuration Options
    # Creates Label To Describe Opacity Option
    opacityMsg = QLabel('<h4>Window Opacity</h4>', parent=window)
    # Creates ComboBox To Choose Opacity Levels
    opacitycombo = QComboBox()
    # Adds Semi-Transparent Opacity Option
    opacitycombo.addItem("Semi-Transparent")
    # Adds Solid Background Opacity Option
    opacitycombo.addItem("Solid Background")
    # Sets Opacity Combo To Default / Previous Setting
    opacitycombo.setCurrentText(settings.opacity)
    #! Words Shown Configuration Options
    # Creates Label To Describe Word Count Option
    wordcountMsg = QLabel('<h4>Words Shown</h4>', parent=window)
    # Creates Spin Box To Choose Word Count
    wordcountSpin = QSpinBox()
    # Set Spin Box To Default / Previous Settings
    wordcountSpin.setValue(settings.wordcount)
    # Creates Label To Give More Info About Word Count Option
    wordcountinfo = QLabel(
        '<p>Configures Max Words To Show On Screen At Time</p>', parent=window)
    #! Show Window On Startup Configuration Options
    # Creates Label To Describe Show Window On Startup Option
    showWindowOnStartupMsg = QLabel(
        '<h4>Show Window on Startup</h4>', parent=window)
    # Creates ComboBox To Configure Show Window On Startup
    showWindowOnStartupCombo = QComboBox()
    # Adds Enabled Option
    showWindowOnStartupCombo.addItem("Enabled")
    # Adds Disabled Option
    showWindowOnStartupCombo.addItem("Disabled")
    # Checks If Configuration File Exists
    file_exists = exists(homeDirectoryPath+"/.globalsubtitles")
    if file_exists == False:  # If It Doesn't Exist
        # Create Dotfile
        dotfile = open(homeDirectoryPath+"/.globalsubtitles", "w")
        # Write Default Configuration
        dotfile.write("F for showWindow")
        # Sets Runtime Setting To Default
        showWindowSetting = "Disabled"
    elif file_exists == True:  # If It Does Exist
        # Open Configuration File
        dotfile = open(homeDirectoryPath+"/.globalsubtitles", "r")
        # Gets Configuration Value From Dotfile
        configfilevalue = dotfile.read(1)
        # Checks Configuration Value
        if configfilevalue == 'T':  # If Enabled
            # Set Runtime Setting To Enabled
            showWindowSetting = "Enabled"
        elif configfilevalue == 'F':
            # Set Runtime Setting To Disabled
            showWindowSetting = "Disabled"
    # Set ComboBox To Runtime Setting Found In Dotfile
    showWindowOnStartupCombo.setCurrentText(showWindowSetting)
    # Creates Button To Start Subtitle Loop And Dismiss PyQt5 Window
    okButton = QPushButton(window)
    # Sets Ok Button Text
    okButton.setText("Start Global Subtitles")
    # Assigns Ok Button To Function
    okButton.clicked.connect(subtitleFunc)
    # Creates Window Layout
    layout = QFormLayout()
    # Adds Rows For All GUI Objects
    layout.addRow(titleImgDisplay, titleMsg)
    layout.addRow(transalationtoMsg, translationcombo)
    layout.addRow(opacityMsg, opacitycombo)
    layout.addRow(transcriptionMsg, transcriptioncombo)
    layout.addRow(transcriptiondetails)
    layout.addRow(wordcountMsg, wordcountSpin)
    layout.addRow(wordcountinfo)
    layout.addRow(showWindowOnStartupMsg, showWindowOnStartupCombo)
    layout.addRow(okButton)
    # Sets Window Size
    window.setGeometry(0, 0, 500, 500)
    # Sets Window To Custom Layout
    window.setLayout(layout)
    # Applies Dark Blue Theming
    apply_stylesheet(sapp, theme='dark_blue.xml')
    # TODO Add Options For More Themes
    # Closes Configuration File Connection
    dotfile.close()
    # Checks If Show Window On Startup Is Enabled
    if showWindowSetting == "Enabled":  # If Enabled
        # Information Log Statement
        print("     INFO: Settings / Welcome Window Opened")
        # Shows PyQt5 Settings / Welcome Window
        window.show()
    # Starts PyQt5 GUI Application (System Tray Applet & Settings / Welcome Window)
    sys.exit(sapp.exec_())


# If Code Is Being Run
if __name__ == "__main__":
    # Prints ASCII Art To Logs
    print("\n")
    print('''    ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     
    ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     
    ██║  ███╗██║     ██║   ██║██████╔╝███████║██║     
    ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     
    ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗
    ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

    ███████╗██╗   ██╗██████╗ ████████╗██╗████████╗██╗     ███████╗███████╗
    ██╔════╝██║   ██║██╔══██╗╚══██╔══╝██║╚══██╔══╝██║     ██╔════╝██╔════╝
    ███████╗██║   ██║██████╔╝   ██║   ██║   ██║   ██║     █████╗  ███████╗
    ╚════██║██║   ██║██╔══██╗   ██║   ██║   ██║   ██║     ██╔══╝  ╚════██║
    ███████║╚██████╔╝██████╔╝   ██║   ██║   ██║   ███████╗███████╗███████║
    ╚══════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝''')
    print("\n")
    # Print Welcome Information
    print("     Read the LICENSE file for License")
    print("     Read README.md for information about the project")
    # Check If User Has Supplied API Keys & Provide Warnings If Not
    if configure.assemblyai_key == "API KEY GOES HERE":
        print("     CRITICAL/WARNING: AssemblyAI API Key NOT FOUND, Subtitle Function Will Not Work")
    if configure.deepl_key == "API KEY GOES HERE":
        print("     WARNING: DeepL API Key NOT FOUND, Translation Will Not Work")
    # Launch PyQt5 GUI Function
    gui()
