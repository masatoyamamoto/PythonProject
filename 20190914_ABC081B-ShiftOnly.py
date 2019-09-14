# inputを受け取る
numberOfNumbers = input()
numbers = list(map(int, input().split()))
# 回数のカウント
a = 0

while sum(list(map(lambda x: x % 2, numbers))) == 0:
    numbers = list(map(lambda y: y / 2, numbers))
    a += 1

print(a)
