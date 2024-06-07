import sys
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import hero
import enemies

red_points = hero.player.max_red_points
green_points = hero.player.max_green_points
blue_points = hero.player.max_blue_points
chosen_cards = [False] * 6
rnd = 0


class BattleEnemy():
    def __init__(self, enemy_class: enemies.Enemy, window):
        super().__init__()
        self.enemy = enemy_class
        self.enemy_hp = QtWidgets.QLabel(window.battlewidget)
        self.enemy_hp.setGeometry(QtCore.QRect(870 + 320 * self.enemy.number, 300, 100, 100))
        self.enemy_hp.setAlignment(QtCore.Qt.AlignCenter)
        self.enemy_hp.setText(str(self.enemy.hp))
        self.enemy_hp.setStyleSheet(
            "QLabel {font-family:monogram; font-size:64px; color: rgb(255,255,255);border-image: url(assets/ui/hp.png);}")

        self.enemy_def = QtWidgets.QLabel(window.battlewidget)
        self.enemy_def.setGeometry(QtCore.QRect(1080 + 320 * self.enemy.number, 300, 100, 100))
        self.enemy_def.setAlignment(QtCore.Qt.AlignCenter)
        self.enemy_def.setText(str(self.enemy.def_points))
        self.enemy_def.setStyleSheet(
            "QLabel {font-family:monogram; font-size:64px; color: rgb(255,255,255);border-image: url(assets/ui/defp.png);}")

        self.enemy_label = QtWidgets.QLabel(window.battlewidget)
        self.enemy_label.setGeometry(
            QtCore.QRect(860 + 320 * self.enemy.number, 150, self.enemy.x_size, self.enemy.y_size))
        self.enemy_idle = QtGui.QMovie(self.enemy.idle_gif)
        self.enemy_label.setMovie(self.enemy_idle)
        self.enemy_idle.start()

        self.enemy_btn = QtWidgets.QPushButton(window.battlewidget)
        self.enemy_btn.setGeometry(
            QtCore.QRect(860 + 320 * self.enemy.number, 150, self.enemy.x_size, self.enemy.y_size))
        self.enemy_btn.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')

        self.run_movie = QtGui.QMovie(self.enemy.run_gif)
        self.run_animation = QtCore.QPropertyAnimation(self.enemy_label, b"geometry")
        self.run_animation.setDuration(500)
        self.run_animation.setStartValue(QtCore.QRect(860 + 320 * self.enemy.number, 150, 550, 550))
        self.run_animation.setEndValue(QtCore.QRect(300, 150, 550, 550))

        self.run_back_movie = QtGui.QMovie(self.enemy.run_back_gif)
        self.run_back_animation = QtCore.QPropertyAnimation(self.enemy_label, b"geometry")
        self.run_back_animation.setDuration(500)
        self.run_back_animation.setStartValue(QtCore.QRect(300, 150, 550, 550))
        self.run_back_animation.setEndValue(QtCore.QRect(860 + 320 * self.enemy.number, 150, 550, 550))

        self.hurt_movie = QtGui.QMovie(self.enemy.hurt_gif)
        self.dead_movie = QtGui.QMovie(self.enemy.dead_gif)
        self.defend_movie = QtGui.QMovie(self.enemy.defend_gif)
        self.attack_movie = QtGui.QMovie(self.enemy.attack_gif)

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

    def reset_enemy(self):
        self.enemy_hp.setText(str(self.enemy.hp))
        self.enemy_def.setText(str(self.enemy.def_points))
        self.enemy_hp.show()
        self.enemy_def.show()

        self.enemy_idle = QtGui.QMovie(self.enemy.idle_gif)
        self.enemy_label.setMovie(self.enemy_idle)
        self.enemy_idle.start()

        self.run_movie = QtGui.QMovie(self.enemy.run_gif)
        self.run_back_movie = QtGui.QMovie(self.enemy.run_back_gif)
        self.hurt_movie = QtGui.QMovie(self.enemy.hurt_gif)
        self.dead_movie = QtGui.QMovie(self.enemy.dead_gif)
        self.defend_movie = QtGui.QMovie(self.enemy.defend_gif)
        self.attack_movie = QtGui.QMovie(self.enemy.attack_gif)


