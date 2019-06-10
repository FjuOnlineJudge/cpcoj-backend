from flask import Flask, Blueprint, render_template
import os, logging

log = logging.getLogger('Admin Panel')

admin_page = Blueprint('admin_page'
                    , __name__
                    , template_folder=os.path.join(utils.cur_path(__file__), 'templates'))