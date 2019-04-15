
## CONDITION WAY ##
import threading
import time
import random
#condition = Condition()

'''
class Producer(Thread):
	global shelf 
	shelf = []
	def run(self):
		while True:
			condition.acquire()
			shelf.append(0)
			print("produced")
			condition.notify()
			condition.release()
			time.sleep(random.random())




class Consumer(Thread):
	def run(self):
		global shelf
		while True:
			condition.acquire()
			if not len(shelf):
				print("Nothing in queue")
				condition.wait()
				print("added")
			shelf.pop()
			print("consumed")
			condition.release()
			time.sleep(random.random())

'''









## SEMAPHORE


n = 10
buffer = [0] * n


filler = threading.Semaphore(0)
empty = threading.Semaphore(n)

def produce():
	print("produced")
	return 1


def consume(y):
	print("consumed")

def producer():
	front = 0
	while True:
		y = produce()
		empty.acquire()
		buffer[front] = y
		filler.release()
		front = (front + 1) % n
		print(buffer)
		



def consumer():
	rear = 0
	while True:
		filler.acquire()
		y = buffer[rear]
		buffer[rear] = 0
		empty.release()
		consume(y)
		rear = (rear + 1) % n
		print(buffer)



producerth = threading.Thread(target = producer)
consumerth = threading.Thread(target = consumer)


producerth.start()
consumerth.start()