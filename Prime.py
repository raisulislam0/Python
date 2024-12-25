import math

T = int(input())


def isPrime(n):
    if n==1:
        return False
    if n==2:
        return True
        
    else:
        for i in range(2, int(math.sqrt(n))+1):
            if n%i==0:
                return False
    return True


for j in range(T):
    n = int(input())

    if(isPrime(n)):
        print("Prime")
    else:
        print("Not prime")
        
