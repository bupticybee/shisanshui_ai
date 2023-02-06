import numpy as np
from scipy.stats import sem
import s3spy
from S3sHelper import S3sHelper
import random
import time
import tqdm

s3shelper = S3sHelper()

evs = []
for i in tqdm.tqdm(range(1000)):
    cards = s3shelper.cardstr[:]
    random.shuffle(cards)
    p1_cards = cards[:13]
    p2_cards = cards[13:26]

    strategy1, strategy2 = s3shelper.get_strategy(p1_cards,p2_cards)

    ind = np.argmax([x["cfr"]["strategy"] for x in strategy1])

    card1 = strategy1[ind]
    card2 = strategy2[-1]

    one_ev = s3shelper.get_result(card1,card2)
    evs.append(one_ev)

wins = [1 if i > 0 else 0 for i in evs]

print("average reward: ",np.mean(evs),"+-",1.96 * sem(evs))
print("average winrate: ",np.mean(wins),"+-",1.96 * sem(wins))