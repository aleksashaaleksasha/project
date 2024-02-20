import random


class Slime:
    def __init__(self):
        self.name = random.choice(['Огненный слизень', 'Ядовитый слизень', 'Водяной слизень'])
        self.hp = random.randint(3, 5)
        self.attack = random.randint(1, 2)
        self.defence = random.randint(2, 3)
        self.def_points = 0

class Spearman:
    def __init__(self):
        self.name = 'Скелет-копейщик'
        self.hp = random.randint(6, 8)
        self.attack = random.randint(2, 3)
        self.defence = random.randint(1, 2)
        self.def_points = 0

class Warrior:
    def __init__(self):
        self.name = 'Скелет-воин'
        self.hp = random.randint(8, 10)
        self.attack = random.randint(1, 2)
        self.defence = random.randint(2, 3)
        self.def_points = 0

class Boss:
    def __init__(self):
        self.name = 'тест'
        self.hp = random.randint(20, 40)
        self.attack = round(100/self.hp)
        self.defence = random.randint(3, 4)
        self.def_points = 0