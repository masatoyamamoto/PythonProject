# Simulate a card game for two, Alice and bob
N = int(input())
a_i = list(map(int, input().split()))

a_i.sort(reverse=True)
alice = 0
bob = 0
for i in range(N):
    if i % 2 == 0:
        alice += a_i[i]
    else:
        bob += a_i[i]

result = abs(alice - bob)
print(result)
