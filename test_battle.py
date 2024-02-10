import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class GameMainWindow(QMainWindow):
    def __init__(self):
        super(GameMainWindow, self).__init__()

        self.setWindowTitle('Card Dungeon')
        self.setGeometry(0, 0, 1920, 1080)
        self.showFullScreen()

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.menu_background = QtWidgets.QLabel(self.centralwidget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        #self.menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/birch_summer.png"))

        self.card1 = QtWidgets.QPushButton(self.centralwidget)
        self.card1.setGeometry(QtCore.QRect(400, 750, 180, 260))
        self.card1.setText("card1")

        self.card2 = QtWidgets.QPushButton(self.centralwidget)
        self.card2.setGeometry(QtCore.QRect(600, 750, 180, 260))
        self.card2.setText("card2")

        self.card3 = QtWidgets.QPushButton(self.centralwidget)
        self.card3.setGeometry(QtCore.QRect(800, 750, 180, 260))
        self.card3.setText("card3")

        self.card4 = QtWidgets.QPushButton(self.centralwidget)
        self.card4.setGeometry(QtCore.QRect(1000, 750, 180, 260))
        self.card4.setText("card4")

        self.card5 = QtWidgets.QPushButton(self.centralwidget)
        self.card5.setGeometry(QtCore.QRect(1200, 750, 180, 260))
        self.card5.setText("card5")

        self.end_turn_button = QtWidgets.QPushButton(self.centralwidget)
        self.end_turn_button.setGeometry(QtCore.QRect(1700, 700, 140, 40))
        self.end_turn_button.setText("end_turn_button")

        self.points = QtWidgets.QLabel(self.centralwidget)
        self.points.setGeometry(QtCore.QRect(170, 700, 60, 60))
        self.points.setText("0")

        self.hero = QtWidgets.QLabel(self.centralwidget)
        self.hero.setGeometry(QtCore.QRect(250, 310, 140, 240))
        self.hero.setText("hero")
        self.hero_hp = QtWidgets.QLabel(self.centralwidget)
        self.hero_hp.setGeometry(QtCore.QRect(250, 570, 140, 20))
        self.hero_hp.setText("hero_hp")

        self.enemy = QtWidgets.QLabel(self.centralwidget)
        self.enemy.setGeometry(QtCore.QRect(1450, 310, 141, 241))
        self.enemy.setText("enemy")
        self.enemy_hp = QtWidgets.QLabel(self.centralwidget)
        self.enemy_hp.setGeometry(QtCore.QRect(1440, 570, 55, 16))
        self.enemy_hp.setText("enemy_hp")

        self.setCentralWidget(self.centralwidget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMainWindow()

    window.show()
    sys.exit(app.exec())