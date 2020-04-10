#Liangyu


import numpy as np
from numpy.polynomial import polynomial as p


q = 4095
n=128
xN_1 = [1] + [0] * (n-1) + [1]


def randomized_round(f, q): 
    round_f = []; 
    lenf = len(f)
    for i in range(lenf):
        coin = np.random.randint(0,2)
        if f[i] == 0:
            if coin == 0:
                round_f.append(0)
            else:
                round_f.append(q-1)   
        elif q%4 ==3 and f[i] == (3*q-1)/4:
            if coin == 0:
                round_f.append(f[i])
            else:
                round_f.append((3*q+3)/4)        
        elif f[i] == (q-1)/4:
            if coin == 0:
                round_f.append(f[i])
            else:
                round_f.append((q+3)/4)
        else:
            round_f.append(f[i])
    return round_f

def ModularRound(v, q):
    return np.round(p.polymul(2/q, v))%2

def CrossRound(v, q):
    return np.floor(p.polymul(4/q, v))%2


def rec(w,b):
    res = []
    index = min(len(w), len(b))
    for i in range(index):
        if b[i] == 1:
            if w[i] >= q/8 and w[i] < 5*q/8:
                res.append(1)
            else:
                res.append(0)
        elif b[i] == 0:
            if w[i] >= 3*q/8 and w[i] < 7*q/8:
                res.append(1)
            else:
                res.append(0)
    return res


print("\nQuantum-Resistant Lattice Cryptography\n")
print("Ring Learning with Error Diffie-Hellman Key Exchange\n")

print("Lattice Dimension: " + str(n))
print()
print("q: " +str(q))
print("q is of the form 2^k-1, q needs to be at least 1023")
print()
print()


a = np.random.randint(0, q, (n))
# a = [89, 13,  6, 73, 28, 30,  0,  1]

print("Public Key a:")
print(a.astype(int))
print()

#sample random errors from Gaussian distribution
s1 = np.floor(np.random.normal(0, size=(n)))
s0 = np.floor(np.random.normal(0, size=(n)))

b = p.polymul(a, s1)%q
b = p.polyadd(b, s0)%q
b = p.polydiv(b, xN_1)[1]%q
print("Public Key b:")
print(b.astype(int))
print()


#sample random errors from Gaussian distribution
e0 = np.floor(np.random.normal(0, size=(n)))
e1 = np.floor(np.random.normal(0, size=(n)))
e2 = np.floor(np.random.normal(0, size=(n)))

u = p.polymul(e0, a)%q
u = p.polyadd(u, e1)%q
u = p.polydiv(u, xN_1)[1]%q
# print("u")
# print(u.astype(int))
# print()

v = p.polymul(e0, b)%q
v = p.polyadd(v, e2)%q
v = p.polydiv(v, xN_1)[1]%q
# print("v")
# print(v.astype(int))
# print()

v_r = randomized_round(v, q)

keystream_a = ModularRound(v_r, q).astype(int)

mask = CrossRound(v_r, q)
print("mask: "+str(mask.astype(int)))
print()
print()

w = p.polymul(u, s1)%q
w = p.polydiv(w, xN_1)[1]%q

keystream_b = rec(w, mask)
keystream_b = np.array(keystream_b).astype(int)


print("Alice's shared secret: " + str(keystream_a))
digest_a = ''.join([str(elem) for elem in keystream_a]) 
print("{0:0>4X}".format(int(digest_a, 2)))
print()

print("Bobby's shared secret: " + str(keystream_b))
digest_b = ''.join([str(elem) for elem in keystream_b]) 
print("{0:0>4X}".format(int(digest_b, 2)))
print()

comparison = keystream_a == keystream_b
equal_arrays = comparison.all()
if equal_arrays == True:
    print("Alice and Bobby's Shared Secret is Equal.")
else:
    print("Error!")




