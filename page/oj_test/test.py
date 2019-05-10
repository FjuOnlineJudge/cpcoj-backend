from flask import Flask, Blueprint, render_template, request, flash, escape
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, validators
import os, datetime

# oj
import utils
from exts import db
from ext_app import app
from models import Account, Submission, Problem

test_page = Blueprint('test_page'
					, __name__
					, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@test_page.route('/test/', methods=['GET'])
def test_handle():
	return 'test'

@test_page.route('/test/genprob')
@test_page.route('/test/genprob/<string:name>')
def test_generate_problem(name='TEST'):
	prob = Problem(problemName=name, uid=1, info='hello', build_time=datetime.datetime.now())

	db.session.add(prob)
	db.session.commit()
	return 'Added!'

@test_page.route('/test/subt', methods=['GET'])
def test_submission():
	acc = Account.query.get(1)
	prob = Problem.query.get(1)
	s = Submission(result='AC', resTime=87.0, resMem=8787.0, code='test'
		, lang='cpp', rank=9000, time=datetime.datetime.now()
		,account=acc, problem=prob)

	db.session.add(s)
	db.session.commit()
	return '<pre>{}</pre>'.format(escape(acc))

@test_page.route('/test/q/<string:name>')
def test_query_user(name):
	acc = Account.query.filter_by(username=name).first()

	s = ''
	if acc != None:
		s += str(acc) + '\n'
		s += '=============================\n'
		for j in acc.submission:
			s += str(j) + '\n'
			s += str(j.problem)
			s += '=============================\n'
	else:
		s = 'Not Found'

	return '<pre>{}</pre>'.format(escape(s))

@test_page.route('/test/log')
def test_log():
	log = None
	with open('log/oj.log') as f:
		log = f.readlines()

	return '<div id="data"><pre>{}</pre></div>'.format(''.join(log))

class FormTestDB_prob(FlaskForm):
	num = IntegerField('Times', validators=[
			validators.DataRequired()
		])
	problem_name = StringField('ProblemName'
		, validators=[
			validators.DataRequired()
		])

	uid = StringField('Author'
		, validators=[
			validators.DataRequired()
		])

	info = TextAreaField('info'
		, validators=[
			validators.DataRequired()
		])

	# build_time = DateTimeField('Build Time')
	submit = SubmitField('Submit')

	def __repr__(self):
		return '<FormTestDB_prob {}>'.format(hex(id(self)))
	def __str__(self):
		info = self.__repr__() + '\n  '
		info += 'num=' + str(self.num.data) + '\n  '
		info += 'problem_name='+str(self.problem_name.data) + '\n  '
		info += 'uid=' + str(self.uid.data) + '\n  '
		info += 'info=\n```\n' + str(self.info.data) + '\n```\n'
		return info

@test_page.route('/test/db/problem', methods=['GET', 'POST'])
def test_add_db_problem():
	form = FormTestDB_prob()
	if request.method == 'POST':
		if form.validate_on_submit():
			print(form)

	return render_template('test_db.html', form=form)