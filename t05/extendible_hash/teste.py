
#Tentando entender os ponteiros em Python
a = [1]
b = a
a[0] = 2
print(b[0])
print(id(b[0]),id(a[0]))
b = [4]
print(id(b[0]),id(a[0]))