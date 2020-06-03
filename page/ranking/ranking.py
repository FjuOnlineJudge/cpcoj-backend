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
            Submission.problem_id).count()
        real_ac = target_user.submission.filter_by(result='AC') \
                    .order_by(Submission.problem_id)              \
                    .group_by(Submission.problem_id).count()
        
        print(type(real_ac), type(total_submit))
        ac_rate = real_ac / total_submit * 100 if total_submit != 0 else 0.0
        

        target.append({
            'username': target_user.username,
            'nickname': target_user.nickname,
            'real_ac': real_ac,
            'total_submit': total_submit,
            'ac_rate': ac_rate
        })

    target = sorted(target, key=lambda k: k['real_ac'], reverse=True)

    return render_template('rank.html', user_info=target)
