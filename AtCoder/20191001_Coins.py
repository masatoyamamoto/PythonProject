# count how many combinations of coins which satisfies sum = X
A = int(input())
B = int(input())
C = int(input())
X = int(input())

countResult = 0

for i in range(A + 1):
    for j in range(B + 1):
        for k in range(C + 1):
            tempResult = i * 500 + j * 100 + k * 50
            if tempResult == X:
                countResult += 1

print(countResult)
