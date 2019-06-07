from flask import Flask, Blueprint, render_template, request, flash, escape
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, validators
import os, datetime, logging

# oj
import utils
from exts import db
from ext_app import app
from models import Account, Submission, Problem, Tag

log = logging.getLogger('test')

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

	problem_id = IntegerField('problemID'
		, validators=[
			validators.Optional()
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

class FormTestDB_delProb(FlaskForm):
	problem_id = StringField('problemID', validators=[
		validators.DataRequired()
	])

	del_btn = SubmitField('Delete')

@test_page.route('/test/db/<path:arg>', methods=['GET', 'POST'])
def test_handle_db(arg):
	arg = arg.split('/')

	if arg[0] == 'e':
		if arg[1] == 'problem':
			form = FormTestDB_prob()
			del_form = FormTestDB_delProb()
			return handle_e_problem(form, del_form, request)
	elif arg[0] == 'l':
		if arg[1] == 'problem':
			return list_db_table(Problem, '/'.join(arg))
		elif arg[1] == 'submission':
			return list_db_table(Submission, '/'.join(arg))

	return escape('Usage: /test/db/<operation>/<table>')

def handle_e_problem(form, del_form, request):
	with app.app_context():
		if request.method == 'POST':
			flag = False
			if not flag and form.validate_on_submit():
				flag = True
				for i in range(int(form.num.data)):
					log.debug('Add problem {} {}/{}'.format(form.problem_name.data, i, form.num.data))
					prob = Problem(problem_id=form.problem_id.data, problemName=form.problem_name.data
						, uid=form.uid.data
						, info=form.info.data
					)

					# set tag
					goal = Tag.query.get(1)
					prob.problem_tag.append(goal)
					goal = Tag.query.get(2)
					prob.problem_tag.append(goal)

					db.session.add(prob)
					db.session.commit()
			if not flag and del_form.validate_on_submit():
				i = del_form.problem_id.data
				l = 0
				r = 0

				if '-' in i:
					l, r = i.split('-')
					l = int(l)
					r = int(r)
				else:
					l = int(i)
					r = l
				for a in range(l, r+1):
					prob = Problem.query.get(a)
					if prob:
						log.debug('Delete the {} problem'.format(a))
						db.session.delete(prob)
						db.session.commit()

	return render_template('test_db.html', form=form, del_form=del_form, path='e/problem')

def list_db_table(database, path):
	with app.app_context():
		l = database.query.all()
	return render_template('test_db_list.html', list=l, path=path)

# tag test
class FormTestDB_tag(FlaskForm):
	tag_id = IntegerField('Tag_id', validators=[
            validators.DataRequired()
        ])

	tag_name = StringField('Tag_name', validators=[
            validators.DataRequired()
        ])

	description = StringField('Description', validators=[
            validators.DataRequired()
        ])

	submit = SubmitField('Submit')


	def __str__(self):
		info = self.__repr__() + '\n  '
		info += 'tag_id=' + str(self.tag_id.data) + '\n  '
		info += 'tag_name='+str(self.tag_name.data) + '\n  '
		info += 'description=' + str(self.description.data) + '\n  '
		return info

@test_page.route('/test/tag', methods=['GET', 'POST'])
def tag():
	form = FormTestDB_tag()
	if request.method == 'POST':
		tag = Tag(tag_id=form.tag_id.data, tag_name=form.tag_name.data, description=form.description.data)
		db.session.add(tag)
		db.session.commit()
		return 'OK'

	return render_template('test_tag.html', form=form)





	


