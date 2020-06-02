import os
from flask import Flask, Blueprint, render_template
import logging

import utils
from models import Account, Submission

log = logging.getLogger('Ranking')

ranking_page = Blueprint('ranking_page',
                        __name__,
                        template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@ranking_page.route('/ranking', methods=['GET'])
def ranking_page_view():
    #TODO (erichsu1224) Add motto, Select Pagez
    """
    Query user's info from database. And return page rank.html from templetes.

    Args:

    Returns:
        render_template('rank.html', user_info=target): Return the page rank.html and paremeter target(user_info) to html.
    """
    target = list()

    query_target = Account.query.filter_by().all()

    for target_user in query_target:
        total_submit = target_user.submission.order_by(
            Submission.problem_id).all()
        total_ac = target_user.submission.filter_by(result="AC").all()

        user_info = {}

        user_info['username'] = target_user.username
        user_info['nickname'] = target_user.nickname
        user_info['total_ac'] = total_ac
        user_info['total_submit'] = total_submit

        target.append(user_info)

    target = sorted(target, key=lambda k: len(k['total_ac']), reverse=True)

    return render_template('rank.html', user_info=target)
