import json, logging
# oj
from judger import judge, manage
from exts import db
from ext_app import app

from models import Submission, Problem

log = logging.getLogger('Judger')

def rejudge(sub_id):
    with app.app_context(): # db access
        sub = Submission.query.get(sub_id)
        if sub:
            log.debug('Start to rejudge sub #{}'.format(sub_id))
            prob = Problem.query.get(sub.problem_id)
            manage.add_judger(sub.submit_id, sub.problem_id,
                              judge.JUDGE_CPP, sub.code, 3.0, 65536, int(json.loads(prob.info)['td_num']))
