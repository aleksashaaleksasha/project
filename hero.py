class ChosenHero:
    def __init__(self, hp, atk, dfnc, rpoints, gpoints, bpoints):
        self.hp = hp
        self.attack = atk
        self.defence = dfnc
        self.def_points = 0
        self.max_red_points = rpoints
        self.max_green_points = gpoints
        self.max_blue_points = bpoints
        self.idle_animation = "assets/heroes/knight/idle.gif"
        self.hurt_animation = "assets/heroes/knight/hurt.gif"
        self.basic_attack_animation = "assets/heroes/knight/basic_attack.gif"
        self.massive_attack_animation = "assets/heroes/knight/massive_attack.gif"
        self.pierce_attack_animation = "assets/heroes/knight/pierce_attack.gif"
        self.defence_animation = "assets/heroes/knight/def.gif"
        self.blank_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/blank_card.png);}
                                                                QPushButton:hover {border-image: url(assets/cards/blank_card_hover.png);}'''
        self.basic_attack_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/attack_card.png);}
                                                                QPushButton:hover {border-image: url(assets/cards/attack_card_hover.png);}
                                                                QPushButton:pressed {border-image: url(assets/cards/attack_card_pressed.png);}'''
        self.basic_attack_sheet_active = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/attack_card_hover.png);}
                                                                        QPushButton:hover {border-image: url(assets/cards/attack_card_hover.png);}
                                                                        QPushButton:pressed {border-image: url(assets/cards/attack_card_pressed.png);}'''
        self.defence_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/def_card.png);}
                                                                                    QPushButton:hover {border-image: url(assets/cards/def_card_hover.png);}
                                                                                    QPushButton:pressed {border-image: url(assets/cards/def_card_pressed.png);}'''
        self.special1_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/aspire_card.png);}
                                                                                            QPushButton:hover {border-image: url(assets/cards/aspire_card_hover.png);}
                                                                                            QPushButton:pressed {border-image: url(assets/cards/aspire_card_pressed.png);}'''
        self.special2_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/massive_card.png);}
                                                                                            QPushButton:hover {border-image: url(assets/cards/massive_card_hover.png);}
                                                                                            QPushButton:pressed {border-image: url(assets/cards/massive_card_pressed.png);}'''
        self.special3_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/pierce_card.png);}
                                                                                            QPushButton:hover {border-image: url(assets/cards/pierce_card_hover.png);}
                                                                                            QPushButton:pressed {border-image: url(assets/cards/pierce_card_pressed.png);}'''
        self.special3_sheet_active = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url(assets/cards/pierce_card_hover.png);}
                                                                                                    QPushButton:hover {border-image: url(assets/cards/pierce_card_hover.png);}
                                                                                                    QPushButton:pressed {border-image: url(assets/cards/pierce_card_pressed.png);}'''


fighter = ChosenHero(15, 3, 3, 3, 3, 3)
rogue = ChosenHero(12, 3, 2, 2, 5, 2)
wizard = ChosenHero(9, 4, 4, 3, 2, 4)
player = fighter
