from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
import os, json

import utils
from models import Problem, Account, Tag
from exts import db

edit_problem_page = Blueprint('edit_problem_page'
                    , __name__
                    , template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

class EditProblemForm(FlaskForm):
    problem_name = StringField('problemName', validators=[
        DataRequired(message='題目名稱不能為空')
    ])
    tags = StringField('tags')
    description = TextAreaField('description')
    input_format = TextAreaField('inputFormat')
    output_format = TextAreaField('outputFormat')
    sample_input = TextAreaField('sampleInput')
    sample_output = TextAreaField('sampleOutput')

# TODO(roy4801): handle the other data (hint, source, td_description, td_num)
@edit_problem_page.route('/problem_edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def problem_edit(pid):
    # current_user = Account.query.first() # debug

    cur_problem = Problem.query.get(pid)
    if not cur_problem:
        # TODO(roy4801): make this auto redirect
        return 'Worng pid'
    if current_user.uid != cur_problem.uid:
        # TODO(roy4801): make this auto redirect
        return redirect(url_for('index'))
    # Prepare the form
    form = EditProblemForm()
    if form.validate_on_submit():
        # problem_name
        cur_problem.problemName = form.problem_name.data
        # tags
        tag_fail_flag = False
        tags = form.tags.data.split(';')
        for i in tags:
            tag = Tag.query.filter_by(tag_name=i).first()
            if tag:
                if tag not in cur_problem.problem_tag:
                    cur_problem.problem_tag.append(tag)
            else:
                flash('錯誤的tag', 'danger')
                tag_fail_flag = True
        # other
        if not tag_fail_flag:
            info = json.loads(cur_problem.info)
            info['description']   = form.description.data
            info['input_format']  = form.input_format.data
            info['output_format'] = form.output_format.data
            info['sample_input']  = form.sample_input.data
            info['sample_output'] = form.sample_output.data
            cur_problem.info = json.dumps(info)
            db.session.commit()
            flash('修改成功', 'success')

    # present the data
    form.problem_name.data = cur_problem.problemName
    # tags
    tmp = ''
    flag = False
    for i in cur_problem.problem_tag:
        tmp += ';' if flag else ''
        tmp += i.tag_name
        flag = True

    form.tags.data = tmp
    info = json.loads(cur_problem.info)
    form.description.data   = info['description']
    form.input_format.data  = info['input_format']
    form.output_format.data = info['output_format']
    form.sample_input.data  = info['sample_input']
    form.sample_output.data = info['sample_output']

    return render_template('problem_edit.html'
        , form=form
        , form_action=url_for('.problem_edit', pid=pid))

# TODO(roy4801): handle the other data (hint, source, td_description, td_num)
@edit_problem_page.route('/new_problem', methods=['GET', 'POST'])
@login_required
def new_problem():
    # current_user = Account.query.first() #debug
    if current_user.permLevel > 1:
        return redirect(url_for('index'))
    form = EditProblemForm()
    if form.validate_on_submit():
        # tag
        appen_tag = []
        tags = form.tags.data.split(';')
        for t in tags:
            db_tag = Tag.query.filter_by(tag_name=t).first()
            if db_tag:
                appen_tag.append(db_tag)
        # info
        info = {'description': '', 'input_format': '', 'output_format': '', 'sample_input': '', 'sample_output': '', 'hint': '', 'source': '', 'td_description': '', 'td_num': ''}
        info['description']   = form.description.data
        info['input_format']  = form.input_format.data
        info['output_format'] = form.output_format.data
        info['sample_input']  = form.sample_input.data
        info['sample_output'] = form.sample_output.data
        new_prob = Problem(problemName=form.problem_name.data
                           , uid=current_user.uid
                           , info=json.dumps(info))
        new_prob.problem_tag = appen_tag
        db.session.add(new_prob)
        db.session.commit()
        flash('新增成功', 'success')
    return render_template('problem_edit.html'
        , form=form
        , form_action=url_for('.new_problem'))
