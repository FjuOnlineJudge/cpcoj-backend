import os
from flask import Flask, Blueprint, render_template
import logging

from models import Contest
import utils

log = logging.getLogger('Contest')

contest_page = Blueprint('contest_page',
                        __name__,
                        template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@contest_page.route('/contest_list', methods=['GET'])
def contest_list_view():
    info = list()
    info.append({
        'cid': 1,
        'title': 'testing_Contest1',
        'status': 'Ended',
        'Start_time': '2020-06-04 18:00:00',
        'End_time': '2020-06-04 20:00:00',
        'Remaining_time': '2:00:00',
        'Owner': 'erichsu'
    })

    info.append({
        'cid': 2,
        'title': 'testing_Contest2',
        'status': 'Running',
        'Start_time': '2020-06-04 20:00:00',
        'End_time': '2020-06-04 22:00:00',
        'Remaining_time': '2:00:00',
        'Owner': 'erichsu'
    })

    return render_template('contest_list.html', info=info)
    
@contest_page.route('/contest/<int:cid>', methods=['GET'])
def contest_page_view(cid):

    return render_template('contest.html')