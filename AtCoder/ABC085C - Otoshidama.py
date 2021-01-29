# N枚のお札の合計金額がY円になるかチェック

Input_Data = list(map(int, input().split()))
N = Input_Data[0]
Y = Input_Data[1]
flag = 0

for i in range(N + 1):
    for j in range(N + 1 - i):
        if (i * 10 + j * 5 + N - i - j) == Y / 1000:
            flag = 1
            a = i
            b = j
            c = N - i - j
            break

if flag == 1:
    print(a, b, c)
else:
    print(-1, -1, -1)
