from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
import os

# oj
import utils

submissions_page = Blueprint('submissions_page'
						, __name__
						, template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@submissions_page.route('/submissions', methods=['GET', 'POST'])
def submissions_handle():
	return render_template('submissions.html')
