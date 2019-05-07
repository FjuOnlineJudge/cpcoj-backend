#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from form import FormRegister
from models import Problem, Account, Submission
import datetime
from exts import db
from form import *
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import config
from flask_login import login_user, current_user, login_required, LoginManager, logout_user

# Dealing with the path problem
import sys
sys.path.append('page')
sys.path.append('judger')

LISTEN_ALL = True

# Init flask app
app = Flask(__name__)
app.config.from_object(config)

# Register blueprints
from submit import submit
app.register_blueprint(submit.submit_page)

from oj_test import test
app.register_blueprint(test.test_page)

db.init_app(app)

bootstrap=Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
	return Account.query.get(int(user_id))

@app.route('/question_list', methods=['GET', 'POST'])
def question_list():
	return render_template('question_list.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
	return render_template('question.html')

@app.route('/submission', methods=['GET', 'POST'])
def submission():
	return render_template('submission.html')

@app.route('/')
def index():
	# 公告

	# 最新問題，目前列出前五個最新的問題
	uid_change_name = []
	questions = Problem.query.order_by(Problem.uid.desc()).all()
	for ques_iter in questions:
		Account_search = Account.query.filter(Account.uid == ques_iter.uid).first()
		uid_change_name.append(Account_search.username)
	# Ranklist

	return render_template('index.html', questions=questions, name=uid_change_name)

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
				account = Account(uid=0, username=form.username.data, nickname=form.nickname.data, password=generate_password_hash(form.password.data), email=form.email.data, permLevel=False, signUpTime=date_time, lastLoginTime=date_time, icon=False)
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

@app.route('/setting')
@login_required
def setting():
	# flash('This is setting.')
	return render_template('setting.html')


@app.route('/edit')
def edit():
	return render_template('edit.html')


@app.route('/userinfo')
def userinfo():
	return 'Here is UserINFO'

if __name__ == '__main__':
	if LISTEN_ALL:
		app.run(host='0.0.0.0')
	else:
		app.run()
