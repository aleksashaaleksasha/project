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
        self.menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/birch_summer.png"))

        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(750, 550, 400, 100))
        self.play_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/play_button.png);}
                                        QPushButton:hover {border-image: url(assets/menu/play_button_pointed.png);}
                                        QPushButton:pressed {border-image: url(assets/menu/play_button_clicked.png);}''')

        self.aboutgame_button = QtWidgets.QPushButton(self.centralwidget)
        self.aboutgame_button.setGeometry(QtCore.QRect(750, 670, 400, 100))
        self.aboutgame_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/aboutgame_button.png);}
                                                QPushButton:hover {border-image: url(assets/menu/aboutgame_button_pointed.png);}
                                                QPushButton:pressed {border-image: url(assets/menu/aboutgame_button_clicked.png);}''')

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(770, 780, 350, 100))
        self.exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit_button.png);}
                                                QPushButton:hover {border-image: url(assets/menu/exit_button_pointed.png);}
                                                QPushButton:pressed {border-image: url(assets/menu/exit_button_clicked.png);}''')
        self.exit_button.clicked.connect(self.exit_game)

        self.setCentralWidget(self.centralwidget)

        self.exit_menu = QtWidgets.QLabel(self.centralwidget)
        self.exit_menu.setGeometry(QtCore.QRect(650, 500, 600, 200))
        self.exit_menu.setPixmap(QtGui.QPixmap("assets/menu/exit_menu.png"))
        self.exit_menu.hide()

    def exit_game(self):
        self.exit_menu.show()


def start_application():
    app = QApplication(sys.argv)
    window = GameMainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_application()
