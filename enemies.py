import json
import random

assets_path = 'assets/enemies/'

with open('assets/enemies/enemies.json') as json_file:
    enemies = json.load(json_file)

bosses_name_list = []
enemies_name_list = []
for en in enemies.keys():
    if enemies[en]["tags"].count('boss') == 1:
        bosses_name_list.append(en)
    else:
        enemies_name_list.append(en)


class Enemy:
    def __init__(self, enemy_name, cnt):
        self.number = cnt
        enemy = enemies[enemy_name]

        self.name = enemy['name']
        self.hp = random.randint(*enemy['hp'])
        self.attack = random.randint(*enemy['attack'])
        self.defence = random.randint(*enemy['defence'])
        self.def_points = 0
        self.is_alive = True

        self.x_size = 320
        self.y_size = 550

        self.idle_gif = f"{assets_path}{enemy_name}/idle.gif"
        self.hurt_gif = f"{assets_path}{enemy_name}/hurt.gif"
        self.dead_gif = f"{assets_path}{enemy_name}/dead.gif"
        self.defend_gif = f"{assets_path}{enemy_name}/protect.gif"
        self.run_gif = f"{assets_path}{enemy_name}/run.gif"
        self.run_back_gif = f"{assets_path}{enemy_name}/run_back.gif"
        self.attack_1_gif = f"{assets_path}{enemy_name}/attack_1.gif"
        self.attack_2_gif = f"{assets_path}{enemy_name}/attack_2.gif"
        self.attack_3_gif = f"{assets_path}{enemy_name}/attack_3.gif"

        self.attack_gif_list = [self.attack_1_gif, self.attack_2_gif, self.attack_3_gif]
