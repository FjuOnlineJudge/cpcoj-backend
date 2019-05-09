import threading

# oj
from judger import judge
from exts import db
from ext_app import app
from models import Submission

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
		with app.app_context():
			att = self.attrib
			judger = self.judger
			# lock
			lock.acquire()

			res, meta = judger.judge(att['prob_id'], att['lang'], att['code'], att['time_lim'], att['mem_lim'], att['test_case'])

			# print(res, meta) # debug

			sub = Submission.query.get(att['submit_id'])

			# SYSERR > Restricted > OTHER > CE > RE > OLE > TLE > MLE > PE > WA > AC
			final_res = 0
			cnt = 0
			for i in res:
				if i == judge.RES_SYS_ERR:
					final_res = judge.RES_SYS_ERR
				elif i == judge.RES_RF:
					final_res = judge.RES_RF
				elif i == judge.RES_OTHER:
					final_res = judge.RES_OTHER
				elif i == judge.RES_CE:
					final_res = judge.RES_CE
				elif i == judge.RES_RE:
					final_res = judge.RES_RE
				elif i == judge.RES_OLE:
					final_res = judge.RES_OLE
				elif i == judge.RES_TLE:
					final_res = judge.RES_TLE
				elif i == judge.RES_MLE:
					final_res = judge.RES_MLE
				elif i == judge.RES_PE:
					final_res = judge.RES_PE
				elif i == judge.RES_WA:
					final_res = judge.RES_WA
				elif i == judge.RES_AC:
					cnt += 1

			if final_res == 0 and cnt == att['test_case']:
				final_res = judge.RES_AC

			sub.result = judge.result_type[final_res]

			total_time = 0
			total_mem = 0
			time_wall_max = 0
			for i in range(att['test_case']):
				now = 'run_{}'.format(i)

				total_time += meta[now]['time'] * 1000.0 if 'time' in meta[now] else 0.0
				total_mem += meta[now]['max-rss'] if 'max-rss' in meta[now] else 0.0
				# Get the maximium of time_wall_max
				if 'time-wall' in meta[now] and meta[now]['time-wall'] > time_wall_max:
					time_wall_max = meta[now]['time-wall']
			# Edit the resTime
			if final_res == judge.RES_TLE:
				sub.resTime = time_wall_max * 1000.0
			else:
				sub.resTime = total_time / att['test_case']
			# Edit the resMem
			sub.resMem = total_mem / att['test_case']

			# db.session.add(sub)
			db.session.commit()

			# release lock
			lock.release()

			print('Thread {} exit'.format(threading.get_ident()))

def add_judger(submit_id, prob_id, lang, code, time_lim, mem_lim, test_case):
	th = JudgeThread(submit_id=submit_id, prob_id=prob_id, lang=lang, code=code, time_lim=time_lim, mem_lim=mem_lim, test_case=test_case)
	th.start()
