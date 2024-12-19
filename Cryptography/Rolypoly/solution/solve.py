from sage.all import GF, PolynomialRing, ZZ
from sage.all import load, vector, matrix, identity_matrix
from hashlib import sha256
from Crypto.Cipher import AES

n = 1201
q = 467424413

K = GF(q)
PR = PolynomialRing(K, names=('t',)); (t,) = PR._first_ngens(1)
R = PR.quotient(PR.ideal([t**n-1 ]))
PR2 = PolynomialRing(R,2 , names=('x', 'y',)); (x, y,) = PR2._first_ngens(2)

# Attack is built from https://archive.ymsc.tsinghua.edu.cn/pacm_download/672/12672-dingjt-j11.pdf
def EvalAt1(X):
    return X.lift().substitute({t:1})

def lift_1(Ctx):
    coefs = Ctx.coefficients()
    monoms= Ctx.monomials()
    eval = K.zero()
    for i in range(0,len(coefs)):
        eval += EvalAt1(coefs[i])*monoms[i]
    return eval

flag_enc, pubkey, Ctx = load('../dist/output.sobj')
# Use t=1 to convert to GF(q)
X00, X10, X01 = [EvalAt1(i) for i in pubkey]
f_ = lift_1(Ctx)
a20, a11, a02, a10, a01, a00 = [K(int(i)) - 6*n for i in f_.coefficients()] # 6n being average of err vector lifted to t=1
a00 -= 3*n//2 # 3n/2 is average of any SampleSmallPoly() i.e. m0

# Solve RLWE using CVP to recover  4*SampleSmallPoly()*x**i*y**j values
B = matrix(ZZ, [[a20, a11, a10, a02, a01, a00]])
# times [r10, r01, r00]
A_MAT = matrix(K, [ [X10, 0  , 0  ],  # x^2
                    [X01, X10, 0  ],  # xy
                    [X00, 0  , X10],  # x
                    [0  , X01, 0  ],  # y^2
                    [0  , X00, X01],  # y
                    [0  , 0  , X00]]) # 1
A = matrix(ZZ, A_MAT.T.rref())
O_MAT = (0*identity_matrix(3)).augment(q*identity_matrix(3))
A = A.stack(O_MAT).stack(B)
A = A.augment(vector(ZZ, [0]*(A.nrows()-1) + [1]))

C = A.LLL()
for e_vec in C:
    if e_vec[-1] == 1:
        break

# Recover r value
e_vec = [int(i) + 6*n for i in e_vec[:6]]
e_vec[-1] += 3*n//2
B = vector(K, [i + 6*n for i in [a20, a11, a10, a02, a01, a00]])
B[-1] += 3*n//2
B -= vector(K, e_vec)
r_vec = vector(ZZ, A_MAT.solve_right(B))

rk = sha256(str(int(r_vec[0]) * int(r_vec[1]) * int(r_vec[2])).encode()).digest()
flag_dec = AES.new(key=rk, mode=AES.MODE_ECB).decrypt(flag_enc)
print(flag_dec)