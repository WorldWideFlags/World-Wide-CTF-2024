from pwn import remote, process

while True:

    r = process("../src/chall.py")
    r.recvuntil(b"my seed: ")
    mseed = bytes.fromhex(r.recvline().rstrip().decode())
    if mseed.startswith(b'\x01'):
        break
    r.close()
    # chall = bytes(get_random_array(42))
    # if chall.startswith(b'\x01'):
    #     break

user_input = b'\x00\x80\x01' + mseed[1:-1] + chr(mseed[-1] ^ 41 ^ 43).encode()
r.recvuntil(b"Enter your seed! > ")
r.sendline(user_input.hex().encode())

flag = r.recvline()
print(flag)
r.close()

# s = bytes.fromhex(user_input.hex())
# if s == chall:
#     print("Hey that's my seed! No copying >:(")
#     exit()
# random.seed(s)
# rrandom_val = random.getrandbits(9999)

# print(f'my new seed -> {str(random_val)[:100]}')
# print(f'    ur seed -> {str(rrandom_val)[:100]}')
# assert rrandom_val == random_val