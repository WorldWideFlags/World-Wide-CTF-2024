from pwn import remote, process
from string import printable

G0 = [0, 225927228766784218634420243069685647443]
G1 = [33227089305676028431404869009266235308, 0]

f1 = b"\x01"
f0 = b"\x01"
#io = process(["python", "chall.py"])
io = remote('amineo.chal.wwctf.com', 1337)

def renew_conn():
    global io
    io.close()
    #io = process(["python", "chall.py"])
    io = remote('amineo.chal.wwctf.com', 1337)

def enc(a):
    return "".join(hex(k)[2:].zfill(32) for k in a).encode()

def prntble(a):
    try:
        a = a.decode()
    except:
        return False
    return all(k in printable for k in a)

while not prntble(f0):    
    io.recvuntil(b">")
    io.sendline(enc(G0))
    io.recvuntil(b"... :")

    f0 = bytes.fromhex(io.recvline().decode().strip())[:16]
    renew_conn()

while not prntble(f1):    
    io.recvuntil(b">")
    io.sendline(enc(G1))
    io.recvuntil(b"... :")

    f1 = bytes.fromhex(io.recvline().decode().strip())[16:]
    renew_conn()

print("flag :", (f0 + f1).decode())