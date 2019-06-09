from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
import os, random, string

# oj
import utils
from exts import db
from models import Submission, Account, Problem

submissions_page = Blueprint('submissions_page'
						, __name__
						, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

def gen_random_str(size=4):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

page_size = 10

@submissions_page.route('/submissions', methods=['GET', 'POST'])
@submissions_page.route('/submissions/<int:page>', methods=['GET', 'POST'])
def submissions_handle(page=1):
	if page <= 0:
		return redirect(url_for('.submissions_handle'))
	uid = None
	pid = None
	# Get submission filter
	if request.method == 'POST':
		if 'username' in request.form and request.form['username'] != '' :
			acc = Account.query.filter_by(username=request.form['username']).first()
			print(acc)
			if acc:
				uid = acc.uid
			else:
				flash('User not found')
		if 'pid' in request.form:
			pid = request.form['pid']

	# print(uid, pid)

	total = 0
	if uid:
		total = Submission.query.filter_by(account_id=uid).count()
	else:
		total = Submission.query.count()

	pagin = {'cur_page': page
		, 'next_lim': 4
		, 'total_page': total//10 +1
		, 'gen_url': lambda p: url_for('.submissions_handle')+'/{}'.format(p)}

	page -= 1

	sub_list = Submission.query
	if uid:
		sub_list = sub_list.filter_by(account_id=uid)
	if pid:
		sub_list = sub_list.filter_by(problem_id=pid)
	# Query for 10 subs for order in desc
	sub_list = sub_list \
				.order_by(Submission.submit_id.desc()) \
				.offset(page*page_size) \
				.limit(page_size) \
				.all()
	# Prepare for the submissions table
	for i in sub_list:
		# Set `submitter`
		u = Account.query.get(i.account_id)
		if u:
			u = u.nickname
		else:
			u = 'Unknown'
		setattr(i, 'submitter', u)

		# Set `codeLen`
		codeLength = '{:.2f} KiB'.format(len(i.code)/1000)
		setattr(i, 'codeLen', codeLength)

		# Set `score`
		# TODO(roy4801): implement score
		setattr(i, 'score', 'NaN')

		# CE modal
		if i.result == 'CE':
			setattr(i, 'ce_id_str', gen_random_str(8))

	return render_template('submissions.html', sub_list=sub_list, pagin=pagin)
