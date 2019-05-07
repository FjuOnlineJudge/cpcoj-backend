from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
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
			date_time = datetime.datetime.now()
			sub = Submission(result='Wait'
					, resTime=-1.0, resMem=-1.0
					, code=code, lang=lang, rank=-1, time=date_time
					, account=current_user, problem=prob)
			db.session.add(sub)
			db.session.commit()
			# print(sub)

			manage.add_judger(sub.submit_id, prob.problem_id, judge.JUDGE_CPP, code, 3.0, 65536, 4)

		return redirect(url_for('submissions_page.submissions_handle'))
	# not if
	return render_template('submit.html')