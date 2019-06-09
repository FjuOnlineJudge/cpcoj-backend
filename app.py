#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, LoginManager, logout_user
import datetime, json

from form import *
from exts import db
from models import Problem, Account, Submission, Tag
import config

# Dealing with the path problem
import sys
sys.path.append('page')
sys.path.append('judger')

LISTEN_ALL = True

from ext_app import app

# Register blueprints
from submit import submit
app.register_blueprint(submit.submit_page)

from oj_test import test
app.register_blueprint(test.test_page)

from submissions import submissions
app.register_blueprint(submissions.submissions_page)

from edit_problem import edit_problem
app.register_blueprint(edit_problem.edit_problem_page)

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
	return Account.query.get(int(user_id))

@app.route('/problem_list', methods=['GET', 'POST'])
def problem_list():
	tag = Tag.query.all()
	author = []
	problem = Problem.query.order_by().all()

	# Popular Question
	## Sort
	ranklist = []
	for pro in problem:
		data = Submission.query.filter_by(problem_id=pro.problem_id).group_by(Submission.account_id).count()
		ranklist.append((pro.problemName, pro.problem_id, data))
	ranklist.sort(key=lambda tup: tup[2], reverse=True)

	# Problem List
	## check state
	checked_tag = []
	if request.method == 'POST':
		for i in tag:
			if i.tag_name in request.form:
				checked_tag.append(i)

	## Gathering problems by tag
	picked_problem = []
	for i in checked_tag:
		picked_problem += i.problem.all()

	if picked_problem != []:
		problem = picked_problem

	## Author's name of the problems
	for prob_iter in problem:
		Account_search = Account.query.filter(Account.uid==prob_iter.uid).first()
		if Account_search:
			author.append(Account_search.username)

	## Submitmission INFO
	sub_info = []
	for pro in problem:
		# target = Account.query.filter_by(username=name).first()
		total_submit = Submission.query.filter_by(problem_id=pro.problem_id).count()
		total_ac = Submission.query.filter_by(problem_id=pro.problem_id).filter_by(result="AC").count()
		# real_ac = Submission.query.filter_by(problem_id=pro.problem_id).filter_by(result="AC").group_by(Submission.account_id).all()
		sub_info.append((total_ac, total_submit))

	return render_template('problem_list.html' , tag=tag
                        						, problem=problem
			                       				, name=author
												, sub_info=sub_info
												, ranklist=ranklist)

@app.route('/problem/<int:pid>', methods=['GET', 'POST'])
def problem(pid):
	problem = Problem.query.filter_by(problem_id=pid).first()
	author = Account.query.filter(Account.uid == problem.uid).first()

	total_submit = Submission.query.filter_by(problem_id=problem.problem_id).count()
	total_ac = Submission.query.filter_by(problem_id=problem.problem_id).filter_by(result="AC").count()
	subinfo = (total_ac, total_submit)
	tags = problem.problem_tag
	# TODO(roy4801): maybe there's json injection
	info = json.loads(problem.info)

	return render_template('problem.html', problem=problem
										 , author=author
										 , subinfo=subinfo
										 , tags=tags
										 , info=info)


@app.route('/sub_detail', methods=['GET', 'POST'])
def submission_detail():
	return render_template('sub_detail.html')

