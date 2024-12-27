# Enter your code here. Read input from STDIN. Print output to STDOUT

import statistics
a = []
dic = {}
n = int(input())
xx = input().split()
x = list(map(int, xx))



for element in x:
    if element in dic:
    
        dic[element] += 1
    else:
        dic[element] = 1

        
maximum = max(dic.values())

for element, freq in dic.items():
    if freq == maximum:
        a.append(element)

if (len(a) > 1):
    mode = min(a)
else:
    mode = statistics.mode(x)
        
            
    
print(statistics.mean(x))
print(statistics.median(x))    
print(mode)