class BlankCard:
    def __init__(self, window, nbr):
        super().__init__()
        self.number = nbr
        self.card = QtWidgets.QPushButton(window.battlewidget)
        self.card.setGeometry(QtCore.QRect(380 + 210 * nbr, 750, 200, 320))


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

        self.start_game_label = QtWidgets.QLabel(self.centralwidget)
        self.start_game_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.start_game_movie = QtGui.QMovie("assets/menu/play.gif")
        self.start_game_label.setMovie(self.start_game_movie)

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
        self.exit_button.clicked.connect(lambda: self.exit_confirm())

        self.exit_confirm_label = QtWidgets.QLabel(self.centralwidget)
        self.exit_confirm_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.exit_confirm_label.setPixmap(QtGui.QPixmap("assets/menu/exit_confirm.png"))
        self.exit_confirm_label.hide()

        self.exit_confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_confirm_button.setGeometry(QtCore.QRect(1060, 600, 280, 110))
        self.exit_confirm_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit_confirm_button.png);}
                                                                   QPushButton:pressed {border-image: url(assets/menu/exit_confirm_button_pressed.png);}''')
        self.exit_confirm_button.clicked.connect(exit)
        self.exit_confirm_button.hide()

        self.exit_cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_cancel_button.setGeometry(QtCore.QRect(585, 600, 280, 110))
        self.exit_cancel_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit_cancel_button.png);}
                                                                           QPushButton:pressed {border-image: url(assets/menu/exit_cancel_button_pressed.png);}''')
        self.exit_cancel_button.clicked.connect(lambda: self.exit_confirm())
        self.exit_cancel_button.hide()

        self.menu_background = QtWidgets.QLabel(self.battlewidget)
        self.menu_background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/battle_cave.png"))

        self.ui = QtWidgets.QLabel(self.battlewidget)
        self.ui.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.ui.setPixmap(QtGui.QPixmap("assets/ui/ui.png"))

        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.level_label = QtWidgets.QLabel(self.battlewidget)
        self.level_label.setGeometry(QtCore.QRect(0, 0, 150, 50))
        self.level_label.setFont(font)
        self.level_label.setStyleSheet("color: white")
        self.level_label.setText(f"Уровень: {rnd}")

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

        self.enemy = [BattleEnemy(enemies.Enemy(random.choice(enemies.enemies_name_list), 0), self),
                      BattleEnemy(enemies.Enemy(random.choice(enemies.enemies_name_list), 1), self),
                      BattleEnemy(enemies.Enemy(random.choice(enemies.enemies_name_list), 2), self)]

        self.hero = QtWidgets.QLabel(self.battlewidget)
        self.hero.setGeometry(QtCore.QRect(200, 320, 500, 400))
        self.hero_idle = QtGui.QMovie(hero.player.idle_gif)
        self.hero.setMovie(self.hero_idle)
        self.hero_idle.start()

        self.hero_basic_attack_movie = QtGui.QMovie(hero.player.basic_attack_gif)
        self.hero_defend_movie = QtGui.QMovie(hero.player.defence_gif)
        self.hero_special1_movie = QtGui.QMovie(hero.player.special1_gif)
        self.hero_special2_movie = QtGui.QMovie(hero.player.special2_gif)
        self.hero_special3_movie = QtGui.QMovie(hero.player.special3_gif)
        self.hero_hurt_movie = QtGui.QMovie(hero.player.hurt_gif)

        self.hero_run_movie = QtGui.QMovie(hero.player.run_gif)
        self.hero_run_animation = QtCore.QPropertyAnimation(self.hero, b"geometry")
        self.hero_run_animation.setDuration(500)

        self.hero_run_back_movie = QtGui.QMovie(hero.player.run_back_gif)
        self.hero_run_back_animation = QtCore.QPropertyAnimation(self.hero, b"geometry")
        self.hero_run_back_animation.setDuration(500)

        self.run_to_next_level_animation = QtCore.QPropertyAnimation(self.hero, b"geometry")
        self.run_to_next_level_animation.setDuration(1000)
        self.run_to_next_level_animation.setStartValue(QtCore.QRect(200, 320, 500, 400))
        self.run_to_next_level_animation.setEndValue(QtCore.QRect(1920, 320, 500, 400))

        self.hero_is_dead_movie = QtGui.QMovie(hero.player.dead_gif)

        self.hero_hp = QtWidgets.QLabel(self.battlewidget)
        self.hero_hp.setGeometry(QtCore.QRect(200, 750, 125, 125))
        self.hero_hp.setStyleSheet("QLabel {font-family:monogram; font-size:128px; color: rgb(255,255,255);}")
        self.hero_hp.setText(str(hero.player.hp))

        self.hero_defence = QtWidgets.QLabel(self.battlewidget)
        self.hero_defence.setGeometry(QtCore.QRect(200, 910, 125, 125))
        self.hero_defence.setStyleSheet("QLabel {font-family:monogram; font-size:128px; color: rgb(255,255,255);}")
        self.hero_defence.setText(str(hero.player.def_points))

        self.menu_label = QtWidgets.QLabel(self.battlewidget)
        self.menu_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.menu_label.setPixmap(QtGui.QPixmap("assets/menu/menu.png"))
        self.menu_label.hide()

        self.menu_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_button.setGeometry(QtCore.QRect(1800, 30, 75, 75))
        self.menu_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/settings.png);}
                                                                            QPushButton:hover {border-image: url(assets/ui/settings_hover.png);}
                                                                            QPushButton:pressed {border-image: url(assets/ui/settings_pressed.png);}''')
        self.menu_button.clicked.connect(lambda: self.menu())

        self.menu_label.raise_()

        self.menu_continue_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_continue_button.setGeometry(QtCore.QRect(710, 305, 500, 100))
        self.menu_continue_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_continue_button.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/menu_continue_button_pressed.png);}''')
        self.menu_continue_button.clicked.connect(lambda: self.menu())
        self.menu_continue_button.hide()

        self.menu_replay_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_replay_button.setGeometry(QtCore.QRect(710, 420, 500, 100))
        self.menu_replay_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_replay_button.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/menu_replay_button_pressed.png);}''')
        self.menu_replay_button.clicked.connect(lambda: self.replay())
        self.menu_replay_button.hide()

        self.menu_exit_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_exit_button.setGeometry(QtCore.QRect(710, 535, 500, 100))
        self.menu_exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_exit_button.png);}
                                                                    QPushButton:pressed {border-image: url(assets/menu/menu_exit_button_pressed.png);}''')
        self.menu_exit_button.clicked.connect(exit)
        self.menu_exit_button.hide()

        self.to_next_level_label = QtWidgets.QLabel(self.battlewidget)
        self.to_next_level_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.to_next_level_movie = QtGui.QMovie("assets/ui/next_level.gif")
        self.to_next_level_label.setMovie(self.to_next_level_movie)
        self.to_next_level_label.hide()

        self.setCentralWidget(self.centralwidget)

    def reset_stats_n_enemies(self):
        global red_points, green_points, blue_points

        hero.player.hp = hero.player.max_hp
        hero.player.def_points = 0
        red_points = hero.player.max_red_points
        green_points = hero.player.max_green_points
        blue_points = hero.player.max_blue_points

        self.hero_hp.setText(str(hero.player.hp))
        self.hero_defence.setText(str(hero.player.def_points))

        self.stats_update_points()

        self.create_enemies()
        for i in range(5):
            self.set_card(i)

    def replay(self):
        global rnd

        rnd = 0
        self.menu()

        self.to_next_level_label.show()
        self.to_next_level_movie.start()

        QtCore.QTimer.singleShot(1200, lambda: self.reset_stats_n_enemies())
        QtCore.QTimer.singleShot(1200, lambda: self.hero.setMovie(self.hero_idle))

        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_movie.stop())
        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_label.hide())

    def menu(self):
        if self.menu_label.isHidden():
            self.menu_label.show()
            self.menu_continue_button.show()
            self.menu_replay_button.show()
            self.menu_exit_button.show()
        else:
            self.menu_label.hide()
            self.menu_continue_button.hide()
            self.menu_replay_button.hide()
            self.menu_exit_button.hide()

    def exit_confirm(self):
        if self.exit_confirm_label.isHidden():
            self.exit_confirm_label.show()
            self.exit_confirm_button.show()
            self.exit_cancel_button.show()
        else:
            self.exit_confirm_label.hide()
            self.exit_confirm_button.hide()
            self.exit_cancel_button.hide()

    def play_game(self):
        self.start_game_movie.start()
        self.start_game_label.raise_()

        self.to_next_level_label.show()
        self.to_next_level_movie.start()

        QtCore.QTimer.singleShot(2000, lambda: self.start_game_movie.stop())
        QtCore.QTimer.singleShot(1000, lambda: self.game_started())

    def game_started(self):
        hero.player = hero.fighter
        for i in range(5):
            self.set_card(i)
        self.create_enemies()
        self.setCentralWidget(self.battlewidget)

        QtCore.QTimer.singleShot(1000, lambda: self.to_next_level_movie.stop())
        QtCore.QTimer.singleShot(1000, lambda: self.to_next_level_label.hide())

    def func(self, animation):
        return animation.frameCount() * 150

    lambda animation: animation.frameCount() * 150

    def end_turn(self):
        global chosen_cards
        if sum(chosen_cards) == 0:
            chosen_cards[5] = True

            self.end_turn_button.setEnabled(False)
            self.end_turn_button.setStyleSheet(
                'QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn_pressed.png);}')
            self.menu_replay_button.setEnabled(False)
            self.menu_replay_button.setStyleSheet(
                '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_replay_button_pressed.png);}''')

            if self.enemy[0].enemy.hp > 0:
                self.enemy[0].enemy.def_points = 0
                self.enemy[0].enemy_def.setText(str(self.enemy[0].enemy.def_points))
                QtCore.QTimer.singleShot(1000, lambda: self.enemy_turn(self.enemy[0]))
            if self.enemy[1].enemy.hp > 0:
                self.enemy[1].enemy.def_points = 0
                self.enemy[1].enemy_def.setText(str(self.enemy[1].enemy.def_points))
                QtCore.QTimer.singleShot(1150 + (
                            self.enemy[0].run_movie.frameCount() + self.enemy[0].attack_movie.frameCount() + self.enemy[
                        0].run_back_movie.frameCount()) * 150, lambda: self.enemy_turn(self.enemy[1]))
            if self.enemy[2].enemy.hp > 0:
                self.enemy[2].enemy.def_points = 0
                self.enemy[2].enemy_def.setText(str(self.enemy[2].enemy.def_points))
                QtCore.QTimer.singleShot(1300 + (
                            self.enemy[1].run_movie.frameCount() + self.enemy[1].attack_movie.frameCount() + self.enemy[
                        1].run_back_movie.frameCount()) * 150, lambda: self.enemy_turn(self.enemy[2]))

            QtCore.QTimer.singleShot(1500 + (
                        self.enemy[2].run_movie.frameCount() + self.enemy[2].attack_movie.frameCount() + self.enemy[
                    2].run_back_movie.frameCount()) * 150, lambda: self.new_turn())
            print('Конец хода - ', chosen_cards)
        print('Сумма выбранных кард - ', sum(chosen_cards))

    def new_turn(self):
        global red_points, green_points, blue_points
        hero.player.def_points = 0
        self.hero_defence.setText(str(hero.player.def_points))
        if hero.player.hp > 0:
            for i in range(5):
                self.get_points()
                self.set_card(i)
            self.stats_update_points()
            chosen_cards[5] = False
            self.end_turn_button.setEnabled(True)
            self.menu_replay_button.setEnabled(True)
            self.end_turn_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn.png);}
                                                                                    QPushButton:pressed {border-image: url(assets/ui/end_turn_pressed.png);}''')
            self.menu_replay_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_replay_button.png);}
                                                                        QPushButton:pressed {border-image: url(assets/menu/menu_replay_button_pressed.png);}''')
        else:
            self.hero.setMovie(self.hero_is_dead_movie)
            self.hero_is_dead_movie.start()
            QtCore.QTimer.singleShot(1200, lambda: self.hero_is_dead_movie.stop())

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
                lambda: self.player_basic_attack(card_is_chosen, self.hero_basic_attack_movie))
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
                    lambda: self.player_basic_attack(card_is_chosen, self.hero_special3_movie))
                self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)

    def check(self, enemy_name):
        enemy_name.enemy_btn.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')
        if enemy_name.enemy.hp <= 0 and enemy_name.enemy.is_alive:
            enemy_name.enemy.is_alive = False

            enemy_name.enemy_label.setMovie(enemy_name.dead_movie)
            enemy_name.dead_movie.start()
            QtCore.QTimer.singleShot(enemy_name.dead_movie.frameCount() * 150 - 100,
                                     lambda: enemy_name.dead_movie.stop())

            enemy_name.enemy_hp.hide()
            enemy_name.enemy_def.hide()

        print(enemy_name.enemy.number, '. ', enemy_name.enemy.name, ' - ', enemy_name.enemy.is_alive)

    def stats_update_points(self):
        self.red_points_label.setText(str(red_points))
        self.green_points_label.setText(str(green_points))
        self.blue_points_label.setText(str(blue_points))

    def stats_update_enemies(self):
        for i in range(3):
            if self.enemy[i].enemy.hp > 0:
                self.enemy[i].enemy_hp.setText(str(self.enemy[i].enemy.hp))
                self.enemy[i].enemy_def.setText(str(self.enemy[i].enemy.def_points))

    def idle_hero(self):
        self.hero.setMovie(self.hero_idle)
        self.hero_idle.start()

    def create_enemies(self):
        global rnd
        rnd += 1
        self.level_label.setText(f"Уровень: {rnd}")
        if rnd == 5:
            self.enemy[0].enemy = enemies.Enemy(random.choice(enemies.enemies_name_list), 0)
            self.enemy[0].reset_enemy()
            self.enemy[1].enemy = enemies.Enemy(random.choice(enemies.bosses_name_list), 1)
            self.enemy[1].reset_enemy()
            self.enemy[2].enemy = enemies.Enemy(random.choice(enemies.enemies_name_list), 2)
            self.enemy[2].reset_enemy()
        else:
            for i in range(3):
                self.enemy[i].enemy = enemies.Enemy(random.choice(enemies.enemies_name_list), i)
                self.enemy[i].reset_enemy()

    def to_next_level(self):
        if (self.enemy[0].enemy.hp <= 0) and (self.enemy[1].enemy.hp <= 0) and (self.enemy[2].enemy.hp <= 0):
            self.to_next_level_label.show()

            self.hero.setMovie(self.hero_run_movie)
            self.hero_run_movie.start()
            self.run_to_next_level_animation.start()

            self.to_next_level_movie.start()

            QtCore.QTimer.singleShot(1000, lambda: self.idle_hero())
            QtCore.QTimer.singleShot(1100, lambda: self.hero.move(200, 320))

            QtCore.QTimer.singleShot(1200, lambda: self.create_enemies())

            QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_movie.stop())
            QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_label.hide())

            for i in range(5):
                self.set_card(i)

    def running_hero(self, destination):
        self.hero_run_animation.setStartValue(QtCore.QRect(200, 320, 500, 400))
        self.hero_run_animation.setEndValue(QtCore.QRect(600 + 320 * destination, 320, 500, 400))
        self.hero_run_animation.setDuration(500 + 150 * destination)
        self.hero.setMovie(self.hero_run_movie)
        self.hero_run_movie.start()
        self.hero_run_animation.start()

    def running_back_hero(self, destination):
        self.hero_run_back_animation.setStartValue(QtCore.QRect(600 + 320 * destination, 320, 500, 400))
        self.hero_run_back_animation.setEndValue(QtCore.QRect(200, 320, 500, 400))
        self.hero_run_back_animation.setDuration(500 + 150 * destination)
        self.hero.setMovie(self.hero_run_back_movie)
        self.hero_run_back_movie.start()
        self.hero_run_back_animation.start()
        QtCore.QTimer.singleShot(500 + 150 * destination, lambda: self.idle_hero())

    def play_animation(self, animation):
        self.hero.setMovie(animation)
        animation.start()
        QtCore.QTimer.singleShot(animation.frameCount() * 150, lambda: animation.stop())

    def running_enemy(self, enemy_name):
        enemy_name.enemy_label.setMovie(enemy_name.run)
        enemy_name.run.start()
        enemy_name.run_animation.start()
        QtCore.QTimer.singleShot(500 + 150 * enemy_name.enemy.number, lambda: enemy_name.run.stop())

    def run_n_play_animation(self, animation, enemy_name):
        self.running_hero(enemy_name.enemy.number)
        QtCore.QTimer.singleShot(500 + 150 * enemy_name.enemy.number, lambda: self.play_animation(animation))
        QtCore.QTimer.singleShot(500 + 150 * enemy_name.enemy.number + animation.frameCount() * 75,
                                 lambda: enemy_name.enemy_label.setMovie(enemy_name.hurt_movie))
        QtCore.QTimer.singleShot(500 + 150 * enemy_name.enemy.number + animation.frameCount() * 75,
                                 lambda: enemy_name.hurt_movie.start())
        QtCore.QTimer.singleShot(
            500 + 150 * enemy_name.enemy.number + animation.frameCount() * 75 + enemy_name.hurt_movie.frameCount() * 150,
            lambda: enemy_name.hurt_movie.stop())
        QtCore.QTimer.singleShot(
            500 + 150 * enemy_name.enemy.number + animation.frameCount() * 75 + enemy_name.hurt_movie.frameCount() * 150,
            lambda: enemy_name.enemy_label.setMovie(enemy_name.enemy_idle))
        QtCore.QTimer.singleShot(500 + 150 * enemy_name.enemy.number + animation.frameCount() * 150,
                                 lambda: self.running_back_hero(enemy_name.enemy.number))
        print(enemy_name.enemy.number)

    def enemy_animation(self, enemy_name, animation):
        enemy_name.setMovie(animation)
        animation.start()
        QtCore.QTimer.singleShot(animation.frameCount() * 150, lambda: animation.stop())

    def enemy_turn(self, enemy_name):
        r = random.randint(1, 2)
        if r == 1:
            enemy_name.enemy_label.setMovie(enemy_name.run_movie)
            enemy_name.run_movie.start()
            enemy_name.run_animation.setDuration(500 + enemy_name.enemy.number * 150)
            enemy_name.run_back_animation.setDuration(500 + enemy_name.enemy.number * 150)
            enemy_name.run_animation.start()
            enemy_name.enemy_label.resize(enemy_name.enemy.y_size, enemy_name.enemy.y_size)
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150, lambda: enemy_name.run_movie.stop())
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150,
                                     lambda: enemy_name.enemy_label.setMovie(enemy_name.attack_movie))
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150, lambda: enemy_name.attack_movie.start())

            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.attack_movie.stop())
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.enemy_label.setMovie(enemy_name.run_back_movie))
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.run_back_movie.start())
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.run_back_animation.start())

            QtCore.QTimer.singleShot(1000 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.run_back_movie.stop())
            QtCore.QTimer.singleShot(1000 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.enemy_label.resize(enemy_name.enemy.x_size,
                                                                           enemy_name.enemy.y_size))
            QtCore.QTimer.singleShot(1000 + enemy_name.enemy.number * 150 + enemy_name.attack_movie.frameCount() * 150,
                                     lambda: enemy_name.enemy_label.setMovie(enemy_name.enemy_idle))

            if hero.player.def_points >= enemy_name.enemy.attack:
                hero.player.def_points -= enemy_name.enemy.attack
            else:
                hero.player.hp = hero.player.hp + hero.player.def_points - enemy_name.enemy.attack
                hero.player.def_points = 0
                QtCore.QTimer.singleShot(800, lambda: self.hero_hp.setText(str(hero.player.hp)))
            QtCore.QTimer.singleShot(800, lambda: self.hero_defence.setText(str(hero.player.def_points)))

            QtCore.QTimer.singleShot(800, lambda: self.play_animation(self.hero_hurt_movie))
            QtCore.QTimer.singleShot(1300, lambda: self.idle_hero())

        elif r == 2:
            enemy_name.enemy.def_points += enemy_name.enemy.defence
            enemy_name.enemy_def.setText(str(enemy_name.enemy.def_points))

            enemy_name.enemy_label.setMovie(enemy_name.defend_movie)
            enemy_name.defend_movie.start()
            QtCore.QTimer.singleShot(enemy_name.defend_movie.frameCount() * 150, lambda: enemy_name.defend_movie.stop())
            QtCore.QTimer.singleShot(enemy_name.defend_movie.frameCount() * 150,
                                     lambda: enemy_name.enemy_label.setMovie(enemy_name.enemy_idle))

    def player_basic_defence(self, card_is_chosen):
        global blue_points
        if blue_points > 0 and sum(chosen_cards) == 0:
            self.play_animation(self.hero_defend_movie)
            QtCore.QTimer.singleShot(self.hero_defend_movie.frameCount() * 150, lambda: self.idle_hero())
            blue_points -= 1
            hero.player.def_points += 3
            self.hero_defence.setText(str(hero.player.def_points))
            self.stats_update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def player_basic_attack(self, card_is_chosen, animation):
        global chosen_cards, red_points, green_points
        if ((animation == self.hero_basic_attack_movie) and (red_points > 0) and (green_points > 0)) or (
                (animation == self.hero_special3_movie) and (red_points > 0) and (blue_points > 0)):
            if sum(chosen_cards) == 0:
                chosen_cards[card_is_chosen] = True
                if animation == self.hero_basic_attack_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet_active)
                elif animation == self.hero_special3_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet_active)
                if self.enemy[0].enemy.hp > 0:
                    self.enemy[0].enemy_btn.clicked.connect(
                        lambda: self.enemy_attacked(self.enemy[0], card_is_chosen, animation))
                    self.enemy[0].enemy_btn.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
                if self.enemy[1].enemy.hp > 0:
                    self.enemy[1].enemy_btn.clicked.connect(
                        lambda: self.enemy_attacked(self.enemy[1], card_is_chosen, animation))
                    self.enemy[1].enemy_btn.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
                if self.enemy[2].enemy.hp > 0:
                    self.enemy[2].enemy_btn.clicked.connect(
                        lambda: self.enemy_attacked(self.enemy[2], card_is_chosen, animation))
                    self.enemy[2].enemy_btn.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
            else:
                if chosen_cards[card_is_chosen]:
                    for i in range(3):
                        self.check(self.enemy[i])
                        if self.enemy[i].enemy.hp > 0:
                            self.enemy[i].enemy_btn.clicked.disconnect()
                    chosen_cards[card_is_chosen] = False
                if animation == self.hero_basic_attack_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet)
                elif animation == self.hero_special3_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)
            print('Индекс - ', card_is_chosen)
            print('Выбор карты атаки - ', chosen_cards)

    def player_heal(self, card_is_chosen):
        global green_points
        if green_points > 1 and sum(chosen_cards) == 0:
            green_points -= 2
            hero.player.hp = min(hero.player.hp + 5, 15)
            self.hero_hp.setText(str(hero.player.hp))
            self.stats_update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)
            self.play_animation(self.hero_special1_movie)
            QtCore.QTimer.singleShot(self.hero_special1_movie.frameCount() * 150, lambda: self.idle_hero())

    def player_massive_attack(self, card_is_chosen):
        global red_points
        if red_points == 3 and sum(chosen_cards) == 0:
            self.run_n_play_animation(self.hero_special2_movie, self.enemy[1])
            red_points -= 3
            for i in range(3):
                if self.enemy[i].enemy.def_points >= hero.player.attack - 1:
                    self.enemy[i].enemy.def_points -= hero.player.attack - 1
                else:
                    self.enemy[i].enemy.hp = self.enemy[i].enemy.hp - (
                                hero.player.attack - 1 - self.enemy[i].enemy.def_points)
                    self.enemy[i].enemy.def_points = 0

            QtCore.QTimer.singleShot(1100, lambda: self.stats_update_enemies())

            QtCore.QTimer.singleShot(1400, lambda: self.check(self.enemy[0]))
            QtCore.QTimer.singleShot(1400, lambda: self.check(self.enemy[1]))
            QtCore.QTimer.singleShot(1400, lambda: self.check(self.enemy[2]))

            QtCore.QTimer.singleShot(2200, lambda: self.to_next_level())
            self.stats_update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def card_is_active(self, card_is_chosen):
        chosen_cards[card_is_chosen] = False

    def enemy_attacked(self, enemy_name, card_is_chosen, animation):
        global red_points, green_points, blue_points, chosen_cards
        enemy_name.enemy_btn.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')
        if self.enemy[0].enemy.hp > 0:
            self.enemy[0].enemy_btn.clicked.disconnect()
        if self.enemy[1].enemy.hp > 0:
            self.enemy[1].enemy_btn.clicked.disconnect()
        if self.enemy[2].enemy.hp > 0:
            self.enemy[2].enemy_btn.clicked.disconnect()
        self.run_n_play_animation(animation, enemy_name)
        red_points -= 1
        if animation == self.hero_basic_attack_movie:
            green_points -= 1
            if enemy_name.enemy.def_points >= hero.player.attack:
                enemy_name.enemy.def_points -= hero.player.attack
            else:
                enemy_name.enemy.hp = enemy_name.enemy.hp - (hero.player.attack - enemy_name.enemy.def_points)
                enemy_name.enemy.def_points = 0
                QtCore.QTimer.singleShot(1100, lambda: enemy_name.enemy_hp.setText(str(enemy_name.enemy.hp)))
            QtCore.QTimer.singleShot(1100, lambda: enemy_name.enemy_def.setText(str(enemy_name.enemy.def_points)))
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet)
        elif animation == self.hero_special3_movie:
            blue_points -= 1
            enemy_name.enemy.hp = enemy_name.enemy.hp - (hero.player.attack - 1)
            QtCore.QTimer.singleShot(1100, lambda: enemy_name.enemy_hp.setText(str(enemy_name.enemy.hp)))
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)
        self.stats_update_points()
        QtCore.QTimer.singleShot(2000, lambda: self.card_is_active(card_is_chosen))
        QtCore.QTimer.singleShot(1400, lambda: self.check(self.enemy[0]))
        QtCore.QTimer.singleShot(1400, lambda: self.check(self.enemy[1]))
        QtCore.QTimer.singleShot(1400, lambda: self.check(self.enemy[2]))
        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level())
        self.deck[card_is_chosen].card.clicked.disconnect()
        self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)
        print('Атаковали врага - ', chosen_cards)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMainWindow()
    window.show()

    QtGui.QFontDatabase.addApplicationFont("assets/monogram.ttf")

    sys.exit(app.exec())
