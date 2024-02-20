import sys
import hero
import enemies
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

enemy1 = enemies.Slime()
enemy2 = enemies.Warrior()
enemy3 = enemies.Spearman()
points = hero.player.max_action_points
card_is_chosen = False


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

        self.card1 = QtWidgets.QPushButton(self.centralwidget)
        self.card1.setGeometry(QtCore.QRect(400, 750, 200, 320))
        self.card1.setText("card1")
        #self.card1.clicked.connect(lambda: self.player_basic_attack())
        #self.card1.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/3attack.png);}
        #                                            QPushButton:hover {border-image: url(assets/ui/3attackhover.png);}''')

        self.card2 = QtWidgets.QPushButton(self.centralwidget)
        self.card2.setGeometry(QtCore.QRect(610, 750, 200, 320))
        self.card2.setText("card2")
        #self.card2.clicked.connect(lambda: self.player_basic_defence())

        self.card3 = QtWidgets.QPushButton(self.centralwidget)
        self.card3.setGeometry(QtCore.QRect(820, 750, 200, 320))
        self.card3.setText("card3")

        self.card4 = QtWidgets.QPushButton(self.centralwidget)
        self.card4.setGeometry(QtCore.QRect(1030, 750, 200, 320))
        self.card4.setText("card4")

        self.card5 = QtWidgets.QPushButton(self.centralwidget)
        self.card5.setGeometry(QtCore.QRect(1240, 750, 200, 320))
        self.card5.setText("card5")

        self.end_turn_button = QtWidgets.QPushButton(self.centralwidget)
        self.end_turn_button.setGeometry(QtCore.QRect(1700, 700, 160, 60))
        self.end_turn_button.setText("end_turn_button")
        self.end_turn_button.clicked.connect(lambda: self.end_turn())

        self.points_label = QtWidgets.QLabel(self.centralwidget)
        self.points_label.setGeometry(QtCore.QRect(170, 700, 60, 60))
        self.points_label.setText(str(points))

        self.hero = QtWidgets.QLabel(self.centralwidget)
        self.hero.setGeometry(QtCore.QRect(250, 310, 140, 240))
        self.hero.setText("hero")
        self.hero_hp = QtWidgets.QLabel(self.centralwidget)
        self.hero_hp.setGeometry(QtCore.QRect(250, 570, 140, 20))
        self.hero_hp.setText(str(hero.player.hp))
        self.hero_defence = QtWidgets.QLabel(self.centralwidget)
        self.hero_defence.setGeometry(QtCore.QRect(250, 620, 140, 20))
        self.hero_defence.setText(str(hero.player.def_points))

        if enemy1.hp > 0:
            self.enemy1_hp = QtWidgets.QLabel(self.centralwidget)
            self.enemy1_hp.setGeometry(QtCore.QRect(1440, 570, 55, 16))
            self.enemy1_hp.setText(str(enemy1.hp))
            self.enemy1_btn = QtWidgets.QPushButton(self.centralwidget)
            self.enemy1_btn.setGeometry(QtCore.QRect(1450, 310, 140, 240))
            self.enemy1_btn.setText(str(enemy1.name))

        if enemy2.hp > 0:
            self.enemy2_hp = QtWidgets.QLabel(self.centralwidget)
            self.enemy2_hp.setGeometry(QtCore.QRect(1290, 570, 55, 16))
            self.enemy2_hp.setText(str(enemy2.hp))
            self.enemy2_btn = QtWidgets.QPushButton(self.centralwidget)
            self.enemy2_btn.setGeometry(QtCore.QRect(1300, 310, 140, 240))
            self.enemy2_btn.setText(str(enemy2.name))

        if enemy3.hp > 0:
            self.enemy3_hp = QtWidgets.QLabel(self.centralwidget)
            self.enemy3_hp.setGeometry(QtCore.QRect(1590, 570, 55, 16))
            self.enemy3_hp.setText(str(enemy3.hp))
            self.enemy3_btn = QtWidgets.QPushButton(self.centralwidget)
            self.enemy3_btn.setGeometry(QtCore.QRect(1600, 310, 140, 240))
            self.enemy3_btn.setText(str(enemy3.name))

        self.setCentralWidget(self.centralwidget)

        hero.player.cards = [lambda: self.set_player_basic_attack(), lambda: self.set_player_basic_defence(),
                             lambda: self.set_player_basic_attack(), lambda: self.set_player_basic_defence(),
                             lambda: self.set_player_basic_attack(), lambda: self.set_player_basic_defence(),
                             lambda: self.set_player_basic_attack(), lambda: self.set_player_basic_defence(),
                             lambda: self.set_player_basic_attack(), lambda: self.set_player_basic_defence()]
        hero.player.active_cards = [''] * 5
        hero.player.played_cards = [''] * 5

    def end_turn(self):
        global points
        points = 0
        self.points_label.setText(str(points))
        if enemy1.hp > 0:
            QtCore.QTimer.singleShot(1000, lambda: self.enemy_attack(enemy1))
        if enemy2.hp > 0:
            QtCore.QTimer.singleShot(2000, lambda: self.enemy_attack(enemy2))
        if enemy3.hp > 0:
            QtCore.QTimer.singleShot(3000, lambda: self.enemy_attack(enemy3))
        QtCore.QTimer.singleShot(4000, lambda: self.new_turn())

    def new_turn(self):
        global points
        hero.player.def_points = 0
        self.hero_defence.setText(str(hero.player.def_points))
        points = hero.player.max_action_points
        self.points_label.setText(str(points))

    def check_and_reset(self, enemy_name, enemy_btn, enemy_hp_label):
        if enemy_name.hp > 0:
            enemy_btn.clicked.disconnect()
        else:
            enemy_btn.hide()
            enemy_hp_label.hide()

    def enemy_attack(self, enemy_name):
        if hero.player.def_points >= enemy_name.attack:
            hero.player.def_points -= enemy_name.attack
        else:
            hero.player.hp = hero.player.hp + hero.player.def_points - enemy_name.attack
            hero.player.def_points = 0
            self.hero_hp.setText(str(hero.player.hp))
        self.hero_defence.setText(str(hero.player.def_points))

    def set_cards(self):
        i = 0
        while '' in hero.player.active_cards:
            hero.player.active_cards[i] = random.choice(hero.player.cards)
            hero.player.cards[hero.player.cards.index(hero.player.active_cards[i])] = ''
            if not hero.player.active_cards[i] == '':
                i += 1

    def set_player_basic_attack(self):
        pass

    def set_player_basic_defence(self):
        pass

    def player_basic_defence(self):
        global points
        points -= 2
        hero.player.def_points += 3
        self.hero_defence.setText(str(hero.player.def_points))
        self.points_label.setText(str(points))

    def player_basic_attack(self):
        global card_is_chosen
        if not card_is_chosen:
            card_is_chosen = True
            #self.card.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/3attackhover.png);}
            #                                                    QPushButton:hover {border-image: url(assets/ui/3attackchosen.png);}''')
            if enemy1.hp > 0:
                self.enemy1_btn.clicked.connect(lambda: self.enemy_attacked(enemy1, self.enemy1_btn, self.enemy1_hp, self.card1))
            if enemy2.hp > 0:
                self.enemy2_btn.clicked.connect(lambda: self.enemy_attacked(enemy2, self.enemy2_btn, self.enemy2_hp, self.card1))
            if enemy3.hp > 0:
                self.enemy3_btn.clicked.connect(lambda: self.enemy_attacked(enemy3, self.enemy3_btn, self.enemy3_hp, self.card1))
        else:
            card_is_chosen = False
            #self.card.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/3attack.png);}
            #                                                    QPushButton:hover {border-image: url(assets/ui/3attackhover.png);}''')
            self.check_and_reset(enemy1, self.enemy1_btn, self.enemy1_hp)
            self.check_and_reset(enemy2, self.enemy2_btn, self.enemy2_hp)
            self.check_and_reset(enemy3, self.enemy3_btn, self.enemy3_hp)

    def enemy_attacked(self, enemy_name, enemy_btn, enemy_hp_label, card_name):
        global card_is_chosen, points
        points -= 3
        enemy_name.hp -= hero.player.attack
        enemy_hp_label.setText(str(enemy_name.hp))
        self.points_label.setText(str(points))
        card_is_chosen = False
        self.check_and_reset(enemy1, self.enemy1_btn, self.enemy1_hp)
        self.check_and_reset(enemy2, self.enemy2_btn, self.enemy2_hp)
        self.check_and_reset(enemy3, self.enemy3_btn, self.enemy3_hp)
        #card_name.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/3attack.png);}
        #                                                                        QPushButton:hover {border-image: url(assets/ui/3attackhover.png);}''')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMainWindow()

    window.show()
    sys.exit(app.exec())
