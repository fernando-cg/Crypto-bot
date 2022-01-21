from ctypes import BigEndianStructure
from tabulate import tabulate
x=[1,2,3]
y=["Bitcoin","Ethereum","Doge coin"]
z =[2344.412,234.42,2334.422]

result = []

for i in range(len(x)):
    result.append([x[i],y[i],z[i]])

print(tabulate(result, headers=["index", "Crypto", "Precio"],tablefmt='plain', stralign='center'))