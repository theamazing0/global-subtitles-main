import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
import settings
from qt_material import apply_stylesheet

def okButtonClicked():
    settings.transcriptionEnabled = transcriptioncombo.currentText()
    print(settings.transcriptionEnabled)
    window.minimize()

sapp = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Settings')

titleMsg = QLabel('<h2>Select Your Settings Below</h2>', parent=window)

transcriptionMsg = QLabel('<h4>Transcription</h4>', parent=window)
transcriptioncombo = QComboBox()
transcriptioncombo.addItem("Enabled")
transcriptioncombo.addItem("Disabled")
transcriptioncombo.setCurrentText(settings.transcriptionEnabled)
transcriptiondetails = QLabel('<p>After Transcription, Output Can Be Found In Your Home Directory</p>', parent=window)

okButton = QPushButton(window)
okButton.setText("Start Global Subtitles")
okButton.clicked.connect(okButtonClicked)

layout = QFormLayout()
layout.addRow(titleMsg)
layout.addRow(transcriptionMsg, transcriptioncombo)
layout.addRow(transcriptiondetails)
layout.addRow(okButton)

window.setGeometry(0, 0, 500, 500)
window.setLayout(layout)
apply_stylesheet(sapp, theme='dark_blue.xml')

window.show()
sys.exit(sapp.exec_())