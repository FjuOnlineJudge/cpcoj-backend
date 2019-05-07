from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
import os

# oj
import utils
from exts import db
from models import Submission, Account

submissions_page = Blueprint('submissions_page'
						, __name__
						, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@submissions_page.route('/submissions', methods=['GET', 'POST'])
def submissions_handle():
	# Query for 10 subs for order in desc
	sub_list = Submission.query \
				.order_by(Submission.submit_id.desc()) \
				.limit(10) \
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

	return render_template('submissions.html', sub_list=sub_list)
