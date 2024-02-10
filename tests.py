import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
from PyQt5.QtCore import Qt, QTimer

def update_progress():
    value = progress.value()
    if value > 0:
        value -= 1
        progress.setValue(value)

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Using QProgressBar")
window.setGeometry(100, 100, 300, 200)
progress = QProgressBar(window)
progress.setGeometry(30, 50, 240, 25)
progress.setMinimum(0)
progress.setMaximum(15)

progress.setFormat('%v')
progress.reset()
progress.setValue(15)
btn = QtWidgets.QPushButton(window)
btn.setGeometry(30, 100, 200, 25)
btn.clicked.connect(update_progress)


window.show()
app.exec()