@app.route('/')
def index():
	# TODO: refactoring
	# 公告

	# 最新問題，目前列出前五個最新的問題
	author = []
	questions = Problem.query.order_by(Problem.uid.desc()).all()
	for prob_iter in questions:
		Account_search = Account.query.filter(Account.uid==prob_iter.uid).first()
		if Account_search:
			author.append(Account_search.username)

	# Ranklist
	all_user = Account.query.all()
	ranklist = []

	for idx in range(0,len(all_user)):
		total_submit = all_user[idx].submission.order_by(Submission.problem_id).count()
		total_ac = all_user[idx].submission.filter_by(result='AC').count()
		tried = all_user[idx].submission.order_by(Submission.problem_id).group_by(Submission.problem_id).count()
		real_ac = all_user[idx].submission.filter_by(result='AC').order_by(Submission.problem_id).group_by(Submission.account_id).count()
		ranklist.append((all_user[idx].username , total_submit, total_ac, tried, real_ac))

	# real_ac sort
	ranklist.sort(key=lambda tup: tup[4], reverse=True)

	return render_template('index.html', questions=questions,
										 name=author,
										 ranklist=ranklist)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form =FormRegister()

	print("{} | {}".format("email", form.email.data))
	if request.method == 'POST':
		if form.validate_on_submit():
			print("validate Success")
			# catch time
			date_time = datetime.datetime.now()

			# user & email collision
			username = Account.query.filter(Account.username == form.username.data).first()
			email = Account.query.filter(Account.email == form.email.data).first()


			if username or email:
				print("Username or Email collision")
				flash('Username or Email collision')
				# return 'Username or Email collision'
			elif form.password.data != form.confirm.data:
				########for test
				print(" two password is different")
				flash('two password is different')
				#######
				# return 'two password is different'
			else:
				account = Account(username=form.username.data
					, nickname=form.nickname.data
					, password=generate_password_hash(form.password.data)
					, email=form.email.data
					, permLevel=2
					, signUpTime=date_time
					, lastLoginTime=date_time
					, icon=False)
				db.session.add(account)
				db.session.commit()
				# flash('Success Thank You')
				return redirect(url_for('login'))
		else:
			flash('Email is worng')

	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = FormLogin()
	if form.validate_on_submit():
		#  當使用者按下login之後，先檢核帳號是否存在系統內。

		user = Account.query.filter_by(username=form.username.data).first()
		if user:
			#  當使用者存在資料庫內再核對密碼是否正確。
			if user.check_password(form.password.data):
				login_user(user, form.remember_me.data)
				date_time = datetime.datetime.now()
				user.lastLoginTime = date_time
				db.session.commit()
				return redirect(url_for('index'))

			else:
				#  如果密碼驗證錯誤，就顯示錯誤訊息。
				flash('Wrong Email/Username or Password')
		else:
			#  如果資料庫無此帳號，就顯示錯誤訊息。
			flash('Wrong Email/Username or Password')
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	# flash('Log Out See You.')
	return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
# @login_required
def edit():
	# current_user = Account.query.first()

	form = FormEdit()
	target = current_user
	if request.method == 'POST':
		if form.validate_on_submit():
			pass_flag = True
			check_coll = Account.query.filter_by(email=form.email.data).first()

			# 驗證現在密碼是否正確
			if not current_user.check_password(form.current_password.data):
				pass_flag = False
				flash('Wrong password', 'danger')

			if pass_flag:
				# print(request.form)
				if form.nickname.data != '':
					target.nickname = form.nickname.data
				if form.email.data != '':
					target.email = form.email.data
				if form.password.data != '':
					target.password = generate_password_hash(form.password.data)
				db.session.commit()
				flash('Succeed', 'success')

	return render_template('edit.html', form=form, target=target)

@app.route('/userinfo/<string:name>')
def userinfo(name):
	# TODO(roy4801): refactoring
	target = Account.query.filter_by(username=name).first()
	total_submit = target.submission.order_by(Submission.problem_id).all()
	total_ac = target.submission.filter_by(result = "AC").all()
	tried = target.submission.order_by(Submission.problem_id).group_by(Submission.problem_id).all()
	real_ac = target.submission.filter_by(result = "AC").order_by(Submission.problem_id).group_by(Submission.account_id).all()

	# print("AC:{}".format(len(real_ac)))
	# print("Try-and-no-AC:{}".format( len(tried)-len(real_ac) ))
	# print("AC-Rate:{}/{}".format(len(total_ac), len(total_submit)))
	wrong = []
	for tri in tried:
		for real in real_ac:
			if real.problem_id != tri.problem_id:
				wrong.append(tri)

	if target:
		return render_template('userinfo.html', info=target
											  , total_submit=total_submit
											  , total_ac=total_ac
											  , tried=tried
											  , real_ac=real_ac
											  , wrong=wrong)
	else:
		#TODO (halloworld) response 404
		return redirect(url_for('index'))

if __name__ == '__main__':
	if LISTEN_ALL:
		app.run(host='0.0.0.0')
	else:
		app.run()
