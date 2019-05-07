import threading
from judger import judge

JUDGE_UNUSE = 0
JUDGE_USING = 1
MAX_JUDGE = 100

lock = threading.Lock()

class JudgeThread(threading.Thread):
	def __init__(self, **kwargs):
		threading.Thread.__init__(self, name='JudgeThread')
		self.attrib = kwargs
		self.judger = judge.Judger()

		print('Thread {} created'.format(threading.get_ident()))

	def run(self):
		att = self.attrib
		judger = self.judger
		# lock
		lock.acquire()
		
		print(judger.judge(att['prob_id'], att['lang'], att['code'], att['time_lim'], att['mem_lim'], att['test_case']))

		# release lock
		lock.release()

		print('Thread {} exit'.format(threading.get_ident()))

def add_judger(prob_id, lang, code, time_lim, mem_lim, test_case):
	th = JudgeThread(prob_id=prob_id, lang=lang, code=code, time_lim=time_lim, mem_lim=mem_lim, test_case=test_case)
	th.start()
