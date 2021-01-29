# N個の要素の重複しない要素の個数をカウント
N = int(input())
a = []

for i in range(N):
    a.append(input())

original_items = list(set(a))
print(len(original_items))