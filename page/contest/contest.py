import os
from flask import Flask, Blueprint, render_template, request
import logging

from models import Contest, Account
import utils
from exts import db

log = logging.getLogger('Contest')

contest_page = Blueprint('contest_page',
    __name__,
    template_folder=os.path.join(utils.cur_path(__file__), 'templates'),
    static_folder=os.path.join(utils.cur_path(__file__), 'static'),
    static_url_path='/contest/static')
# TODO: ?????

@contest_page.route('/contest_list', methods=['GET'])
def contest_list_view():
    status = ['??', 'Scheduled', 'Running', 'Ended']
    info = []

    # contest_info, b = .first()
    
    
    for row, username in db.session.query(Contest, Account.username).join(Account, Contest.owner == Account.uid, isouter=True):
        print(type(row))
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
@contest_page.route('/create_contest', methods=['GET'])
def create_contest_view():
    return render_template('create_contest.html')