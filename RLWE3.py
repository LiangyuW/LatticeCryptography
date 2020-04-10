
import numpy as np
from numpy.polynomial import polynomial as p
import json
import base64

q = 255
n=128
xN_1 = [1] + [0] * (n-1) + [1]

# character to send
c = "king"

print("\nQuantum-Resistant Lattice Cryptography\n")
print("Ring Learning with Error\n")

# convert polynomial to centered representation
def center(f):
    center_f = []
    for c in f:
        if c >= 0 and c <= (q-1)/2:
            center_f.append(c)
        elif c > q/2 and c <= q-1:
            center_f.append(c-q)
    return center_f

def str2bin(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bin2str(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def decapsulate(u, v, s):
    dm = p.polymul(u, s)%q
    dm = p.polydiv(dm, xN_1)[1]%q
    dm = center(p.polysub(v, dm)%q)
    dm = [int(np.round((t*2)/q+0.1)) for t in dm]
    dm = np.absolute(dm)
    return dm


a = np.random.randint(0, q, (128))
s = np.floor(np.random.normal(0, size=(128)))
e = [2,0,-1,0,1,0,-1]

b = p.polymul(a, s)%q
b = p.polyadd(b, e)%q
b = p.polydiv(b, xN_1)[1].astype(int)%q

print("Lattice Dimension: " + str(n))
print()
print("q: " +str(q))



c = input('Enter message to encrypt: ')


print()
print("public key (a, b)")
print("a")
print(a)
print("b")
print(b)


m = [int(bit) for bit in str2bin(c)]
print()
print("message to encrypt")
print(c)
print()
print("binary of message to send")
print(np.asarray(m))

r = [1,0,-1,0,1,0,1]
e1 = [1,0,1,0,-1,0,1]
e2 = [2,0,1,0,1,0,-1]


# r = np.floor(np.random.normal(0, size=(5)))
# e1 = np.floor(np.random.normal(0, size=(5)))
# e2 = np.floor(np.random.normal(0, size=(5)))



print()
u = p.polymul(a, r)%q
u = p.polyadd(u, e1)%q
u = p.polydiv(u, xN_1)[1]%q
u = u.astype(int)


print()
z = [int(np.round(q/2+0.1))*i for i in m]
v = p.polymul(b, r)%q
v = p.polyadd(v, e2)%q
v = p.polydiv(v, xN_1)[1]%q
v = p.polyadd(v, z)%q
v = p.polydiv(v, xN_1)[1]%q
v = v.astype(int)
print("ciphertext (u, v)")
print(u)
print(v)
print()

print("base64: ")

uv = u.tolist()+v.tolist()
uvstr = json.dumps(uv)
base64str = base64.b64encode(uvstr.encode('utf-8'))
print(base64str)
print()


dm = decapsulate(u, v, s)


print("Decryption ")
print(dm)

print(bin2str("".join(str(bit) for bit in dm)))

# print()
# print("test")
# k = p.polymul(r, e)
# w = p.polymul(s, e1)
# k = p.polysub(k, w)
# k = p.polyadd(k, e2)
# k = p.polydiv(k, xN_1)[1]
# print(k)

# k = p.polyadd(k, z)
# print(z)
# print(k)


# print()
# print(m)

# for t in dm:
#     if (t < q/4):
#         print(0, end = "")
#     else:
#         print(1, end = "")



