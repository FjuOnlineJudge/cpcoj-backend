import os
from flask import Flask, Blueprint, render_template, request, url_for
import logging, random, string
from flask_login import login_user, current_user, LoginManager

from datetime import datetime
from models import Contest, Account, Problem, Submission
import utils
from exts import db

log = logging.getLogger('Contest')

contest_page = Blueprint('contest_page',
    __name__,
    template_folder=os.path.join(utils.cur_path(__file__), 'templates'),
    static_folder=os.path.join(utils.cur_path(__file__), 'static'),
    static_url_path='/contest/static')
# TODO: ?????

def gen_random_str(size=4):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


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

    contest_info = db.session.query(Contest).filter(Contest.contest_id == cid).first()
    
    print(contest_info.problem_id)

    problem_id = []

    for i in (contest_info.problem_id.strip('\n').split(',')):
        if(i != ''):
            problem_id.append(int(i))

        # Submission
    sub_list = Submission.query
    sub_list = sub_list\
                    .order_by(Submission.submit_id.desc())\
                    .filter(Submission.for_test == cid)\
                    .all()


    for i in sub_list:
        # Rejudge button (check if the user is admin)
        if current_user.is_authenticated and current_user.permLevel <= 0:
            setattr(i, 'rejudge_link', url_for('api_blueprint.rejudge_submission', subid=i.submit_id)) # rejudge link

        # Set `submitter`
        u = Account.query.get(i.account_id)
        setattr(i, 'submitter', u.nickname if u else 'Unknown')
        setattr(i, 'username', u.username if u else None)

        # Set `codeLen`
        codeLength = '{:.2f} KiB'.format(len(i.code)/1000)
        setattr(i, 'codeLen', codeLength)

        # Set `score`
        # TODO(roy4801): implement score
        setattr(i, 'score', 'NaN')

        # CE modal
        if i.result == 'CE':
            setattr(i, 'ce_id_str', gen_random_str(8))


    print(sub_list)
    
    return render_template('contest.html', sub_list=sub_list, is_admin=current_user.is_authenticated, info={
        'cid': contest_info.contest_id,
        'title': contest_info.contest_title,
        'problem_id': problem_id,
        'start_time': contest_info.start_time,
        'end_time': contest_info.end_time
    })

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
def cmp_items(a, b):
    if a['penalty'] > b['penalty']:
        return 1
    elif a['penalty'] == b['penalty']:
        return 0
    else:
        return -1
    
@contest_page.route('/contest/getrank/<int:cid>', methods=['GET'])
def get_rank(cid):

    rank_dict = {}
    problem_dict = {}

    contest_info = db.session.query(Contest.paticipant, Contest.problem_id, Contest.start_time)\
                            .filter(Contest.contest_id == cid)\
                            .first()

    contest_starttime = datetime.strptime(str(contest_info.start_time), '%Y-%m-%d %H:%M:%S')

    contest_pro = contest_info.problem_id.strip(',').split(',')
    
    for i in range(len(contest_pro)):
        problem_dict[int(contest_pro[i])] = {
            'AC_time': '-1',
            'Wrong_num': 0
        }
    


    contest_par = contest_info.paticipant.strip(',').split(',')

    for i in range(len(contest_par)): 
        rank_dict[int(contest_par[i])] = {
            'user_name':'',
            'penalty':0,
            'problems':problem_dict
        }

    user_list = Account.query.all()
    
    for i in user_list:
        if i.uid in rank_dict:
            rank_dict[i.uid]['user_name'] = i.username


    sub_list = Submission.query
    sub_list = sub_list.filter(Submission.for_test == cid)\
                        .order_by(Submission.submit_id)\
                        .all()
    from operator import itemgetter, attrgetter, getitem

    for sub in sub_list:
        if rank_dict[sub.account_id]['problems'][sub.problem_id]['AC_time'] == '-1':
            if sub.result == 'AC':
                sub_datetime = datetime.strptime(str(sub.time), '%Y-%m-%d %H:%M:%S')
                rank_dict[sub.account_id]['problems'][sub.problem_id]['AC_time'] = sub.time
                rank_dict[sub.account_id]['penalty'] = (sub_datetime-contest_starttime).days + rank_dict[sub.account_id]['problems'][sub.problem_id]['Wrong_num']*20
            else:
                rank_dict[sub.account_id]['problems'][sub.problem_id]['Wrong_num'] += 1

    rank_dict = sorted(rank_dict.items(),key=lambda x:getitem(x[1],'penalty'), reverse=True)

    return {
        'result': 'success',
        'rank': rank_dict
        }

    
