from flask import Flask, Blueprint, redirect, url_for
import os, logging

import utils

log = logging.getLogger('API')

api_blueprint = Blueprint('api_blueprint',
    __name__,
    template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@api_blueprint.route('/api/rejudge/<int:subid>', methods=["GET"])
def rejudge_submission(subid):
    import judger_utils
    judger_utils.rejudge(subid)
    return {
        'result': 'redjuge',
        'submission': subid,
        'redirect': url_for('submissions_page.submissions_handle')
    }
