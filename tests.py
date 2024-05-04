import sys
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import hero
import enemies

red_points = hero.player.max_red_points
green_points = hero.player.max_green_points
blue_points = hero.player.max_blue_points
chosen_cards = [False] * 5


class BattleEnemy(enemies.Enemy):
    def __init__(self, enemy_name, cnt, window):
        super().__init__(enemy_name, cnt)
        self.enemy_hp = QtWidgets.QLabel(window.battlewidget)
        self.enemy_hp.setGeometry(QtCore.QRect(870 + 320 * self.number, 300, 100, 100))
        self.enemy_hp.setAlignment(QtCore.Qt.AlignCenter)
        self.enemy_hp.setText(str(self.hp))
        self.enemy_hp.setStyleSheet(
            "QLabel {font-family:monogram; font-size:64px; color: rgb(255,255,255);border-image: url(assets/ui/hp.png);}")

        self.enemy_def = QtWidgets.QLabel(window.battlewidget)
        self.enemy_def.setGeometry(QtCore.QRect(1080 + 320 * self.number, 300, 100, 100))
        self.enemy_def.setAlignment(QtCore.Qt.AlignCenter)
        self.enemy_def.setText(str(self.def_points))
        self.enemy_def.setStyleSheet(
            "QLabel {font-family:monogram; font-size:64px; color: rgb(255,255,255);border-image: url(assets/ui/defp.png);}")

        self.enemy_label = QtWidgets.QLabel(window.battlewidget)
        self.enemy_label.setGeometry(QtCore.QRect(860 + 320 * self.number, 150, self.x_size, self.y_size))
        self.enemy_idle = QtGui.QMovie(self.idle_gif)
        self.enemy_label.setMovie(self.enemy_idle)
        self.enemy_idle.start()

        self.enemy_btn = QtWidgets.QPushButton(window.battlewidget)
        self.enemy_btn.setGeometry(QtCore.QRect(860 + 320 * self.number, 150, self.x_size, self.y_size))
        self.enemy_btn.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')

        self.run_movie = QtGui.QMovie(self.run_gif)
        self.run_animation = QtCore.QPropertyAnimation(self.enemy_label, b"geometry")
        self.run_animation.setDuration(500)
        self.run_animation.setStartValue(QtCore.QRect(860 + 320 * self.number, 150, 550, 550))
        self.run_animation.setEndValue(QtCore.QRect(300, 150, 550, 550))

        self.run_back_movie = QtGui.QMovie(self.run_back_gif)
        self.run_back_animation = QtCore.QPropertyAnimation(self.enemy_label, b"geometry")
        self.run_back_animation.setDuration(500)
        self.run_back_animation.setStartValue(QtCore.QRect(300, 150, 550, 550))
        self.run_back_animation.setEndValue(QtCore.QRect(860 + 320 * self.number, 150, 550, 550))

        self.hurt_movie = QtGui.QMovie(self.hurt_gif)
        self.dead_movie = QtGui.QMovie(self.dead_gif)
        self.defend_movie = QtGui.QMovie(self.defend_gif)
        self.attack_movie = QtGui.QMovie(self.attack_gif)
    
    def hide_enemy(self):
        self.enemy_btn.hide()
        self.enemy_hp.hide()
        self.enemy_label.hide()
        self.enemy_def.hide()
        
    def show_enemy(self):
        self.enemy_btn.show()
        self.enemy_hp.show()
        self.enemy_label.show()
        self.enemy_def.show()


class BlankCard:
    def __init__(self, window, nbr):
        super().__init__()
        self.number = nbr
        self.card = QtWidgets.QPushButton(window.battlewidget)
        self.card.setGeometry(QtCore.QRect(380+210*nbr, 750, 200, 320))


