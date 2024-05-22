import time

start = time.time()

f = open("matrix_python.txt", "w")

max_size = 1000

for i in range(max_size):
    for j in range(max_size):
        f.write(str((i*max_size)+j) + " ")
    f.write("\n")

f.close()

end = time.time()

print(end - start)