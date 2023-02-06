import numpy as np
import s3spy
import deuces
from deuces import Card, Evaluator, Deck
from deuces.lookup import LookupTable
import itertools

class S3sHelper():
    def __init__(self):
        hackcode = [
            0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D, # 方块 A - K
            0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D, # 梅花 A - K
            0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D, # 红心 A - K
            0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4A,0x4B,0x4C,0x4D, # 黑桃 A - K
        ]

        self.cardstr = []
        for color in "dchs":
            for rank in "A23456789TJQK":
                self.cardstr.append(rank + color)

        self.hackcode2cardstr = dict(zip(hackcode,self.cardstr))
        self.cardstr2hackcode = dict(zip(self.cardstr,hackcode))
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
            # check 前墩中墩后墩是否符合大小关系
            if ranks[1] < ranks[2]:
                continue

            if ranks[1] > LookupTable.MAX_STRAIGHT:
                # rank 比三个少
                if ranks[1] <= LookupTable.MAX_TWO_PAIR and ranks[1] > LookupTable.MAX_THREE_OF_A_KIND:
                    if ranks[0] < 13:
                        continue
                else:
                    rank_second_dun_as_first = min([
                                                   self.evaluator.evaluate_three([
                                                       Card.new(j) for j in i
                                                   ],[])
                                                   for i in
                        itertools.combinations(one_cards[3:8],3)]
                    )
                    if ranks[0] <= rank_second_dun_as_first:
                        continue

            flag = False
            for each in ret_cards:
                each_ranks = each["ranks"]
                if ranks[0] >= each_ranks[0] and ranks[1] >= each_ranks[1] and ranks[2] >= each_ranks[2]:
                    flag = True
                elif ranks[0] < each_ranks[0] and ranks[1] < each_ranks[1] and ranks[2] < each_ranks[2]:
                    each["del"] = True
            if not flag:
                ret_cards.append({"cards":one_cards,"ranks":ranks,"duns":[1,1,1]})
            ret_cards = [x for x in ret_cards if "del" not in x]

        return ret_cards

    def get_result(self,one_cand1,one_cand2):
        cand1_strategy = one_cand1["cfr"]["strategy"]
        cand1_ranks = one_cand1["ranks"]
        cand1_duns = one_cand1["duns"]

        cand2_strategy = one_cand2["cfr"]["strategy"]
        cand2_ranks = one_cand2["ranks"]
        cand2_duns = one_cand2["duns"]
        one_ev = 0
        for rk1,rk2,dk1,dk2 in zip(cand1_ranks,cand2_ranks,cand1_duns,cand2_duns):
            if rk1 < rk2:
                one_ev += dk1
            elif rk1 > rk2:
                one_ev -= dk2
        return one_ev


    def _cfr_iter(self,cand1,cand2,iter_num):
        ev = 0

        for one_cand1 in cand1:
            cand1_strategy = one_cand1["cfr"]["strategy"]
            cand1_ranks = one_cand1["ranks"]
            cand1_duns = one_cand1["duns"]

            cand1_ev = 0
            total_prob = 0
            for one_cand2 in cand2:
                cand2_strategy = one_cand2["cfr"]["strategy"]
                cand2_ranks = one_cand2["ranks"]
                cand2_duns = one_cand2["duns"]
                one_ev = 0
                for rk1,rk2,dk1,dk2 in zip(cand1_ranks,cand2_ranks,cand1_duns,cand2_duns):
                    if rk1 < rk2:
                        one_ev += dk1
                    elif rk1 > rk2:
                        one_ev -= dk2

                cand1_ev += one_ev * cand2_strategy
                total_prob += cand2_strategy
            assert(np.isclose(total_prob,1))
            one_cand1["cfr"]["ev"] = cand1_ev
            ev += cand1_ev * cand1_strategy


        total_cum_regretp = 0
        for one_cand1 in cand1:
            cfr_cand1 = one_cand1["cfr"]
            regret = cfr_cand1["ev"] - ev
            cfr_cand1["cum_regret+"] = max(cfr_cand1["cum_regret+"] + regret,0)
            total_cum_regretp += cfr_cand1["cum_regret+"]

        for one_cand1 in cand1:
            cfr_cand1 = one_cand1["cfr"]
            if total_cum_regretp == 0:
                cfr_cand1["strategy"] = 1.0 / float(len(cand1))
            else:
                cfr_cand1["strategy"] = cfr_cand1["cum_regret+"] / total_cum_regretp



    def get_strategy(self,p1_cards,p2_cards):
        cand1 = self.get_candidate(p1_cards)
        cand2 = self.get_candidate(p2_cards)
        for each in cand1:
            each["cfr"] = {
                "cum_regret+" : 0,
                "strategy": 1.0 / float(len(cand1)),
            }
        for each in cand2:
            each["cfr"] = {
                "cum_regret+" : 0,
                "strategy": 1.0 / float(len(cand2)),
            }


        for i in range(100):
            self._cfr_iter(cand1,cand2,i+1)
            self._cfr_iter(cand2,cand1,i+1)

        return cand1,cand2