class GameMainWindow(QMainWindow):
    def __init__(self):
        super(GameMainWindow, self).__init__()

        self.setWindowTitle('Card Dungeon')
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.showFullScreen()

        self.battlewidget = QtWidgets.QWidget(self)
        self.battlewidget.setObjectName("battlewidget")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.menu_background = QtWidgets.QLabel(self.centralwidget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/menu_background.png"))

        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(460, 430, 320, 120))
        self.play_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/play.png);}
                                                            QPushButton:hover {border-image: url(assets/menu/play_hover.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/play_pressed.png);}''')
        self.play_button.clicked.connect(lambda: self.play_game())

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(470, 690, 320, 160))
        self.exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit.png);}
                                                            QPushButton:hover {border-image: url(assets/menu/exit_hover.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/exit_pressed.png);}''')
        self.exit_button.clicked.connect(exit)

        self.menu_background = QtWidgets.QLabel(self.battlewidget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/battle_cave1.png"))

        self.ui = QtWidgets.QLabel(self.battlewidget)
        self.ui.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.ui.setPixmap(QtGui.QPixmap("assets/ui/ui.png"))

        self.exit_battle = QtWidgets.QPushButton(self.battlewidget)
        self.exit_battle.setGeometry(QtCore.QRect(1800, 30, 75, 75))
        self.exit_battle.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/settings.png);}
                                                                    QPushButton:hover {border-image: url(assets/ui/settings_hover.png);}
                                                                    QPushButton:pressed {border-image: url(assets/ui/settings_pressed.png);}''')
        self.exit_battle.clicked.connect(exit)

        self.deck = [BlankCard(self, 0), BlankCard(self, 1), BlankCard(self, 2), BlankCard(self, 3), BlankCard(self, 4)]

        self.end_turn_button = QtWidgets.QPushButton(self.battlewidget)
        self.end_turn_button.setGeometry(QtCore.QRect(1675, 775, 200, 100))
        self.end_turn_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn.png);}
                                                                        QPushButton:pressed {border-image: url(assets/ui/end_turn_pressed.png);}''')
        self.end_turn_button.clicked.connect(lambda: self.end_turn())

        self.red_points_label = QtWidgets.QLabel(self.battlewidget)
        self.red_points_label.setGeometry(QtCore.QRect(1550, 851, 56, 56))
        self.red_points_label.setStyleSheet("QLabel {font-family:monogram; font-size:96px; color: rgb(255,200,200);}")
        self.red_points_label.setText(str(red_points))

        self.green_points_label = QtWidgets.QLabel(self.battlewidget)
        self.green_points_label.setGeometry(QtCore.QRect(1550, 923, 56, 56))
        self.green_points_label.setStyleSheet("QLabel {font-family:monogram; font-size:96px; color: rgb(200,255,200);}")
        self.green_points_label.setText(str(green_points))

        self.blue_points_label = QtWidgets.QLabel(self.battlewidget)
        self.blue_points_label.setGeometry(QtCore.QRect(1550, 995, 56, 56))
        self.blue_points_label.setStyleSheet("QLabel {font-family:monogram; font-size:96px; color: rgb(200,200,255);}")
        self.blue_points_label.setText(str(blue_points))

        self.enemy = [BattleEnemy('blue_slime', 0, self),
                      BattleEnemy('blue_slime', 1, self),
                      BattleEnemy('blue_slime', 2, self)]

        self.hero = QtWidgets.QLabel(self.battlewidget)
        self.hero.setGeometry(QtCore.QRect(200, 320, 500, 400))
        self.hero_idle = QtGui.QMovie(hero.player.idle_animation)
        self.hero.setMovie(self.hero_idle)
        self.hero_idle.start()

        self.hero_basic_attack = QtGui.QMovie(hero.player.basic_attack_animation)
        self.hero_massive_attack = QtGui.QMovie(hero.player.massive_attack_animation)
        self.hero_pierce_attack = QtGui.QMovie(hero.player.pierce_attack_animation)
        self.hero_defend = QtGui.QMovie(hero.player.defence_animation)
        self.hero_hurt = QtGui.QMovie(hero.player.hurt_animation)

        self.animations = {
            'basic': {
                'animation':  self.hero_basic_attack,
                'ms': 600
            },
            'massive': {
                'animation': self.hero_massive_attack,
                'ms': 900
            },
            'pierce': {
                'animation': self.hero_pierce_attack,
                'ms': 600
            },
            'defend': {
                'animation': self.hero_defend,
                'ms': 450
            },
            'hurt': {
                'animation': self.hero_hurt,
                'ms': 250
            },
        }

        self.hero_run_movie = QtGui.QMovie("assets/heroes/knight/run.gif")
        self.hero_run_animation = QtCore.QPropertyAnimation(self.hero, b"geometry")
        self.hero_run_animation.setDuration(500)

        self.hero_run_back_movie = QtGui.QMovie("assets/heroes/knight/run_back.gif")
        self.hero_run_back_animation = QtCore.QPropertyAnimation(self.hero, b"geometry")
        self.hero_run_back_animation.setDuration(500)

        self.run_to_next_level_animation = QtCore.QPropertyAnimation(self.hero, b"geometry")
        self.run_to_next_level_animation.setDuration(1000)
        self.run_to_next_level_animation.setStartValue(QtCore.QRect(200, 320, 500, 400))
        self.run_to_next_level_animation.setEndValue(QtCore.QRect(1920, 320, 500, 400))

        self.hero_hp = QtWidgets.QLabel(self.battlewidget)
        self.hero_hp.setGeometry(QtCore.QRect(200, 750, 125, 125))
        self.hero_hp.setText(str(hero.player.hp))

        self.hero_defence = QtWidgets.QLabel(self.battlewidget)
        self.hero_defence.setGeometry(QtCore.QRect(200, 910, 125, 125))
        self.hero_defence.setText(str(hero.player.def_points))

        self.to_next_level_label = QtWidgets.QLabel(self.battlewidget)
        self.to_next_level_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.to_next_level_movie = QtGui.QMovie("assets/ui/next_level.gif")
        self.to_next_level_label.hide()

        self.setCentralWidget(self.centralwidget)

    def play_game(self):
        hero.player = hero.fighter
        for i in range(5):
            self.set_card(i)
        self.setCentralWidget(self.battlewidget)

    def end_turn(self):
        global chosen_cards
        if sum(chosen_cards) == 0:
            chosen_cards[0] = 1
            self.end_turn_button.setEnabled(False)
            self.end_turn_button.setStyleSheet(
                'QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn_pressed.png);}')
            if self.enemy[0].hp > 0:
                self.enemy[0].def_points = 0
                self.enemy[0].enemy_def.setText(str(self.enemy[0].def_points))
                QtCore.QTimer.singleShot(1000, lambda: self.enemy_turn(self.enemy[0]))
            if self.enemy[1].hp > 0:
                self.enemy[1].def_points = 0
                self.enemy[1].enemy_def.setText(str(self.enemy[1].def_points))
                QtCore.QTimer.singleShot(2500, lambda: self.enemy_turn(self.enemy[1]))
            if self.enemy[2].hp > 0:
                self.enemy[2].def_points = 0
                self.enemy[2].enemy_def.setText(str(self.enemy[2].def_points))
                QtCore.QTimer.singleShot(4000, lambda: self.enemy_turn(self.enemy[2]))
            QtCore.QTimer.singleShot(6000, lambda: self.new_turn())
            print('Конец хода - ', chosen_cards)
        print('Сумма выбранных кард - ', sum(chosen_cards))

    def new_turn(self):
        global red_points, green_points, blue_points
        hero.player.def_points = 0
        self.hero_defence.setText(str(hero.player.def_points))
        for i in range(5):
            self.get_points()
            self.set_card(i)
        self.update_points()
        self.end_turn_button.setEnabled(True)
        chosen_cards[0] = 0
        self.end_turn_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn.png);}
                                                                                QPushButton:pressed {border-image: url(assets/ui/end_turn_pressed.png);}''')

    def get_points(self):
        global red_points, green_points, blue_points
        arr = []
        if red_points < 3:
            arr += 'r'
        if green_points < 3:
            arr += 'g'
        if blue_points < 3:
            arr += 'b'
        if arr == []:
            arr += 'n'
        f = random.choice(arr)
        if f == 'r':
            red_points += 1
        elif f == 'g':
            green_points += 1
        elif f == 'b':
            blue_points += 1

    def set_card(self, card_is_chosen):
        r = random.randint(1, 3)
        # if card_name.disconnect():
        try:
            self.deck[card_is_chosen].card.clicked.disconnect()
        except:
            pass
        if r == 1:
            self.deck[card_is_chosen].card.clicked.connect(
                lambda: self.player_basic_attack(card_is_chosen, self.animations['basic']))
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet)
        elif r == 2:
            self.deck[card_is_chosen].card.clicked.connect(lambda: self.player_basic_defence(card_is_chosen))
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.defence_sheet)
        else:
            r = random.randint(1, 3)
            if r == 1:
                self.deck[card_is_chosen].card.clicked.connect(lambda: self.player_heal(card_is_chosen))
                self.deck[card_is_chosen].card.setStyleSheet(hero.player.special1_sheet)
            elif r == 2:
                self.deck[card_is_chosen].card.clicked.connect(lambda: self.player_massive_attack(card_is_chosen))
                self.deck[card_is_chosen].card.setStyleSheet(hero.player.special2_sheet)
            elif r == 3:
                self.deck[card_is_chosen].card.clicked.connect(
                    lambda: self.player_basic_attack(card_is_chosen, self.animations['pierce']))
                self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)

    def check(self, enemy_name):
        enemy_name.enemy_btn.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')
        if enemy_name.hp <= 0:
            enemy_name.enemy_label.setMovie(enemy_name.dead_movie)
            enemy_name.dead_movie.start()
            QtCore.QTimer.singleShot(900, lambda: enemy_name.dead_movie.stop())
            QtCore.QTimer.singleShot(900, lambda: enemy_name.hide_enemy())
        if (self.enemy[0].hp <= 0) and (self.enemy[1].hp <= 0) and (self.enemy[2].hp <= 0):
            QtCore.QTimer.singleShot(900, lambda: self.to_next_level())

    def update_points(self):
        self.red_points_label.setText(str(red_points))
        self.green_points_label.setText(str(green_points))
        self.blue_points_label.setText(str(blue_points))

    def update_hero(self):
        pass

    def idle_hero(self):
        self.hero.setMovie(self.hero_idle)
        self.hero_idle.start()

    def create_enemies(self):
        self.enemy[0] = BattleEnemy('warrior', 0, self)
        self.enemy[0].show_enemy()
        self.enemy[1] = BattleEnemy('spearman', 1, self)
        self.enemy[1].show_enemy()
        self.enemy[2] = BattleEnemy('warrior', 2, self)
        self.enemy[2].show_enemy()

    def to_next_level(self):
        self.to_next_level_label.show()
        self.hero.setMovie(self.hero_run_movie)
        self.hero_run_movie.start()
        self.run_to_next_level_animation.start()
        self.to_next_level_label.setMovie(self.to_next_level_movie)
        self.to_next_level_movie.start()
        QtCore.QTimer.singleShot(1000, lambda: self.idle_hero())
        QtCore.QTimer.singleShot(1100, lambda: self.hero.move(200, 320))
        QtCore.QTimer.singleShot(1100, lambda: self.create_enemies())
        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_movie.stop())
        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_label.hide())

    def running_hero(self, destination):
        self.hero_run_animation.setStartValue(QtCore.QRect(200, 320, 500, 400))
        self.hero_run_animation.setEndValue(QtCore.QRect(600 + 320 * destination, 320, 500, 400))
        self.hero.setMovie(self.hero_run_movie)
        self.hero_run_movie.start()
        self.hero_run_animation.start()

    def running_back_hero(self, destination):
        self.hero_run_back_animation.setStartValue(QtCore.QRect(600 + 320 * destination, 320, 500, 400))
        self.hero_run_back_animation.setEndValue(QtCore.QRect(200, 320, 500, 400))
        self.hero.setMovie(self.hero_run_back_movie)
        self.hero_run_back_movie.start()
        self.hero_run_back_animation.start()
        QtCore.QTimer.singleShot(500, lambda: self.idle_hero())

    def play_animation(self, type):
        self.hero.setMovie(type['animation'])
        type['animation'].start()
        QtCore.QTimer.singleShot(type['ms'], lambda: type['animation'].stop())

    def running_enemy(self, enemy_name):
        enemy_name.enemy_label.setMovie(enemy_name.run)
        enemy_name.run.start()
        enemy_name.run_animation.start()
        QtCore.QTimer.singleShot(500, lambda: enemy_name.run.stop())

    def run_n_play_animation(self, type, enemy_name):
        self.running_hero(enemy_name.number)
        QtCore.QTimer.singleShot(500, lambda: self.play_animation(type))
        QtCore.QTimer.singleShot(500+type['ms'], lambda: self.running_back_hero(enemy_name.number))
        print(enemy_name.number)

    def enemy_animation(self, enemy_name, animation):
        enemy_name.setMovie(animation)
        animation.start()
        QtCore.QTimer.singleShot(enemy_name.attack_ms, lambda: animation.stop())

    def enemy_turn(self, enemy_name):
        r = random.randint(1, 2)
        if r == 1:
            enemy_name.enemy_label.setMovie(enemy_name.run_movie)
            enemy_name.run_movie.start()
            enemy_name.run_animation.start()
            enemy_name.enemy_label.resize(enemy_name.y_size, enemy_name.y_size)
            QtCore.QTimer.singleShot(500, lambda: enemy_name.run_movie.stop())
            QtCore.QTimer.singleShot(500, lambda: enemy_name.enemy_label.setMovie(enemy_name.attack_movie))
            QtCore.QTimer.singleShot(500, lambda: enemy_name.attack_movie.start())
            QtCore.QTimer.singleShot(500 + enemy_name.attack_ms, lambda: enemy_name.attack_movie.stop())
            QtCore.QTimer.singleShot(500 + enemy_name.attack_ms, lambda: enemy_name.enemy_label.setMovie(enemy_name.run_back_movie))
            QtCore.QTimer.singleShot(500 + enemy_name.attack_ms, lambda: enemy_name.run_back_movie.start())
            QtCore.QTimer.singleShot(500 + enemy_name.attack_ms, lambda: enemy_name.run_back_animation.start())
            QtCore.QTimer.singleShot(1000 + enemy_name.attack_ms, lambda: enemy_name.run_back_movie.stop())
            QtCore.QTimer.singleShot(1000 + enemy_name.attack_ms, lambda: enemy_name.enemy_label.resize(enemy_name.x_size, enemy_name.y_size))
            QtCore.QTimer.singleShot(1000 + enemy_name.attack_ms, lambda: enemy_name.enemy_label.setMovie(enemy_name.enemy_idle))
            if hero.player.def_points >= enemy_name.attack:
                hero.player.def_points -= enemy_name.attack
            else:
                hero.player.hp = hero.player.hp + hero.player.def_points - enemy_name.attack
                hero.player.def_points = 0
                QtCore.QTimer.singleShot(800, lambda: self.hero_hp.setText(str(hero.player.hp)))
            QtCore.QTimer.singleShot(800, lambda: self.hero_defence.setText(str(hero.player.def_points)))
            QtCore.QTimer.singleShot(800, lambda: self.play_animation(self.animations['hurt']))
            QtCore.QTimer.singleShot(1300, lambda: self.idle_hero())
        elif r == 2:
            enemy_name.def_points += enemy_name.defence
            enemy_name.enemy_def.setText(str(enemy_name.def_points))
            enemy_name.enemy_label.setMovie(enemy_name.defend_movie)
            enemy_name.defend_movie.start()
            QtCore.QTimer.singleShot(500, lambda: enemy_name.defend_movie.stop())
            QtCore.QTimer.singleShot(500, lambda: enemy_name.enemy_label.setMovie(enemy_name.enemy_idle))

    def player_basic_defence(self, card_is_chosen):
        global blue_points
        if blue_points > 0 and sum(chosen_cards) == 0:
            self.play_animation(self.animations['defend'])
            QtCore.QTimer.singleShot(450, lambda: self.idle_hero())
            blue_points -= 1
            hero.player.def_points += 3
            self.hero_defence.setText(str(hero.player.def_points))
            self.update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def player_basic_attack(self, card_is_chosen, type):
        global chosen_cards, red_points, green_points
        if ((type['animation'] == self.hero_basic_attack) and (red_points > 0) and (green_points > 0)) or ((type['animation'] == self.hero_pierce_attack) and (red_points > 0) and (blue_points > 0)):
            if sum(chosen_cards) == 0:
                chosen_cards[card_is_chosen] = True
                if type['animation'] == self.hero_basic_attack:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet_active)
                elif type['animation'] == self.hero_pierce_attack:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet_active)
                if self.enemy[0].hp > 0:
                    self.enemy[0].enemy_btn.clicked.connect(
                        lambda: self.enemy_attacked(self.enemy[0], card_is_chosen, type))
                    self.enemy[0].enemy_btn.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
                if self.enemy[1].hp > 0:
                    self.enemy[1].enemy_btn.clicked.connect(
                        lambda: self.enemy_attacked(self.enemy[1], card_is_chosen, type))
                    self.enemy[1].enemy_btn.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
                if self.enemy[2].hp > 0:
                    self.enemy[2].enemy_btn.clicked.connect(
                        lambda: self.enemy_attacked(self.enemy[2], card_is_chosen, type))
                    self.enemy[2].enemy_btn.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
            else:
                if chosen_cards[card_is_chosen]:
                    self.check(self.enemy[0])
                    self.check(self.enemy[1])
                    self.check(self.enemy[2])
                chosen_cards[card_is_chosen] = False
                if type['animation'] == self.hero_basic_attack:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet)
                elif type['animation'] == self.hero_pierce_attack:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)
            print('Индекс - ', card_is_chosen)
            print('Выбор карты атаки - ', chosen_cards)

    def player_heal(self, card_is_chosen):
        global green_points
        if green_points > 1 and sum(chosen_cards) == 0:
            green_points -= 2
            hero.player.hp = min(hero.player.hp + 5, 15)
            self.hero_hp.setText(str(hero.player.hp))
            self.update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def player_massive_attack(self, card_is_chosen):
        global red_points
        if red_points == 3 and sum(chosen_cards) == 0:
            self.run_n_play_animation(self.animations['massive'], self.enemy[1])
            red_points -= 3
            if self.enemy[0].def_points >= hero.player.attack-1:
                self.enemy[0].def_points -= hero.player.attack-1
            else:
                self.enemy[0].hp = self.enemy[0].hp - (hero.player.attack-1 - self.enemy[0].def_points)
                self.enemy[0].def_points = 0
                QtCore.QTimer.singleShot(1100, lambda: self.enemy[0].enemy_hp.setText(str(self.enemy[0].hp)))
            QtCore.QTimer.singleShot(1100, lambda: self.enemy[0].enemy_def.setText(str(self.enemy[0].def_points)))
            if self.enemy[1].def_points >= hero.player.attack-1:
                self.enemy[1].def_points -= hero.player.attack-1
            else:
                self.enemy[1].hp = self.enemy[1].hp - (hero.player.attack-1 - self.enemy[1].def_points)
                self.enemy[1].def_points = 0
                QtCore.QTimer.singleShot(1100, lambda: self.enemy[1].enemy_hp.setText(str(self.enemy[1].hp)))
            QtCore.QTimer.singleShot(1100, lambda: self.enemy[1].enemy_def.setText(str(self.enemy[1].def_points)))
            if self.enemy[2].def_points >= hero.player.attack-1:
                self.enemy[2].def_points -= hero.player.attack-1
            else:
                self.enemy[2].hp = self.enemy[2].hp - (hero.player.attack-1 - self.enemy[2].def_points)
                self.enemy[2].def_points = 0
                QtCore.QTimer.singleShot(1100, lambda: self.enemy[2].enemy_hp.setText(str(self.enemy[2].hp)))
            QtCore.QTimer.singleShot(1100, lambda: self.enemy[2].enemy_def.setText(str(self.enemy[2].def_points)))
            QtCore.QTimer.singleShot(1300, lambda: self.enemy[0].enemy_hp.setText(str(self.enemy[0].hp)))
            QtCore.QTimer.singleShot(1300, lambda: self.enemy[1].enemy_hp.setText(str(self.enemy[1].hp)))
            QtCore.QTimer.singleShot(1300, lambda: self.enemy[2].enemy_hp.setText(str(self.enemy[2].hp)))
            QtCore.QTimer.singleShot(1300, lambda: self.check(self.enemy[0]))
            QtCore.QTimer.singleShot(1300, lambda: self.check(self.enemy[1]))
            QtCore.QTimer.singleShot(1300, lambda: self.check(self.enemy[2]))
            self.update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def card_is_active(self, card_is_chosen):
        chosen_cards[card_is_chosen] = False
        
    def enemy_attacked(self, enemy_name, card_is_chosen, type):
        global red_points, green_points, blue_points, chosen_cards
        enemy_name.enemy_btn.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')
        if self.enemy[0].hp > 0:
            self.enemy[0].enemy_btn.clicked.disconnect()
        if self.enemy[1].hp > 0:
            self.enemy[1].enemy_btn.clicked.disconnect()
        if self.enemy[2].hp > 0:
            self.enemy[2].enemy_btn.clicked.disconnect()
        self.run_n_play_animation(type, enemy_name)
        red_points -= 1
        if type['animation'] == self.hero_basic_attack:
            green_points -= 1
            if enemy_name.def_points >= hero.player.attack:
                enemy_name.def_points -= hero.player.attack
            else:
                enemy_name.hp = enemy_name.hp - (hero.player.attack - enemy_name.def_points)
                enemy_name.def_points = 0
                QtCore.QTimer.singleShot(1100, lambda: enemy_name.enemy_hp.setText(str(enemy_name.hp)))
            QtCore.QTimer.singleShot(1100, lambda: enemy_name.enemy_def.setText(str(enemy_name.def_points)))
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet)
        elif type['animation'] == self.hero_pierce_attack:
            blue_points -= 1
            enemy_name.hp = enemy_name.hp - (hero.player.attack - 1)
            QtCore.QTimer.singleShot(1100, lambda: enemy_name.enemy_hp.setText(str(enemy_name.hp)))
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)
        self.update_points()
        QtCore.QTimer.singleShot(2000, lambda: self.card_is_active(card_is_chosen))
        QtCore.QTimer.singleShot(1100, lambda: self.check(self.enemy[0]))
        QtCore.QTimer.singleShot(1100, lambda: self.check(self.enemy[1]))
        QtCore.QTimer.singleShot(1100, lambda: self.check(self.enemy[2]))
        self.deck[card_is_chosen].card.clicked.disconnect()
        self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)
        print('Атаковали врага - ', chosen_cards)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMainWindow()
    window.show()

    QtGui.QFontDatabase.addApplicationFont("assets/monogram.ttf")
    app.setStyleSheet("QLabel {font-family:monogram; font-size:128px; color: rgb(255,255,255);}")

    sys.exit(app.exec())
