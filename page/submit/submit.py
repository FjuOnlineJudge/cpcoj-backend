from flask import Flask, Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import os, datetime

import utils
from models import Problem, Submission
from exts import db

from judger import judge
from judger import manage

submit_page = Blueprint('submit_page'
						, __name__
						, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@submit_page.route('/submit', methods=['GET','POST'])
@login_required
def submit_handle():
	if request.method == 'POST':
		pid = int(request.form['probID'])
		lang = request.form['lang']
		code = request.form['code']

		prob = Problem.query.get(pid)
		if prob:
			sub = Submission(result='Wait'
					, resTime=-1.0, resMem=-1.0
					, code=code, lang=lang, rank=-1, time=datetime.datetime.now()
					, account=current_user, problem=prob)
			db.session.add(sub)
			db.session.commit()
			print(sub)

		manage.add_judger(1, judge.JUDGE_CPP, code, 3.0, 65536, 4)

		# judger = judge.Judger()
		# res = judger.judge(1, judge.JUDGE_CPP, code, 3.0, 65536, 4)
		# res = [judge.result_type[i] for i in res]
		# print(res)
		# flash(' '.join(res))

	return render_template('submit.html')