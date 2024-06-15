import sys
import random

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QApplication, QMainWindow

import hero
import enemies


class BattleEnemy:
    def __init__(self, enemy_class: enemies.Enemy, widget):
        super().__init__()
        self.enemy = enemy_class
        self.hp = QtWidgets.QLabel(widget)
        self.hp.setGeometry(QtCore.QRect(870 + 320 * self.enemy.number, 300, 100, 100))
        self.hp.setAlignment(QtCore.Qt.AlignCenter)
        self.hp.setText(str(self.enemy.hp))
        self.hp.setStyleSheet(
            "QLabel {font-family:monogram; font-size:64px; color: rgb(255,255,255);border-image: url(assets/ui/hp.png);}")

        self.defence = QtWidgets.QLabel(widget)
        self.defence.setGeometry(QtCore.QRect(1080 + 320 * self.enemy.number, 300, 100, 100))
        self.defence.setAlignment(QtCore.Qt.AlignCenter)
        self.defence.setText(str(self.enemy.def_points))
        self.defence.setStyleSheet(
            "QLabel {font-family:monogram; font-size:64px; color: rgb(255,255,255);border-image: url(assets/ui/defp.png);}")

        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(
            QtCore.QRect(860 + 320 * self.enemy.number, 150, self.enemy.x_size, self.enemy.y_size))
        self.idle = QtGui.QMovie(self.enemy.idle_gif)
        self.label.setMovie(self.idle)
        self.idle.start()

        self.button = QtWidgets.QPushButton(widget)
        self.button.setGeometry(
            QtCore.QRect(860 + 320 * self.enemy.number, 150, self.enemy.x_size, self.enemy.y_size))
        self.button.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')

        self.run_movie = QtGui.QMovie(self.enemy.run_gif)
        self.run_animation = QtCore.QPropertyAnimation(self.label, b"geometry")
        self.run_animation.setDuration(500)
        self.run_animation.setStartValue(QtCore.QRect(860 + 320 * self.enemy.number, 150, 550, 550))
        self.run_animation.setEndValue(QtCore.QRect(300, 150, 550, 550))

        self.run_back_movie = QtGui.QMovie(self.enemy.run_back_gif)
        self.run_back_animation = QtCore.QPropertyAnimation(self.label, b"geometry")
        self.run_back_animation.setDuration(500)
        self.run_back_animation.setStartValue(QtCore.QRect(300, 150, 550, 550))
        self.run_back_animation.setEndValue(QtCore.QRect(860 + 320 * self.enemy.number, 150, 550, 550))

        self.hurt_movie = QtGui.QMovie(self.enemy.hurt_gif)
        self.dead_movie = QtGui.QMovie(self.enemy.dead_gif)
        self.defend_movie = QtGui.QMovie(self.enemy.defend_gif)
        self.attack_movie = QtGui.QMovie(self.enemy.attack_1_gif)

    def hide_enemy(self):
        self.button.hide()
        self.hp.hide()
        self.label.hide()
        self.defence.hide()

    def show_enemy(self):
        self.button.show()
        self.hp.show()
        self.label.show()
        self.defence.show()

    def reset_enemy(self):
        self.hp.setText(str(self.enemy.hp))
        self.defence.setText(str(self.enemy.def_points))
        self.hp.show()
        self.defence.show()

        self.idle = QtGui.QMovie(self.enemy.idle_gif)
        self.label.setMovie(self.idle)
        self.idle.start()

        self.run_movie = QtGui.QMovie(self.enemy.run_gif)
        self.run_back_movie = QtGui.QMovie(self.enemy.run_back_gif)
        self.hurt_movie = QtGui.QMovie(self.enemy.hurt_gif)
        self.dead_movie = QtGui.QMovie(self.enemy.dead_gif)
        self.defend_movie = QtGui.QMovie(self.enemy.defend_gif)
        self.attack_movie = QtGui.QMovie(self.enemy.attack_1_gif)

    def clear_button(self):
        if self.enemy.is_alive:
            self.button.setStyleSheet('QPushButton {border: none;margin: 0px;padding: 0px;}')
            self.button.clicked.disconnect()


class BlankCard:
    def __init__(self, window, nbr):
        super().__init__()
        self.number = nbr
        self.card = QtWidgets.QPushButton(window.battlewidget)
        self.card.setGeometry(QtCore.QRect(380 + 210 * nbr, 750, 200, 320))


