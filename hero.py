class ChosenHero:
    def __init__(self, hp, atk, dfnc, points, cards):
        self.hp = hp
        self.attack = atk
        self.defence = dfnc
        self.cards = cards
        self.def_points = 0
        self.max_action_points = points
        self.active_cards = []*5
        self.played_cards = []*5
        self.attack_sheet = ''
        self.defence_sheet = ''


fighter = ChosenHero(15, 2, 3, 10, ['atk', 'atk', 'atk', 'atk', 'atk', 'dfnc', 'dfnc', 'dfnc', 'dfnc', 'dfnc'])
rogue = ChosenHero(12, 3, 2, 12, ['atk', 'atk', 'atk', 'atk', 'atk', 'dfnc', 'dfnc', 'dfnc', 'dfnc', 'dfnc'])
wizard = ChosenHero(9, 4, 3, 10, ['atk', 'atk', 'atk', 'atk', 'atk', 'dfnc', 'dfnc', 'dfnc', 'dfnc', 'dfnc'])
player = fighter
