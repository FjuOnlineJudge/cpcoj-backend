from manage import JudgeThread
import time

th_list = []

i = 100000
for j in range(10):
	th_list.append(JudgeThread(work=i*j))
	th_list[j].start()

while True:
	time.sleep(1)