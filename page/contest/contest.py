import os
from flask import Flask, Blueprint, render_template, request
import logging
from flask_login import login_user, current_user

from models import Contest, Account, Problem
import utils
from exts import db

log = logging.getLogger('Contest')

contest_page = Blueprint('contest_page',
    __name__,
    template_folder=os.path.join(utils.cur_path(__file__), 'templates'),
    static_folder=os.path.join(utils.cur_path(__file__), 'static'),
    static_url_path='/contest/static')
# TODO: ?????

@contest_page.route('/contest/list', methods=['GET'])
def contest_list_view():
    status = ['??', 'Scheduled', 'Running', 'Ended']
    info = []

    # contest_info, b = .first()
    
    
    for row, username in db.session.query(Contest, Account.username).join(Account, Contest.owner == Account.uid, isouter=True):
        info.append({
            'cid': row.contest_id,
            'title': row.contest_title,
            'status': status[row.status],
            'start_time': str(row.start_time),
            'end_time': str(row.end_time),
            'remaining_time': str(row.end_time-row.start_time),
            'owner': username
        })

    return render_template('contest_list.html', info=info)
    
@contest_page.route('/contest/<int:cid>', methods=['GET'])
def contest_page_view(cid):
    return render_template('contest.html')

# TODO Finish Create Page -- Erichsu
# watch out premlevel
@contest_page.route('/contest/create', methods=['GET', 'POST'])
def create_contest_view():

    if request.method == 'POST':

        title = request.form['Title']
        StartDate = request.form['StartDate']
        EndDate = request.form['EndDate']
        problem_num = int(request.form['problem_num'])
        problems = ''

        for i in range(problem_num):
            tmp = (request.form['problem_'+str(i+1)].split(' '))[0][1:]
            problems += tmp+','

        query = Contest(contest_title=title,
                    problem_id=problems,
                    owner=current_user.uid,
                    start_time = StartDate,
                    end_time = EndDate,
                    status = 1)
        db.session.add(query)
        db.session.commit()

        log.debug('Add Contest title={}'.format(title))

    return render_template('create_contest.html')


@contest_page.route('/contest/getproblem', methods=['GET'])
def get_problem():
    problem_info = db.session.query(Problem.problem_id, Problem.problemName).all()
    print(problem_info)
    return {
        'result': 'success',
        'data': {
            'problem_info': problem_info,
        }
    }, 200

# TODO Default DateTime
    
    
