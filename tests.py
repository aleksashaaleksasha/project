import random
import hero
import enemies

while hero.player.hp > 0:
    i = 0
    played_cards_cnt = 0
    while '' in hero.player.active_cards:
        hero.player.active_cards[i] = random.choice(hero.player.cards)
        hero.player.cards[hero.player.cards.index(hero.player.active_cards[i])] = ''
        if not hero.player.active_cards[i] == '':
            i += 1
    print(hero.player.cards)
    print(hero.player.active_cards)
    while True:
        play_card_id = int(input())
        if play_card_id == 6:
            break
        hero.player.active_cards[play_card_id-1], hero.player.played_cards[play_card_id-1] = '', hero.player.active_cards[play_card_id-1]
        played_cards_cnt = max(played_cards_cnt, play_card_id)
        print(hero.player.played_cards)
    
    for i in range(10):
        if hero.player.cards[i] == '':
            hero.player.cards[i] = hero.player.played_cards[played_cards_cnt-1]
            hero.player.played_cards[played_cards_cnt-1] = ''
            played_cards_cnt -= 1
    #print(hero.player.cards)
    #print(hero.player.active_cards)
    #break
