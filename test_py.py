import numpy as np
import s3spy
from S3sHelper import S3sHelper
import random
import time

input_cards = np.asarray([0x12,0x23,0x33,0x44,0x35,0x25,0x28,0x29,0x39,0x3C,0x4C,0x2D,0x1C],dtype=np.uint8)

s3spy.getS3Sarr(input_cards,True).reshape(-1,13)

s3shelper = S3sHelper()

input_cardstrs = [s3shelper.hackcode2cardstr[i] for i in input_cards]
print(input_cardstrs)
for one_candidate in s3shelper.get_candidate(input_cardstrs):
    print(one_candidate)

print("=" * 70)


cards = s3shelper.cardstr[:]
random.shuffle(cards)

p1_cards = cards[:13]
p2_cards = cards[13:26]

start = time.time()
strategy1, strategy2 = s3shelper.get_strategy(p1_cards,p2_cards)
end = time.time()
print("cfr used: ",end - start,"s")

print("=" * 20 + "STRATEGY 1" + "=" * 20)
for one_strategy in strategy1:
    print(one_strategy)

print("=" * 20 + "STRATEGY 2" + "=" * 20)
for one_strategy in strategy2:
    print(one_strategy)
