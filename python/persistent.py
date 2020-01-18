import time


count = 0
while True :
	time.sleep(5)
	file = open("persistent.txt", "a")
	file.write("executed persistent python at time " + str(count) + "\n")
	count = count + 1
	file.close()