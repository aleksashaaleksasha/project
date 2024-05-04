import random

assets_path = 'assets/enemies/'
dict_enemy = {'red_slime': {'name': 'Огненный слизень',
                            'hp': (3, 5),
                            'attack': (1, 2),
                            'defence': (2, 3)},
              'green_slime': {'name': 'Ядовитый слизень',
                              'hp': (3, 5),
                              'attack': (1, 2),
                              'defence': (2, 3)},
              'blue_slime': {'name': 'Водяной слизень',
                             'hp': (3, 5),
                             'attack': (1, 2),
                             'defence': (2, 3)},
              'spearman': {'name': 'Скелет-копейщик',
                           'hp': (6, 8),
                           'attack': (2, 3),
                           'defence': (1, 2)},
              'warrior': {'name': 'Скелет-воин',
                          'hp': (8, 10),
                          'attack': (1, 2),
                          'defence': (3, 4)},
              'boss': {'name': 'Босс',
                       'hp': (20, 40),
                       'attack': (3, 5),
                       'defence': (3, 4)}
              }


class Enemy:
    def __init__(self, enemy_name, cnt):
        self.number = cnt
        enemy = dict_enemy[enemy_name]
        self.name = enemy['name']
        self.hp = random.randint(*enemy['hp'])
        self.attack = random.randint(*enemy['attack'])
        self.defence = random.randint(*enemy['defence'])
        self.def_points = 0
        self.x_size = 320
        self.y_size = 550
        self.idle_gif = f"{assets_path}{enemy_name}/idle.gif"
        self.hurt_gif = f"{assets_path}{enemy_name}/hurt.gif"
        self.dead_gif = f"{assets_path}{enemy_name}/dead.gif"
        self.defend_gif = f"{assets_path}{enemy_name}/protect.gif"
        self.run_gif = f"{assets_path}{enemy_name}/run.gif"
        self.run_back_gif = f"{assets_path}{enemy_name}/run_back.gif"
        self.attack_ms = 600
        self.attack_gif = f"{assets_path}{enemy_name}/basic_attack.gif"
