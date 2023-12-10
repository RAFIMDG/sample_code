str= {'a':3, "b":2, "c":1}
print(str["a"])
str2=sorted(str, key=str.get)
print(str2)
for k in str2: #['c', 'b', 'a']
    zip(k, str[k])