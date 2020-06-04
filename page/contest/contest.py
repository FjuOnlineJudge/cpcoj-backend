import os
from flask import Flask, Blueprint, render_template
import logging

import utils

log = logging.getLogger('Contest')

contest_page = Blueprint('contest_page',
                        __name__,
                        template_folder=os.path.join(utils.cur_path(__file__), 'templates'))

@contest_page.route('/contest', methods=['GET'])
def contest_page_view():
    return render_template('contest.html')