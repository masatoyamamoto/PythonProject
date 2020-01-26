# T_candidatesからSという文字列を作り出すことができるか試行
S = input()
T_candidates = ['dream', 'dreamer', 'erase', 'eraser']

s = S.replace(T_candidates[3],"").replace(T_candidates[2],"").replace(T_candidates[1],"").replace(T_candidates[0],"")

if s:
    print("NO")
else:
    print("YES")

