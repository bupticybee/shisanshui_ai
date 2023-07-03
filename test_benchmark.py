import numpy as np
from scipy.stats import sem
import s3spy
from S3sHelper import S3sHelper
import random
import time
import tqdm

s3shelper = S3sHelper()

evs = []
for i in tqdm.tqdm(range(100)):
    cards = s3shelper.cardstr[:]
    random.shuffle(cards)

    # 随机给p1 和 p2 发牌
    p1_cards = cards[:13]
    p2_cards = cards[13:26]

    fake_cards = cards[13:]
    random.shuffle(fake_cards)

    # P1的策略使用类似 Deterministic MCTS的思路来解决 十三水中的不完全信息问题。会和那是均衡有偏离，
    # 但是于完全的CFR相比，节省了大量的算力

    fake_cards = fake_cards[:13]
    strategy1, _ = s3shelper.get_strategy(p1_cards,fake_cards)

    # 使用n = 10 的 Deterministic MCTS ， 理论上越大越好。 但是越大计算时间越久
    for i in range(10):
        fake_cards = cards[13:]
        random.shuffle(fake_cards)
        fake_cards = fake_cards[:13]
        s_strategy1, _ = s3shelper.get_strategy(p1_cards,fake_cards)
        assert(len(s_strategy1) == len(strategy1))
        for x in range(len(s_strategy1)):
            strategy1[x]["cfr"]["strategy"] += s_strategy1[x]["cfr"]["strategy"]

    # P2 则使用n=1的MCTS， 以证明Deterministic的n增大可以提高胜率
    fake_cards = cards[13:]
    random.shuffle(fake_cards)
    _, strategy2 = s3shelper.get_strategy(fake_cards[:13],p2_cards)

    ind_p1 = np.argmax([x["cfr"]["strategy"] for x in strategy1])
    ind_p2 = np.argmax([x["cfr"]["strategy"] for x in strategy2])

    card1 = strategy1[ind_p1]
    card2 = strategy2[ind_p2]

    one_ev = s3shelper.get_result(card1,card2)
    evs.append(one_ev)

wins = [1 if i > 0 else 0 for i in evs]

print("average reward: ",np.mean(evs),"+-",1.96 * sem(evs))
print("average winrate: ",np.mean(wins),"+-",1.96 * sem(wins))