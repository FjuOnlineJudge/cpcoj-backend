from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, RadioField, SelectMultipleField, validators
import os, datetime, logging

# oj
import utils

log = logging.getLogger('test')

test_page = Blueprint('test_page'
					, __name__
					, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@test_page.route('/test/rejudge/<int:subid>', methods=['GET'])
def test_rejudge(subid):
	import judger_utils
	judger_utils.rejudge(subid)
	return redirect(url_for('submissions_page.submissions_handle'))
