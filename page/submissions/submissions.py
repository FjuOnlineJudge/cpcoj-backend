from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
import os

# oj
import utils
from exts import db
from models import Submission, Account

submissions_page = Blueprint('submissions_page'
						, __name__
						, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

page_size = 10

# TODO(roy4801): check if methods are right
@submissions_page.route('/submissions', methods=['GET', 'POST'])
@submissions_page.route('/submissions/<int:page>', methods=['GET', 'POST'])
def submissions_handle(page=1):
	# TODO(roy4801): add page check
	total = Submission.query.count()
	pagin = {'cur_page': page
		, 'next_lim': 4
		, 'total_page': round(total/10)
		, 'gen_url': lambda p: url_for('.submissions_handle')+'/{}'.format(p)}

	page -= 1

	# Query for 10 subs for order in desc
	sub_list = Submission.query \
				.order_by(Submission.submit_id.desc()) \
				.offset(page*page_size) \
				.limit(page_size) \
				.all()

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

	return render_template('submissions.html', sub_list=sub_list, pagin=pagin)
