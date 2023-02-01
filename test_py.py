import numpy as np
import s3spy

input_cards = np.asarray([0x12,0x23,0x33,0x44,0x35,0x25,0x28,0x29,0x39,0x3C,0x4C,0x2D,0x1C],dtype=np.uint8)

print(s3spy.getS3Sarr(input_cards,True).reshape(-1,13) % 16)
print(s3spy.getS3Sarr(input_cards,False).reshape(-1,13) // 16)
