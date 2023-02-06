import numpy as np
from scipy.stats import sem
import s3spy
from S3sHelper import S3sHelper
import random
import time
import tqdm
from simple_term_menu import TerminalMenu

s3shelper = S3sHelper()


def pretty_str(cards):
    retstr = ""
    retstr += "["
    for one_card in cards[:3]:
        one_card = one_card.replace("d","♦").replace("c","♣").replace("h","♥").replace("s","♠")
        retstr += one_card + " "
    retstr += "] "

    retstr += "{"
    for one_card in cards[3:8]:
        one_card = one_card.replace("d","♦").replace("c","♣").replace("h","♥").replace("s","♠")
        retstr += one_card + " "
    retstr += "} "

    retstr += "["
    for one_card in cards[8:]:
        one_card = one_card.replace("d","♦").replace("c","♣").replace("h","♥").replace("s","♠")
        retstr += one_card + " "
    retstr += "] "

    return retstr

evs = []
for i in tqdm.tqdm(range(100)):
    cards = s3shelper.cardstr[:]
    random.shuffle(cards)
    p1_cards = cards[:13]
    p2_cards = cards[13:26]

    strategy1, strategy2 = s3shelper.get_strategy(p1_cards,p2_cards)
    ind2 = np.argmax([x["cfr"]["strategy"] for x in strategy2])


    random.shuffle(strategy1)
    options = [pretty_str(x["cards"]) for x in strategy1]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    card1 = strategy1[menu_entry_index]
    card2 = strategy2[ind2]
    card2_cards = card2["cards"]

    one_ev = s3shelper.get_result(card1,card2)

    print(f"You have selected {options[menu_entry_index]}!")
    print(f"Opponent have selected {pretty_str(card2_cards)}, your ev = {one_ev}")

    evs.append(one_ev)

wins = [1 if i > 0 else 0 for i in evs]

print("average reward: ",np.mean(evs),"+-",1.96 * sem(evs))
print("average winrate: ",np.mean(wins),"+-",1.96 * sem(wins))
