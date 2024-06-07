import json

assets_path = 'assets/heroes/'

with open(f'{assets_path}heroes.json') as json_file:
    heroes = json.load(json_file)


class ChosenHero:
    def __init__(self, name):
        hero = heroes[name]
        self.name = hero['name']
        self.max_hp = hero["hp"]
        self.hp = hero["hp"]
        self.attack = hero["atk"]
        self.defence = hero["dfnc"]
        self.def_points = 0

        self.max_red_points = hero["red_points"]
        self.max_green_points = hero["green_points"]
        self.max_blue_points = hero["blue_points"]

        self.idle_gif = f"{assets_path}{name}/idle.gif"
        self.hurt_gif = f"{assets_path}{name}/hurt.gif"
        self.basic_attack_gif = f"{assets_path}{name}/basic_attack.gif"
        self.defence_gif = f"{assets_path}{name}/def.gif"
        self.special1_gif = f"{assets_path}{name}/special1.gif"
        self.special2_gif = f"{assets_path}{name}/special2.gif"
        self.special3_gif = f"{assets_path}{name}/special3.gif"
        self.run_gif = f"{assets_path}{name}/run.gif"
        self.run_back_gif = f"{assets_path}{name}/run_back.gif"
        self.dead_gif = f"{assets_path}{name}/dead.gif"

        self.blank_sheet = str('QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards/blank_card.png);}
                                                                QPushButton:hover {border-image: url('''+assets_path+name+'''/cards/blank_card_hover.png);}''')
        self.basic_attack_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards/attack_card.png);}
                                                                QPushButton:hover {border-image: url('''+assets_path+name+'''/cards/attack_card_hover.png);}
                                                                QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards/attack_card_pressed.png);}'''
        self.basic_attack_sheet_active = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards/attack_card_hover.png);}
                                                                        QPushButton:hover {border-image: url('''+assets_path+name+'''/cards/attack_card_hover.png);}
                                                                        QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards/attack_card_pressed.png);}'''
        self.defence_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards/def_card.png);}
                                                                                    QPushButton:hover {border-image: url('''+assets_path+name+'''/cards/def_card_hover.png);}
                                                                                    QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards/def_card_pressed.png);}'''
        self.special1_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards/special1_card.png);}
                                                                                            QPushButton:hover {border-image: url('''+assets_path+name+'''/cards/special1_card_hover.png);}
                                                                                            QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards/special1_card_pressed.png);}'''
        self.special2_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards/special2_card.png);}
                                                                                            QPushButton:hover {border-image: url('''+assets_path+name+'''/cards//special2_card_hover.png);}
                                                                                            QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards//special2_card_pressed.png);}'''
        self.special3_sheet = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards//special3_card.png);}
                                                                                            QPushButton:hover {border-image: url('''+assets_path+name+'''/cards//special3_card_hover.png);}
                                                                                            QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards//special3_card_pressed.png);}'''
        self.special3_sheet_active = '''QPushButton {border: none;margin: 0px;padding: 0px;border-image: url('''+assets_path+name+'''/cards//special3_card_hover.png);}
                                                                                                    QPushButton:hover {border-image: url('''+assets_path+name+'''/cards//special3_card_hover.png);}
                                                                                                    QPushButton:pressed {border-image: url('''+assets_path+name+'''/cards//special3_card_pressed.png);}'''


fighter = ChosenHero('knight')

player = fighter
