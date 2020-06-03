from flask import Flask, Blueprint, redirect, url_for, abort
import os, logging

import utils
from models import Submission, Account

log = logging.getLogger('API')

api_blueprint = Blueprint('api_blueprint',
    __name__,
    template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@api_blueprint.route('/api/rejudge/<int:subid>', methods=["GET"])
def rejudge_submission(subid):
    log.info('Rejudge {}'.format(subid))
    import judger_utils
    judger_utils.rejudge(subid)
    return {
        'result': 'redjuge',
        'submission': subid,
        'redirect': url_for('submissions_page.submissions_handle')
    }

@api_blueprint.route('/api/submission/<int:submission_id>', methods=['GET'])
def submission_info(submission_id):
    submission = Submission.query.filter_by(submit_id=submission_id).first()
    if not submission:
        return {
            'message': 'Submission {} not found'.format(submission_id),
            'result': 'fail'
        }, 404
    # Get user info
    user = Account.query.get(submission.account_id)
    username = user.username if user else 'Unknown'
    nickname = user.nickname if user else 'Unknown'
    # Get run memory
    if submission.resMem > 1000:
        mem_usage = '{} MiB'.format(submission.resMem / 1000.0)
    else:
        mem_usage = '{} KiB'.format(submission.resMem)
    return {
        'result': 'success',
        'submit_id': submission.submit_id,
        'problem_id': username,
        'username': nickname,
        'runtime': submission.resTime,
        'memory': mem_usage,
        'result': submission.result,
        'lang': submission.lang,
        'code_length': '{} KiB'.format(len(submission.code)/1000),
        'date': submission.time.strftime("%Y-%m-%d %H:%M:%S")
    }, 200
