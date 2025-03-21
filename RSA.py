import random as rand

def computeGCD(x, y):
    while(y):
       x, y = y, x % y
    return abs(x)

def string_to_acsii(str):
    l = []
    for i in str:
        l.append(ord(i))
    return l

def encrypt(e, plain_text,n):
    m = string_to_acsii(plain_text)
    c = [pow(ch,e,n) for ch in m]
    return c
    
def decrypt(d,cipher,n):
    p = [pow(ch,d,n) for ch in cipher]
    ans = "".join(chr(ch) for ch in p)
    return ans



def Euclidian_algo(x , y ):
    r1 = x
    r2 = y
    s1 =1
    s2 =0
    t1 = 0
    t2 =1
    while r2 != 1:
        q = r1 // r2
        r = r1 % r2
        t = t1 - q * t2
        s = s1 - q*s2
        s1 = s2
        s2 =s
        t1 = t2
        t2 = t
        r1 = r2
        r2 = r
    if(t < 0):
        return (t+x) % x
    return t        
p = 61
q = 53
phi = (p-1) * (q-1)
n = p * q 
e = rand.randint(1,phi)
while(computeGCD(phi,e) != 1) and e != 1:
    e = rand.randint(1,phi)

m = "HELLO $ Fuckers"
print(e)
print(phi)
print(n)
d = Euclidian_algo(phi,e)
print(d)
cipher=encrypt(e,m,n)
print(cipher)
print(decrypt(d,cipher,n))



