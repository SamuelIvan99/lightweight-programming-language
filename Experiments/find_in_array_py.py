import time
import random

start = time.time()

f = open("Texts/find_in_array_py.txt", "w")

max_size = 10000000
arrayS = [0] * max_size

min = 10001
max = 0

nums = [0,0]

for i in range(max_size):
    arrayS[i] = random.randint(0, max_size)

for i in range(max_size):
    if arrayS[i] < min:
        min = arrayS[i]
    if max < arrayS[i]:
        max = arrayS[i]

for i in range(max_size):
    if arrayS[i] == max:
        nums[1] += 1
    if arrayS[i] == min:
        nums[0] += 1

f.write("Min element is: " + str(min) + "\n")
f.write("Min element found: " + str(nums[0]) + " times\n")
f.write("Max element is: " + str(max) + "\n")
f.write("Max element found: " + str(nums[1]) + " times\n")

f.write("\n\n\nFull Array:\n ")

for i in range(max_size):
    f.write(str(arrayS[i]) + "\n")

f.close()

end = time.time()

print(end - start)