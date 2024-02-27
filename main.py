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
        self.menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/menu_background1.png"))

        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(80, 550, 400, 100))
        self.play_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/play_button.png);}
                                                    QPushButton:hover {border-image: url(assets/menu/play_button_pointed.png);}
                                                    QPushButton:pressed {border-image: url(assets/menu/play_button_clicked.png);}''')

        self.parameters_button = QtWidgets.QPushButton(self.centralwidget)
        self.parameters_button.setGeometry(QtCore.QRect(80, 670, 600, 100))
        self.parameters_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/parametres.png);}
                                                    QPushButton:hover {border-image: url(assets/menu/parametres_pointed.png);}
                                                    QPushButton:pressed {border-image: url(assets/menu/parametres_clicked.png);}''')

        self.aboutgame_button = QtWidgets.QPushButton(self.centralwidget)
        self.aboutgame_button.setGeometry(QtCore.QRect(80, 780, 350, 100))
        self.aboutgame_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/aboutgame_button.png);}
                                                QPushButton:hover {border-image: url(assets/menu/aboutgame_button_pointed.png);}
                                                QPushButton:pressed {border-image: url(assets/menu/aboutgame_button_clicked.png);}''')

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(80, 890, 350, 100))
        self.exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit_button.png);}
                                                    QPushButton:hover {border-image: url(assets/menu/exit_button_pointed.png);}
                                                    QPushButton:pressed {border-image: url(assets/menu/exit_button_clicked.png);}''')
        self.exit_button.clicked.connect(self.exit_menu_open)

        self.setCentralWidget(self.centralwidget)

        self.exit_menu_label = QtWidgets.QLabel(self.centralwidget)
        self.exit_menu_label.setGeometry(QtCore.QRect(650, 500, 600, 200))
        self.exit_menu_label.setPixmap(QtGui.QPixmap("assets/menu/exit_confirm.png"))
        self.exit_menu_label.hide()

        self.exit_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.exit_cancel.setGeometry(QtCore.QRect(750, 625, 100, 30))
        self.exit_cancel.setText('отмена')
        self.exit_cancel.clicked.connect(self.exit_menu_close)
        self.exit_cancel.hide()

        self.exit_confirm = QtWidgets.QPushButton(self.centralwidget)
        self.exit_confirm.setGeometry(QtCore.QRect(1100, 625, 30, 30))
        self.exit_confirm.setText('да')
        self.exit_confirm.clicked.connect(exit)
        self.exit_confirm.hide()

    def exit_menu_open(self):
        self.exit_menu_label.show()
        self.exit_cancel.show()
        self.exit_confirm.show()
        self.play_button.hide()
        self.parameters_button.hide()
        self.aboutgame_button.hide()
        self.exit_button.hide()

    def exit_menu_close(self):
        self.exit_menu_label.hide()
        self.exit_cancel.hide()
        self.exit_confirm.hide()
        self.play_button.show()
        self.parameters_button.show()
        self.aboutgame_button.show()
        self.exit_button.show()


def start_application():
    app = QApplication(sys.argv)
    window = GameMainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_application()
