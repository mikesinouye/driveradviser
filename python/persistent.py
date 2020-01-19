import time
import requests

while True :
	time.sleep(1)
	try :
		r = requests.post(url="http://localhost:9190/data", data="hello")
		print(r.text)
		file = open("persistent.txt", "a")
		file.write(r.text + "\n")
		file.close()
	except: 
		file = open("persistent.txt", "a")
		file.write("failed" + "\n")
		file.close()