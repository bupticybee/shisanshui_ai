import numpy as np
import s3spy
from S3sHelper import S3sHelper

input_cards = np.asarray([0x12,0x23,0x33,0x44,0x35,0x25,0x28,0x29,0x39,0x3C,0x4C,0x2D,0x1C],dtype=np.uint8)

s3spy.getS3Sarr(input_cards,True).reshape(-1,13)

s3shelper = S3sHelper()

input_cardstrs = [s3shelper.hackcode2cardstr[i] for i in input_cards]
print(input_cardstrs)
for one_candidate in s3shelper.get_candidate(input_cardstrs):
    print(one_candidate)



