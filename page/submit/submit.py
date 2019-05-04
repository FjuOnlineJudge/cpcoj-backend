from flask import Flask, Blueprint, render_template, request, flash
from flask_login import login_required
import os


cur_path = os.path.abspath(os.path.dirname(__file__))

import judge

submit_page = Blueprint('submit_page'
						, __name__
						, template_folder=os.path.join(cur_path, 'templates'))

@submit_page.route('/submit', methods=['GET','POST'])
@login_required
def submit_handle():
	if request.method == 'POST':
		pid = request.form['probID']
		lang = request.form['lang']
		code = request.form['code']

		judger = judge.Judger()
		res = judger.judge(1, judge.JUDGE_CPP, code, 3.0, 65536, 4)
		res = [judge.result_type[i] for i in res]
		print(res)
		flash(' '.join(res))

	return render_template('submit.html')