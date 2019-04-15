import threading
import queue
import time

def facorial(listnum):
	h = listnum[0]
	for i in listnum[1:]:
		h *= i
	q.put(h)



def prepare_list(num):
	global nums
	nums = []
	for i in range(num + 1):
		nums.append(i)
	return nums


def prepare_indexes(numlst):
	x = len(numlst) // 2
	global step1, step2
	step1 = numlst[1: x]
	step2 = numlst[x : len(numlst)]


start = time.time()
prepare_list(5000)
prepare_indexes(nums)


q = queue.Queue()
first = threading.Thread(facorial(step1))
second = threading.Thread(facorial(step2))

first.start()
second.start()
a = q.get()
b = q.get()
print(a * b)
end = time.time()
print(end - start)






