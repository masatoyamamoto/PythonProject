# sums of each digits
inputList = list(map(int, input().split()))
tempResult = 0
N = inputList[0]
A = inputList[1]
B = inputList[2]


def sum_of_digits(num):
    array = sum(map(int, str(num)))
    return array


for i in range(N):
    temp = sum_of_digits(i + 1)
    if A <= temp <= B:
        tempResult += i + 1

print(tempResult)
