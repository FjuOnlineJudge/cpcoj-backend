from flask import Flask, Blueprint, render_template, request, flash, escape
import os, datetime

# oj
import utils
from exts import db
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

	for t in log:
		if 'GET /test/log' in t:
			log.remove(t)
	if log:
		log.reverse()
	return '<pre>{}</pre>'.format(''.join(log))