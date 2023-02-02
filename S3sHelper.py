import numpy as np
import s3spy
import deuces
from deuces import Card, Evaluator, Deck

class S3sHelper():
    def __init__(self):
        hackcode = [
            0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D, # 方块 A - K
            0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D, # 梅花 A - K
            0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D, # 红心 A - K
            0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4A,0x4B,0x4C,0x4D, # 黑桃 A - K
        ]

        cardstr = []
        for color in "dchs":
            for rank in "A23456789TJQK":
                cardstr.append(rank + color)

        self.hackcode2cardstr = dict(zip(hackcode,cardstr))
        self.cardstr2hackcode = dict(zip(cardstr,hackcode))
        self.evaluator = Evaluator()

    def get_candidate(self,cards):
        card_hackarr = []
        for one_card in cards:
            assert(one_card in self.cardstr2hackcode)
            card_hackarr.append(self.cardstr2hackcode[one_card])

        input_cards = np.asarray(card_hackarr,dtype=np.uint8)

        ret_candidates = s3spy.getS3Sarr(input_cards,False).reshape(-1,13)

        ret_cards = []
        for one_candidate in ret_candidates:
            one_cards = []
            for one_cardhack in one_candidate:
                one_cards.append(self.hackcode2cardstr[one_cardhack])

            ranks = [
                self.evaluator.evaluate_three([
                    Card.new(i) for i in one_cards[:3]
                ],[]),
                self.evaluator.evaluate([
                    Card.new(i) for i in one_cards[3:8]
                ],[]),
                self.evaluator.evaluate([
                    Card.new(i) for i in one_cards[8:13]
                ],[])
            ]
            ret_cards.append({"cards":one_cards,"ranks":ranks})

        return ret_cards



