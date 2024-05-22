import time
import random

start = time.time()

f = open("Texts/bubble_sort_python.txt", "w")

max_size = 10000
arrayS = [0] * max_size

f.write("Unsorted\n")

for i in range(max_size):
    arrayS[i] = random.randint(0, 9147413941)
    f.write(str(arrayS[i]) + "\n")


for i in range(max_size - 1):
    flag = False
    for j in range(max_size - i - 1):
        if(arrayS[j + 1] < arrayS[j]):
            temp = arrayS[j]
            arrayS[j] = arrayS[j + 1]
            arrayS[j + 1] = temp
            flag = True
    
    if(flag == False):
        break

f.write("\n\n\n\nSorted\n")
for i in range(max_size):
    f.write(str(arrayS[i]) + "\n")     

f.close()

end = time.time()

print(end - start)