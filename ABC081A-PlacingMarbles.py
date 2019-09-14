# inputを変数に格納
data = input()
s = str(data)
array = list(map(int,s))
print(sum(array))