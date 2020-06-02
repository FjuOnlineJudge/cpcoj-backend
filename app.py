#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session, flash, escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, LoginManager, logout_user
import datetime, json, logging

from form import *
from exts import db
from models import Problem, Account, Submission, Tag, Announce
import config

# Dealing with the path problem
import sys
sys.path.append('page')
sys.path.append('judger')

from ext_app import app

# Test for custom filter
## ref:http://flask.pocoo.org/snippets/28/
import re
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    # result = u'\n\n'.join(u'<p style="margin: 0px">%s</p>' % p.replace('\n', '<br>\n')
    #                       for p in _paragraph_re.split(escape(value)))
    result = value.replace('\n', '<br>\n')
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
###

# Register blueprints
from page import submit
app.register_blueprint(submit.submit_page)

from oj_test import test
app.register_blueprint(test.test_page)

from page import submissions
app.register_blueprint(submissions.submissions_page)

from page import edit_problem
app.register_blueprint(edit_problem.edit_problem_page)

from page import ranking
app.register_blueprint(ranking.ranking_page)

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
    # If the pid is invalid, go to problem_list
    if not problem:
        return redirect(url_for('problem_list'))

    author = Account.query.filter(Account.uid == problem.uid).first()

    total_submit = Submission.query.filter_by(problem_id=problem.problem_id).count()
    total_ac = Submission.query.filter_by(problem_id=problem.problem_id).filter_by(result="AC").count()
    subinfo = (total_ac, total_submit)
    tags = problem.problem_tag
    # TODO(roy4801): maybe there's json injection
    info = json.loads(problem.info)

    # if the current_user is able to edit the problem
    editable = False
    if hasattr(current_user, 'uid') and current_user.uid == problem.uid:
        editable = True

    return render_template('problem.html'
                        , problem=problem
                        , author=author
                        , subinfo=subinfo
                        , tags=tags
                        , info=info
                        , editable=editable)

@app.route('/sub_detail', methods=['GET', 'POST'])
def submission_detail():
    return render_template('sub_detail.html')

@app.route('/announce', methods=['GET', 'POST'])
@login_required
def announce():
    form = FormAnnounce()
    date_time = datetime.datetime.now()

    if request.method == 'POST':
        if form.validate_on_submit():
            announce = Announce(title=form.title.data
                                , name=current_user.username
                                , content=form.content.data
                                , time=date_time)
            db.session.add(announce)
            db.session.commit()
            flash('發布成功', 'success')

    return render_template('announce.html', form=form)

@app.route('/announce/<int:aid>', methods=['GET'])
def announce_id(aid):
    ann = Announce.query.filter(Announce.announce_id == aid).first()
    if ann:
        # ann.content = escape(ann.content)
        return render_template('announce_show.html', announce=ann)
    else:
        # TODO: make a redirect page for waiting
        return redirect(url_for('index'))

@app.route('/announce_list', methods=['GET', 'POST'])
def announce_list():
    announce = Announce.query.order_by(Announce.time.desc()).all()
    return render_template('announce_list.html', announce=announce)

@app.route('/announce_edit/<int:aidd>', methods=['GET', 'POST'])
@login_required
def announce_edit(aidd):
    form = FormAnnounce()
    date_time = datetime.datetime.now()
    ann = Announce.query.filter(Announce.announce_id == aidd).first()

    if current_user.permLevel <= 0:
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.validate_on_submit():
                    ann.title = form.title.data
                    ann.content = form.content.data
                    ann.time = date_time
                    db.session.commit()
                    flash('更改成功', 'success')
            else:
                # TODO(roy4801): Add form.error to flash in template
                flash('更改失敗', 'danger')
        return render_template('announce_edit.html', form=form, ann=ann)
    else:
        return redirect(url_for('announce'))

@app.route('/')
def index():
    # TODO: refactoring
    # 公告
    announce = Announce.query.order_by(Announce.time.desc()).all()

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
        # total_ac = all_user[idx].submission.filter_by(result='AC').count()
        # tried = all_user[idx].submission.order_by(Submission.problem_id).group_by(Submission.problem_id).count()
        real_ac = all_user[idx].submission.filter_by(result='AC') \
                    .order_by(Submission.problem_id)              \
                    .group_by(Submission.problem_id).count()
        # calc ac_rate
        ac_rate = real_ac / total_submit * 100 if total_submit != 0 else 0.0
        ranklist.append({
            'name': all_user[idx].username,
            'real_ac': real_ac,
            'ac_rate': ac_rate
        })
    # sort the ranklist with total_ac
    ranklist.sort(key=lambda x: x['real_ac'], reverse=True)

    return render_template('index.html', announce=announce,
                                         questions=questions,
                                         name=author,
                                         ranklist=ranklist)

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger = logging.getLogger('Register')
    form =FormRegister()

    if request.method == 'POST':
        if form.validate_on_submit():
            date_time = datetime.datetime.now()

            # user & email collision
            username = Account.query.filter(Account.username == form.username.data).first()
            email = Account.query.filter(Account.email == form.email.data).first()

            if username:
                flash('{} has been used.'.format(form.username.data))
            if email:
                flash('The email "{}" has been used'.format(form.email.data))

            if not username and not email:
                logger.debug('{} {} {}'.format(form.username.data, form.password.data, form.email.data))
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
                return redirect(url_for('login'))

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

                if 'next' in request.values and request.values['next'] != '/logout':
                    # TODO(roy4801): Possibe CSRF
                    return redirect(request.values['next'])
                else:
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
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
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

    if not target:
        #TODO (halloworld) response 404
        return redirect(url_for('index'))

    total_submit = target.submission.order_by(Submission.problem_id).all()
    total_ac = target.submission.filter_by(result = "AC").all()
    tried = target.submission.order_by(Submission.problem_id).group_by(Submission.problem_id).all()
    real_ac = target.submission.filter_by(result = "AC").order_by(Submission.problem_id).group_by(Submission.problem_id).all()

    wrong = []
    wrong = list(set(tried) - set(real_ac))

    return render_template('userinfo.html',
        info=target,
        total_submit=total_submit,
        total_ac=total_ac,
        tried=tried,
        real_ac=real_ac,
        wrong=wrong)

@app.route('/about', methods=['GET'])
def about_page():
    """
    Page for the site info.

    Args:

    Returns:
        render_template('about.html'): Return the page about.html/
    """
    return render_template('about.html')

import click

@click.command()
@click.option('-p', '--port', default=80, help='Port number')
@click.option('-l', '--listen', default='0.0.0.0', help='Listen address')
@click.option('-d', '--debug', is_flag=True, help='Debug mode')
def runserver(port, listen, debug):
    app.run(host=listen, port=port, debug=debug)

if __name__ == '__main__':
    runserver()
