# LCG.py

# inputs: m is the modelus, a is the multiplier, c is the increment, X_0
# is the initial seed

# outputs: P - period of the sequence,
# mean - average of one period of the real random numbers,
# var - variance of the sequence of one period of the random numbers,
# one period and three P + 3 integer numbers.

import numpy as np


def generator(m, a, c, seed):
    seed = ((a * seed + c) % m)
    return seed


def lcg(m, a, c, seed):
    rand = [seed]
    count = 1
    for i in range(m):
        seed = int(generator(m, a, c, seed))
        if seed != rand[0]:
            count += 1
            rand.append(seed)
        else:
            break
    rand = np.array(rand) / m

    return count, np.mean(rand), np.std(rand), rand

lcg_rand = lcg(64, 17, 43, 27)
print(lcg_rand)
