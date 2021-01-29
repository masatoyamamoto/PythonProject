# 20190907
# 出力読み込み
a, b = map(int, input().split())
# 偶奇判定
oddFlag = abs((a * b) % 2)
# 表示
if oddFlag :
    print("Odd")
else :
    print("Even")

