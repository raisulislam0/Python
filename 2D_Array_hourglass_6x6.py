#!/bin/python3

import math
import os
import random
import re
import sys

def hourglass(arr):
    total = 0
    totalArr = []
    
    for i in range(4):
        for j in range(4):
            minus = arr[i+1][j] + arr[i+1][j+2]
            for k in range(i, 3 + i):
                for l in range(j, 3 + j):
                    total +=arr[k][l]
            totalArr.append(total - minus)
            total = 0
            minus = 0
    return max(totalArr)
                    

if __name__ == '__main__':

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))
    
    print(hourglass(arr))
