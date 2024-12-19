from notaes import notAES, xor_bytes, r_con, s_box, inv_mix_columns, inv_shift_rows, add_round_key, bytes2matrix, matrix2bytes
from os import urandom


key = urandom(16)
cipher = notAES(key)
flag = b"wwf{0n3_sm4l1_shiFt_In_sb0X_1_giAnt_l3aK_iN_expl0itk1nD}"
flag_enc = cipher.encrypt(flag)
print(f'{flag_enc = }')


# Recover the last round key set
last_rkeys = {i:list(range(256)) for i in range(16)}
cnt = 0
while not all(len(i) == 1 for i in last_rkeys.values()):

    # Query oracle here
    my_guess = cipher.encrypt(urandom(16))

    not_rkey = xor_bytes(my_guess, b"\xea"*16)
    for p,x in enumerate(not_rkey):
        if x not in last_rkeys[p]:
            continue
        last_rkeys[p].remove(x)
    cnt += 1

print(f"Recovered after {cnt} queries")


# Reverse to obtain all round keys
rkeys = [[last_rkeys[i][0] for i in range(16)]]

def get_prev_rkey(rkey, rcon_index):
    prev = []
    for i in range(15, 3, -1):
        prev = [rkey[i] ^ rkey[i-4]] + prev
    x = [s_box[i] for i in prev[-3:] + [prev[-4]]]
    x[0] ^= r_con[rcon_index]
    prev = list(xor_bytes(x, rkey[:4])) + prev
    return prev

for i in range(10, 0, -1):
    rkeys = [get_prev_rkey(rkeys[0], i)] + rkeys
key_matrices = [bytes2matrix(i) for i in rkeys]


# Decrypt encrypted flag
def inv_s_box(cipher_state):
    # wack inv_s_box that has a 1/2^k of working where k is the number of 0x93s that appear in cipher_state input
    cipher_state = matrix2bytes(cipher_state)
    cipher_state = [s_box.index(i) for i in cipher_state]
    cipher_state = bytes2matrix(cipher_state)
    return cipher_state


def decrypt_block(ciphertext):
    assert len(ciphertext) == 16
    cipher_state = bytes2matrix(ciphertext)

    add_round_key(cipher_state, key_matrices[-1])
    inv_shift_rows(cipher_state)

    cipher_state = inv_s_box(cipher_state)

    for i in range(9, 0, -1):
        add_round_key(cipher_state, key_matrices[i])
        inv_mix_columns(cipher_state)
        inv_shift_rows(cipher_state)

        cipher_state = inv_s_box(cipher_state)
    
    add_round_key(cipher_state, key_matrices[0])
    return matrix2bytes(cipher_state)


for i in range(0, len(flag_enc), 16):
    try:
        res = decrypt_block(flag_enc[i:i+16])
    except ValueError: # s_box.index(i) breaks due to wrong guess prior in inv_s_box
        res = b"ERR"
    print(res)

# Spam run this script until all flag blocks are recovered, 
# or hardcode choice making in inv_s_box from the same flag_enc and round key params
# or, get really lucky: (about 1 in 10 times i think)
"""
> python .\sol.py
flag_enc = b'\xe0\xec?hJ\x137\xb6~>1Sh+\xa4af\x93u\xbdD\xcdY\xd8a\xab\xd6/\x0b\x8e1\x17\xed\x1dV\xfa\xb8%\xd3zq\x00\x86(\xabx\x16\xe1\xe7\xc2\xa7Ob\xf8\x1c\x1b\xfe\xafq\xeaWp\x98a'
Recovered after 2090 queries
b'wwf{0n3_sm4l1_sh'
b'iFt_In_sb0X_1_gi'
b'Ant_l3aK_iN_expl'
b'0itk1nD}\x08\x08\x08\x08\x08\x08\x08\x08'
"""