class GameMainWindow(QMainWindow):
    def __init__(self):
        super(GameMainWindow, self).__init__()

        self.setWindowTitle('Пещера карт')
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.showFullScreen()

        self.main_menu_widget = QtWidgets.QWidget(self)
        self.main_menu_widget.setObjectName("main_menu_widget")

        self.battlewidget = QtWidgets.QWidget(self)
        self.battlewidget.setObjectName("battlewidget")

        self.button_sound = QtMultimedia.QSoundEffect()
        self.button_sound.setSource(QtCore.QUrl.fromLocalFile("assets/sounds/btn.wav"))
        self.button_sound.setVolume(0.5)

        self.hurt_sound = QtMultimedia.QSoundEffect()
        self.hurt_sound.setSource(QtCore.QUrl.fromLocalFile("assets/sounds/hurt.wav"))
        self.hurt_sound.setVolume(0.5)

        self.utility_sound = QtMultimedia.QSoundEffect()
        self.utility_sound.setSource(QtCore.QUrl.fromLocalFile("assets/sounds/utility.wav"))
        self.utility_sound.setVolume(0.05)

        self.main_menu_background = QtWidgets.QLabel(self.main_menu_widget)
        self.main_menu_background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.main_menu_background.setPixmap(QtGui.QPixmap("assets/backgrounds/menu_background.png"))

        self.start_game_label = QtWidgets.QLabel(self.main_menu_widget)
        self.start_game_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.start_game_movie = QtGui.QMovie("assets/menu/play.gif")
        self.start_game_label.setMovie(self.start_game_movie)

        self.main_play_button = QtWidgets.QPushButton(self.main_menu_widget)
        self.main_play_button.setGeometry(QtCore.QRect(460, 430, 320, 120))
        self.main_play_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/play.png);}
                                                            QPushButton:hover {border-image: url(assets/menu/play_hover.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/play_pressed.png);}''')
        self.main_play_button.clicked.connect(lambda: self.play_game())

        self.main_exit_button = QtWidgets.QPushButton(self.main_menu_widget)
        self.main_exit_button.setGeometry(QtCore.QRect(470, 690, 320, 160))
        self.main_exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit.png);}
                                                            QPushButton:hover {border-image: url(assets/menu/exit_hover.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/exit_pressed.png);}''')
        self.main_exit_button.clicked.connect(sys.exit)

        self.battle_background = QtWidgets.QLabel(self.battlewidget)
        self.battle_background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.battle_background.setPixmap(QtGui.QPixmap("assets/backgrounds/battle_cave.png"))

        self.ui = QtWidgets.QLabel(self.battlewidget)
        self.ui.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.ui.setPixmap(QtGui.QPixmap("assets/ui/ui.png"))

        self.font = QtGui.QFont()
        self.font.setFamily("MS Serif")
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.font.setWeight(75)

        self.rnd = 0

        self.level_label = QtWidgets.QLabel(self.battlewidget)
        self.level_label.setGeometry(QtCore.QRect(45, 10, 150, 50))
        self.level_label.setFont(self.font)
        self.level_label.setStyleSheet("color: white")
        self.level_label.setText(f"Уровень: {self.rnd}")

        self.deck = [BlankCard(self, 0), BlankCard(self, 1), BlankCard(self, 2), BlankCard(self, 3), BlankCard(self, 4)]

        self.end_turn_button = QtWidgets.QPushButton(self.battlewidget)
        self.end_turn_button.setGeometry(QtCore.QRect(1675, 775, 200, 100))
        self.end_turn_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn.png);}
                                                                        QPushButton:pressed {border-image: url(assets/ui/end_turn_pressed.png);}''')
        self.end_turn_button.clicked.connect(lambda: self.end_turn())

        self.red_points_label = QtWidgets.QLabel(self.battlewidget)
        self.red_points_label.setGeometry(QtCore.QRect(1550, 851, 56, 56))
        self.red_points_label.setStyleSheet("QLabel {font-family:monogram; font-size:96px; color: rgb(255,200,200);}")
        self.red_points_label.setText(str(hero.player.red_points))

        self.green_points_label = QtWidgets.QLabel(self.battlewidget)
        self.green_points_label.setGeometry(QtCore.QRect(1550, 923, 56, 56))
        self.green_points_label.setStyleSheet("QLabel {font-family:monogram; font-size:96px; color: rgb(200,255,200);}")
        self.green_points_label.setText(str(hero.player.green_points))

        self.blue_points_label = QtWidgets.QLabel(self.battlewidget)
        self.blue_points_label.setGeometry(QtCore.QRect(1550, 995, 56, 56))
        self.blue_points_label.setStyleSheet("QLabel {font-family:monogram; font-size:96px; color: rgb(200,200,255);}")
        self.blue_points_label.setText(str(hero.player.blue_points))

        self.enemy = [BattleEnemy(enemies.Enemy(random.choice(enemies.enemies_name_list), 0), self.battlewidget),
                      BattleEnemy(enemies.Enemy(random.choice(enemies.enemies_name_list), 1), self.battlewidget),
                      BattleEnemy(enemies.Enemy(random.choice(enemies.enemies_name_list), 2), self.battlewidget)]

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
        self.menu_button.setGeometry(QtCore.QRect(1800, 15, 75, 75))
        self.menu_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/settings.png);}
                                                                            QPushButton:hover {border-image: url(assets/ui/settings_hover.png);}
                                                                            QPushButton:pressed {border-image: url(assets/ui/settings_pressed.png);}''')
        self.menu_button.clicked.connect(lambda: self.menu())

        self.menu_label.raise_()

        self.menu_continue_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_continue_button.setGeometry(QtCore.QRect(710, 275, 500, 100))
        self.menu_continue_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_continue_button.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/menu_continue_button_pressed.png);}''')
        self.menu_continue_button.clicked.connect(lambda: self.menu())
        self.menu_continue_button.hide()

        self.menu_replay_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_replay_button.setGeometry(QtCore.QRect(710, 385, 500, 100))
        self.menu_replay_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_replay_button.png);}
                                                            QPushButton:pressed {border-image: url(assets/menu/menu_replay_button_pressed.png);}''')
        self.menu_replay_button.clicked.connect(lambda: self.replay())
        self.menu_replay_button.hide()

        self.menu_exit_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_exit_button.setGeometry(QtCore.QRect(710, 495, 500, 100))
        self.menu_exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_exit_button.png);}
                                                                    QPushButton:pressed {border-image: url(assets/menu/menu_exit_button_pressed.png);}''')
        self.menu_exit_button.clicked.connect(lambda: self.exit_confirm())
        self.menu_exit_button.hide()

        self.menu_tutorial_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_tutorial_button.setGeometry(QtCore.QRect(710, 600, 75, 75))
        self.menu_tutorial_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/tutorial.png);}
                                                                    QPushButton:hover {border-image: url(assets/ui/tutorial_hover.png);}
                                                                    QPushButton:pressed {border-image: url(assets/ui/tutorial_pressed.png);}''')
        self.menu_tutorial_button.clicked.connect(lambda: self.tutorial_next())
        self.menu_tutorial_button.hide()

        self.sound_is_enabled = True
        self.menu_sound_button = QtWidgets.QPushButton(self.battlewidget)
        self.menu_sound_button.setGeometry(QtCore.QRect(1130, 600, 75, 75))
        self.menu_sound_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/sound_button.png);}
                                                                            QPushButton:hover {border-image: url(assets/ui/sound_button_hover.png);}''')
        self.menu_sound_button.clicked.connect(lambda: self.sound_enabler())
        self.menu_sound_button.hide()

        self.tutorial_page_count = 1
        self.tutorial_label = QtWidgets.QLabel(self.battlewidget)
        self.tutorial_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.tutorial_label.setPixmap(QtGui.QPixmap("assets/backgrounds/tutorial1.png"))
        self.tutorial_label.mousePressEvent = lambda _: self.tutorial_next()

        self.end_game_label = QtWidgets.QLabel(self.battlewidget)
        self.end_game_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.end_game_label.hide()

        self.end_game_exit_button = QtWidgets.QPushButton(self.battlewidget)
        self.end_game_exit_button.setGeometry(QtCore.QRect(1320, 750, 350, 100))
        self.end_game_exit_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_game_exit_button.png);}
                                                                    QPushButton:pressed {border-image: url(assets/ui/end_game_exit_button_pressed.png);}''')
        self.end_game_exit_button.clicked.connect(lambda: self.exit_confirm())
        self.end_game_exit_button.hide()

        self.end_game_replay_button = QtWidgets.QPushButton(self.battlewidget)
        self.end_game_replay_button.setGeometry(QtCore.QRect(259, 750, 350, 100))
        self.end_game_replay_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_game_replay_button.png);}
                                                                            QPushButton:pressed {border-image: url(assets/ui/end_game_replay_button_pressed.png);}''')
        self.end_game_replay_button.clicked.connect(lambda: self.replay())
        self.end_game_replay_button.hide()

        self.exit_confirm_label = QtWidgets.QLabel(self.battlewidget)
        self.exit_confirm_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.exit_confirm_label.setPixmap(QtGui.QPixmap("assets/menu/exit_confirm.png"))
        self.exit_confirm_label.hide()

        self.exit_confirm_button = QtWidgets.QPushButton(self.battlewidget)
        self.exit_confirm_button.setGeometry(QtCore.QRect(1095, 510, 230, 95))
        self.exit_confirm_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit_confirm_button.png);}
                                                                           QPushButton:pressed {border-image: url(assets/menu/exit_confirm_button_pressed.png);}''')
        self.exit_confirm_button.clicked.connect(sys.exit)
        self.exit_confirm_button.hide()

        self.exit_cancel_button = QtWidgets.QPushButton(self.battlewidget)
        self.exit_cancel_button.setGeometry(QtCore.QRect(600, 510, 230, 95))
        self.exit_cancel_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/exit_cancel_button.png);}
                                                                                   QPushButton:pressed {border-image: url(assets/menu/exit_cancel_button_pressed.png);}''')
        self.exit_cancel_button.clicked.connect(lambda: self.exit_confirm())
        self.exit_cancel_button.hide()

        self.to_next_level_label = QtWidgets.QLabel(self.battlewidget)
        self.to_next_level_label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.to_next_level_movie = QtGui.QMovie("assets/ui/next_level.gif")
        self.to_next_level_label.setMovie(self.to_next_level_movie)
        self.to_next_level_label.hide()

        self.setCentralWidget(self.main_menu_widget)

    def sound_enabler(self):
        if self.sound_is_enabled:
            self.sound_is_enabled = False
            self.menu_sound_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/no_sound_button.png);}
                                                                                QPushButton:hover {border-image: url(assets/ui/no_sound_button_hover.png);}''')
        else:
            self.sound_is_enabled = True
            self.menu_sound_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/sound_button.png);}
                                                                                QPushButton:hover {border-image: url(assets/ui/sound_button_hover.png);}''')
            self.play_sound(self.button_sound)

    def play_sound(self, sound):
        if self.sound_is_enabled:
            sound.play()

    def tutorial_next(self):
        if not self.menu_label.isHidden():
            self.play_sound(self.button_sound)

            self.menu()
            self.tutorial_page_count = 0
            self.tutorial_label.show()

        self.tutorial_page_count += 1
        if self.tutorial_page_count == 4:
            self.tutorial_label.hide()
        else:
            self.tutorial_label.setPixmap(QtGui.QPixmap(f"assets/backgrounds/tutorial{self.tutorial_page_count}.png"))

    def reset_stats_n_enemies(self):

        hero.player.hp = hero.player.max_hp
        hero.player.def_points = 0
        hero.player.red_points = hero.player.max_red_points
        hero.player.green_points = hero.player.max_green_points
        hero.player.blue_points = hero.player.max_blue_points

        self.hero_hp.setText(str(hero.player.hp))
        self.hero_defence.setText(str(hero.player.def_points))

        self.stats_update_points()

        self.create_enemies()
        for i in range(5):
            self.set_card(i)

    def replay(self):
        self.rnd = 0
        if self.end_game_label.isHidden():
            self.menu()
        else:
            self.play_sound(self.button_sound)

            QtCore.QTimer.singleShot(1000, lambda: self.end_game_label.hide())
            QtCore.QTimer.singleShot(1000, lambda: self.end_game_exit_button.hide())
            QtCore.QTimer.singleShot(1000, lambda: self.end_game_replay_button.hide())

        self.to_next_level_label.show()
        self.to_next_level_movie.start()

        QtCore.QTimer.singleShot(1100, lambda: self.reset_stats_n_enemies())
        QtCore.QTimer.singleShot(1200, lambda: self.hero.setMovie(self.hero_idle))

        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_movie.stop())
        QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_label.hide())

    def menu(self):
        self.play_sound(self.button_sound)

        if self.menu_label.isHidden():
            self.menu_label.show()
            self.menu_continue_button.show()
            self.menu_replay_button.show()
            self.menu_exit_button.show()
            self.menu_tutorial_button.show()
            self.menu_sound_button.show()
        else:
            self.menu_label.hide()
            self.menu_continue_button.hide()
            self.menu_replay_button.hide()
            self.menu_exit_button.hide()
            self.menu_tutorial_button.hide()
            self.menu_sound_button.hide()

    def exit_confirm(self):
        self.play_sound(self.button_sound)

        if self.exit_confirm_label.isHidden():
            self.exit_confirm_label.show()
            self.exit_confirm_button.show()
            self.exit_cancel_button.show()
        else:
            self.exit_confirm_label.hide()
            self.exit_confirm_button.hide()
            self.exit_cancel_button.hide()

    def play_game(self):
        self.play_sound(self.button_sound)

        self.start_game_movie.start()
        self.start_game_label.raise_()

        self.to_next_level_label.show()
        self.to_next_level_movie.start()

        QtCore.QTimer.singleShot(2000, lambda: self.start_game_movie.stop())
        QtCore.QTimer.singleShot(1000, lambda: self.game_started())

    def game_started(self):
        hero.player = hero.ChosenHero('knight')
        for i in range(5):
            self.set_card(i)
        self.create_enemies()
        self.setCentralWidget(self.battlewidget)

        QtCore.QTimer.singleShot(1000, lambda: self.to_next_level_movie.stop())
        QtCore.QTimer.singleShot(1000, lambda: self.to_next_level_label.hide())

    def enemy_turn_delay(self, enemy_name):
        summ = 1000
        for i in range(enemy_name.enemy.number + 1):
            if self.enemy[i].enemy.is_alive:
                summ += 150 + (self.enemy[i].run_movie.frameCount()
                               + self.enemy[i].attack_movie.frameCount()
                               + self.enemy[i].run_back_movie.frameCount()) * 150
        return summ

    def end_turn(self):
        if sum(hero.player.chosen_cards) == 0:
            self.play_sound(self.button_sound)

            hero.player.chosen_cards[5] = True

            self.end_turn_button.setEnabled(False)
            self.end_turn_button.setStyleSheet(
                'QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn_pressed.png);}')
            self.menu_replay_button.setEnabled(False)
            self.menu_replay_button.setStyleSheet(
                '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_replay_button_pressed.png);}''')

            if self.enemy[0].enemy.hp > 0:
                self.enemy[0].enemy.def_points = 0
                self.enemy[0].defence.setText(str(self.enemy[0].enemy.def_points))
                QtCore.QTimer.singleShot(1000, lambda: self.enemy_turn(self.enemy[0]))
            if self.enemy[1].enemy.hp > 0:
                self.enemy[1].enemy.def_points = 0
                self.enemy[1].defence.setText(str(self.enemy[1].enemy.def_points))
                QtCore.QTimer.singleShot(self.enemy_turn_delay(self.enemy[0]), lambda: self.enemy_turn(self.enemy[1]))
            if self.enemy[2].enemy.hp > 0:
                self.enemy[2].enemy.def_points = 0
                self.enemy[2].defence.setText(str(self.enemy[2].enemy.def_points))
                QtCore.QTimer.singleShot(self.enemy_turn_delay(self.enemy[1]), lambda: self.enemy_turn(self.enemy[2]))

            QtCore.QTimer.singleShot(self.enemy_turn_delay(self.enemy[2]), lambda: self.new_turn())

    def new_turn(self):
        hero.player.def_points = 0
        self.hero_defence.setText(str(hero.player.def_points))

        if hero.player.hp > 0:
            for i in range(5):
                self.get_points()
                self.set_card(i)
            self.stats_update_points()
            hero.player.chosen_cards[5] = False

            self.end_turn_button.setEnabled(True)
            self.menu_replay_button.setEnabled(True)
            self.end_turn_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/ui/end_turn.png);}
                                                                                    QPushButton:pressed {border-image: url(assets/ui/end_turn_pressed.png);}''')
            self.menu_replay_button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/menu/menu_replay_button.png);}
                                                                        QPushButton:pressed {border-image: url(assets/menu/menu_replay_button_pressed.png);}''')
        else:
            self.to_next_level_label.show()
            self.to_next_level_movie.start()

            self.hero.setMovie(self.hero_is_dead_movie)
            self.hero_is_dead_movie.start()

            self.end_game_label.setPixmap(QtGui.QPixmap("assets/backgrounds/lose.png"))
            QtCore.QTimer.singleShot(1000, lambda: self.end_game_label.show())
            QtCore.QTimer.singleShot(1000, lambda: self.end_game_exit_button.show())
            QtCore.QTimer.singleShot(1000, lambda: self.end_game_replay_button.show())

            QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_movie.stop())
            QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_label.hide())

            QtCore.QTimer.singleShot(self.hero_is_dead_movie.frameCount() * 150, lambda: self.hero_is_dead_movie.stop())

    def get_points(self):
        arr = []
        if hero.player.red_points < 3:
            arr += 'r'
        if hero.player.green_points < 3:
            arr += 'g'
        if hero.player.blue_points < 3:
            arr += 'b'
        if arr == []:
            arr += 'n'
        f = random.choice(arr)
        if f == 'r':
            hero.player.red_points += 1
        elif f == 'g':
            hero.player.green_points += 1
        elif f == 'b':
            hero.player.blue_points += 1

    def set_card(self, card_is_chosen):
        r = random.randint(1, 3)
        # if card_name.disconnect():
        try:
            self.deck[card_is_chosen].card.clicked.disconnect()
        except:
            pass
        if r == 1:
            self.deck[card_is_chosen].card.clicked.connect(
                lambda: self.apply_attack_on_enemy_btn(card_is_chosen, self.hero_basic_attack_movie))
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
                    lambda: self.apply_attack_on_enemy_btn(card_is_chosen, self.hero_special3_movie))
                self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)

    def stats_update_points(self):
        self.red_points_label.setText(str(hero.player.red_points))
        self.green_points_label.setText(str(hero.player.green_points))
        self.blue_points_label.setText(str(hero.player.blue_points))

    def idle_hero(self):
        self.hero.setMovie(self.hero_idle)

    def create_enemies(self):
        self.rnd += 1
        self.level_label.setText(f"Уровень: {self.rnd}")
        if self.rnd == 5:
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
            self.to_next_level_movie.start()

            self.hero.setMovie(self.hero_run_movie)
            self.hero_run_movie.start()
            self.run_to_next_level_animation.start()

            QtCore.QTimer.singleShot(1000, lambda: self.idle_hero())
            QtCore.QTimer.singleShot(1100, lambda: self.hero.move(200, 320))

            if self.rnd == 5:
                self.end_game_label.setPixmap(QtGui.QPixmap("assets/backgrounds/win.png"))
                QtCore.QTimer.singleShot(1000, lambda: self.end_game_label.show())
                QtCore.QTimer.singleShot(1050, lambda: self.end_game_exit_button.show())
                QtCore.QTimer.singleShot(1100, lambda: self.end_game_replay_button.show())
            else:
                QtCore.QTimer.singleShot(1200, lambda: self.create_enemies())

            QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_movie.stop())
            QtCore.QTimer.singleShot(2000, lambda: self.to_next_level_label.hide())

            for i in range(5):
                self.set_card(i)
                self.get_points()
            self.stats_update_points()

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

    def run_n_play_animation(self, animation, enemy_name):
        self.running_hero(enemy_name.enemy.number)
        QtCore.QTimer.singleShot(500 + 150 * enemy_name.enemy.number,
                                 lambda: self.play_animation(animation))
        QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number + animation.frameCount()) * 150,
                                 lambda: self.running_back_hero(enemy_name.enemy.number))

    def enemy_animation(self, enemy_name, animation):
        enemy_name.label.setMovie(animation)
        animation.start()
        QtCore.QTimer.singleShot(animation.frameCount() * 150, lambda: animation.stop())

    def enemy_idle(self, enemy_name):
        enemy_name.label.setMovie(enemy_name.idle)

    def enemy_turn(self, enemy_name):
        r = random.randint(1, 2)
        if r == 1:
            random_attack_movie = QtGui.QMovie(random.choice(enemy_name.enemy.attack_gif_list))
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150 + random_attack_movie.frameCount() * 75,
                                     lambda: self.play_sound(self.hurt_sound))

            enemy_name.label.setMovie(enemy_name.run_movie)
            enemy_name.run_movie.start()
            enemy_name.run_animation.setDuration(500 + enemy_name.enemy.number * 150)
            enemy_name.run_back_animation.setDuration(500 + enemy_name.enemy.number * 150)
            enemy_name.run_animation.start()
            enemy_name.label.resize(enemy_name.enemy.y_size, enemy_name.enemy.y_size)
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150, lambda: enemy_name.run_movie.stop())
            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150,
                                     lambda: self.enemy_animation(enemy_name, random_attack_movie))
            QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number + random_attack_movie.frameCount()) * 150,
                                     lambda: enemy_name.label.setMovie(enemy_name.run_back_movie))
            QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number + random_attack_movie.frameCount()) * 150,
                                     lambda: enemy_name.run_back_movie.start())
            QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number + random_attack_movie.frameCount()) * 150,
                                     lambda: enemy_name.run_back_animation.start())

            QtCore.QTimer.singleShot(1000 + (enemy_name.enemy.number * 2 + random_attack_movie.frameCount()) * 150,
                                     lambda: enemy_name.run_back_movie.stop())
            QtCore.QTimer.singleShot(1000 + (enemy_name.enemy.number * 2 + random_attack_movie.frameCount()) * 150,
                                     lambda: enemy_name.label.resize(enemy_name.enemy.x_size,
                                                                     enemy_name.enemy.y_size))
            QtCore.QTimer.singleShot(1000 + (enemy_name.enemy.number * 2 + random_attack_movie.frameCount()) * 150,
                                     lambda: enemy_name.label.setMovie(enemy_name.idle))

            if hero.player.def_points >= enemy_name.enemy.attack:
                hero.player.def_points -= enemy_name.enemy.attack
            else:
                hero.player.hp = hero.player.hp + hero.player.def_points - enemy_name.enemy.attack
                hero.player.def_points = 0
                QtCore.QTimer.singleShot(800, lambda: self.hero_hp.setText(str(hero.player.hp)))
            QtCore.QTimer.singleShot(800, lambda: self.hero_defence.setText(str(hero.player.def_points)))

            QtCore.QTimer.singleShot(500 + enemy_name.enemy.number * 150 + random_attack_movie.frameCount() * 75,
                                     lambda: self.play_animation(self.hero_hurt_movie))
            QtCore.QTimer.singleShot(
                500 + enemy_name.enemy.number * 150 + random_attack_movie.frameCount() * 75 + self.hero_hurt_movie.frameCount() * 150,
                lambda: self.idle_hero())

        elif r == 2:
            self.play_sound(self.utility_sound)

            enemy_name.enemy.def_points += enemy_name.enemy.defence
            enemy_name.defence.setText(str(enemy_name.enemy.def_points))

            self.enemy_animation(enemy_name, enemy_name.defend_movie)
            QtCore.QTimer.singleShot(enemy_name.defend_movie.frameCount() * 150,
                                     lambda: enemy_name.label.setMovie(enemy_name.idle))

    def clear_enemies_btn(self):
        for i in range(3):
            self.enemy[i].clear_button()

    def enemy_is_attacked(self, enemy_name):
        if enemy_name.enemy.is_alive:
            self.enemy_animation(enemy_name, enemy_name.hurt_movie)
            self.play_sound(self.hurt_sound)

        if enemy_name.enemy.hp <= 0:
            if enemy_name.enemy.is_alive:
                enemy_name.enemy.is_alive = False

                QtCore.QTimer.singleShot(enemy_name.hurt_movie.frameCount() * 150,
                                         lambda: enemy_name.label.setMovie(enemy_name.dead_movie))
                QtCore.QTimer.singleShot(enemy_name.hurt_movie.frameCount() * 150,
                                         lambda: enemy_name.dead_movie.start())
                QtCore.QTimer.singleShot(
                    (enemy_name.hurt_movie.frameCount() + enemy_name.dead_movie.frameCount()) * 150 - 100,
                    lambda: enemy_name.dead_movie.stop())

                enemy_name.hp.hide()
                enemy_name.defence.hide()
        else:
            QtCore.QTimer.singleShot(enemy_name.hurt_movie.frameCount() * 75,
                                     lambda: enemy_name.hp.setText(str(enemy_name.enemy.hp)))
            QtCore.QTimer.singleShot(enemy_name.hurt_movie.frameCount() * 75,
                                     lambda: enemy_name.defence.setText(str(enemy_name.enemy.def_points)))
            QtCore.QTimer.singleShot(enemy_name.hurt_movie.frameCount() * 150,
                                     lambda: self.enemy_idle(enemy_name))

    def player_basic_defence(self, card_is_chosen):
        if hero.player.blue_points > 0 and sum(hero.player.chosen_cards) == 0:
            self.play_animation(self.hero_defend_movie)
            self.play_sound(self.utility_sound)

            QtCore.QTimer.singleShot(self.hero_defend_movie.frameCount() * 150, lambda: self.idle_hero())
            hero.player.blue_points -= 1
            hero.player.def_points += 3
            self.hero_defence.setText(str(hero.player.def_points))
            self.stats_update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def apply_attack_on_enemy_btn(self, card_is_chosen, animation):
        if ((animation == self.hero_basic_attack_movie) and (hero.player.red_points > 0) and (
                hero.player.green_points > 0)) or (
                (animation == self.hero_special3_movie) and (hero.player.red_points > 0) and (
                hero.player.blue_points > 0)):
            if sum(hero.player.chosen_cards) == 0:
                hero.player.chosen_cards[card_is_chosen] = True
                if animation == self.hero_basic_attack_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet_active)
                elif animation == self.hero_special3_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet_active)
                if self.enemy[0].enemy.hp > 0:
                    self.enemy[0].button.clicked.connect(
                        lambda: self.attack_enemy(self.enemy[0], card_is_chosen, animation))
                    self.enemy[0].button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
                if self.enemy[1].enemy.hp > 0:
                    self.enemy[1].button.clicked.connect(
                        lambda: self.attack_enemy(self.enemy[1], card_is_chosen, animation))
                    self.enemy[1].button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
                if self.enemy[2].enemy.hp > 0:
                    self.enemy[2].button.clicked.connect(
                        lambda: self.attack_enemy(self.enemy[2], card_is_chosen, animation))
                    self.enemy[2].button.setStyleSheet('''QPushButton {border: none;margin: 0px;padding: 0px;}
                                                                QPushButton:hover {border-image: url(assets/enemies/enemy_hover.png);}''')
            else:
                if hero.player.chosen_cards[card_is_chosen]:
                    self.clear_enemies_btn()
                    hero.player.chosen_cards[card_is_chosen] = False
                if animation == self.hero_basic_attack_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.basic_attack_sheet)
                elif animation == self.hero_special3_movie:
                    self.deck[card_is_chosen].card.setStyleSheet(hero.player.special3_sheet)

    def player_heal(self, card_is_chosen):
        if hero.player.green_points > 1 and sum(hero.player.chosen_cards) == 0:
            self.play_sound(self.utility_sound)

            hero.player.green_points -= 2
            hero.player.hp = min(hero.player.hp + 5, 15)
            self.hero_hp.setText(str(hero.player.hp))
            self.stats_update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)
            self.play_animation(self.hero_special1_movie)
            QtCore.QTimer.singleShot(self.hero_special1_movie.frameCount() * 150, lambda: self.idle_hero())

    def player_massive_attack(self, card_is_chosen):
        if hero.player.red_points == 3 and sum(hero.player.chosen_cards) == 0:
            self.run_n_play_animation(self.hero_special2_movie, self.enemy[1])
            hero.player.red_points -= 3
            for i in range(3):
                if self.enemy[i].enemy.def_points >= hero.player.attack - 1:
                    self.enemy[i].enemy.def_points -= hero.player.attack - 1
                else:
                    self.enemy[i].enemy.hp = self.enemy[i].enemy.hp - (
                            hero.player.attack - 1 - self.enemy[i].enemy.def_points)
                    self.enemy[i].enemy.def_points = 0

            QtCore.QTimer.singleShot(
                500 + (self.enemy[1].enemy.number * 2 + self.hero_special2_movie.frameCount()) * 75,
                lambda: self.enemy_is_attacked(self.enemy[0]))
            QtCore.QTimer.singleShot(
                500 + (self.enemy[1].enemy.number * 2 + self.hero_special2_movie.frameCount()) * 75,
                lambda: self.enemy_is_attacked(self.enemy[1]))
            QtCore.QTimer.singleShot(
                500 + (self.enemy[1].enemy.number * 2 + self.hero_special2_movie.frameCount()) * 75,
                lambda: self.enemy_is_attacked(self.enemy[2]))
            QtCore.QTimer.singleShot(1500 + (
                    self.enemy[1].enemy.number * 4 + self.hero_special2_movie.frameCount() + self.enemy[
                1].hurt_movie.frameCount() * 2) * 75,
                                     lambda: self.to_next_level())
            self.stats_update_points()
            self.deck[card_is_chosen].card.clicked.disconnect()
            self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)

    def card_is_active(self, card_is_chosen):
        hero.player.chosen_cards[card_is_chosen] = False

    def attack_enemy(self, enemy_name, card_is_chosen, animation):
        self.run_n_play_animation(animation, enemy_name)
        hero.player.red_points -= 1
        if animation == self.hero_basic_attack_movie:
            hero.player.green_points -= 1
            if enemy_name.enemy.def_points >= hero.player.attack:
                enemy_name.enemy.def_points -= hero.player.attack
            else:
                enemy_name.enemy.hp = enemy_name.enemy.hp - (hero.player.attack - enemy_name.enemy.def_points)
                enemy_name.enemy.def_points = 0
                QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number * 2 + animation.frameCount()) * 75,
                                         lambda: enemy_name.hp.setText(str(enemy_name.enemy.hp)))
            QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number * 2 + animation.frameCount()) * 75,
                                     lambda: enemy_name.defence.setText(str(enemy_name.enemy.def_points)))
        elif animation == self.hero_special3_movie:
            hero.player.blue_points -= 1
            enemy_name.enemy.hp = enemy_name.enemy.hp - (hero.player.attack - 1)
            QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number * 2 + animation.frameCount()) * 75,
                                     lambda: enemy_name.hp.setText(str(enemy_name.enemy.hp)))
        self.stats_update_points()
        self.clear_enemies_btn()
        QtCore.QTimer.singleShot(500 + (enemy_name.enemy.number * 2 + animation.frameCount()) * 75,
                                 lambda: self.enemy_is_attacked(enemy_name))
        QtCore.QTimer.singleShot(
            1000 + (enemy_name.enemy.number * 2 + animation.frameCount() + enemy_name.hurt_movie.frameCount()) * 150,
            lambda: self.card_is_active(card_is_chosen))
        QtCore.QTimer.singleShot(
            1500 + (enemy_name.enemy.number * 2 + animation.frameCount() + enemy_name.hurt_movie.frameCount()) * 150,
            lambda: self.to_next_level())
        self.deck[card_is_chosen].card.clicked.disconnect()
        self.deck[card_is_chosen].card.setStyleSheet(hero.player.blank_sheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMainWindow()
    window.show()

    QtGui.QFontDatabase.addApplicationFont("assets/monogram.ttf")

    sys.exit(app.exec())
