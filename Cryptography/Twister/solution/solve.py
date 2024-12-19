from sage.all import Zmod, matrix, vector
from dataclasses import dataclass
from cmath import exp
from pwn import *


#####
# Every bit is essentially just sum mod 2 aka XOR of the values of the chosen "waves".
# You know the values, now you need to know which ones are used.
# That's like solving a system of equations mod 2 (multiplication is like an AND gate).
# I could then talk about how it is done, but that's basic stuff you can google yourself.
#####

# --- code from chall
@dataclass
class Wave:
    a: int
    b: int

    def eval(self, x):
        theta = x / self.a + self.b
        return ((exp(1j * theta) - exp(-1j * theta)) / 2j).real


all_waves = [Wave(a, b) for a in range(2, 32) for b in range(7)]
# ---

# pwntools as in I/O
context.encoding = "UTF-8"
#pi = process(["python", "deploy.py"])  # for local
pi = remote("twister.chal.wwctf.com", 1337) # for remote

# recv data
data = []

for _ in range(8):  # make sure you use enough samples!
    pi.sendline("1")  # commits to leak random values
    result = int(
        pi.recvregex(
            r"You commited a fix deleting ([0-9]+) lines\.", capture=True
        ).group(1)
    )
    data += list(bin(result)[2:].zfill(32))

pi.sendline("2")  # call the senior!

# to use sagemath is to be a sage
F = Zmod(2)

mat = matrix(
    F,
    [
        [round(wave.eval(state)) % 2 for wave in all_waves]
        for state in range(1337, 1337 + len(data))
    ],
)

used = mat.solve_right(vector(F, data))

waves = [wave for i, wave in enumerate(all_waves) if used[i]]

# --- code from chall (modified)
state = 1337 + len(data)


def get_randbit():
    global state
    result = 0
    for wave in waves:
        result += round(wave.eval(state))
    result %= 2
    state += 1

    return result


def get_randbits(k):
    return int("".join(str(get_randbit()) for _ in range(k)), 2)


def get_token_bytes(k):
    return bytes([get_randbits(8) for _ in range(k)])


# ---

key = get_token_bytes(16)

pi.sendline(key.hex())

pi.interactive()