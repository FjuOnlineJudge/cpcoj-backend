from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
import datetime

#oj
import utils

# TODO(roy4801): Rename this to problem_tag_relation
relations = db.Table('relations',
                    db.Column('problem', db.Integer,
                              db.ForeignKey('problem.problem_id')),
                    db.Column('tag', db.Integer,
                              db.ForeignKey('tag.tag_id'))
                    )

# build the tables
class Problem(db.Model):
	__tablename__  = 'problem'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	problem_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	problemName = db.Column(db.String(100), nullable=False, unique=False) # 名稱
	uid = db.Column(db.Integer, nullable=False, unique=False) # problemsetter
	info = db.Column(db.JSON, nullable=False)           # 內容
	build_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now()) # 建立時間

	# Relation
	submission = db.relationship('Submission', backref=db.backref('problem', uselist=False))
	problem_tag = db.relationship('Tag', secondary=relations, lazy='subquery',backref=db.backref('problem', lazy="dynamic"))

	# For debug print
	def __repr__(self):
		return "<Problem {}>".format(self.problem_id)
	def __str__(self):
		info = self.__repr__() + '\n'
		info += utils.str_row('problem_id', self.problem_id)
		info += utils.str_row('problemName', self.problemName)
		info += utils.str_row('uid', self.uid)
		info += utils.str_row('info', self.info)
		info += utils.str_row('build_time', self.build_time)
		return info

class Tag(db.Model):
	__tablename__  = 'tag'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	tag_id = db.Column(db.Integer, primary_key=True, nullable=False)
	tag_name = db.Column(db.String(30), nullable=False, unique=True)
	description = db.Column(db.Text, nullable=True)

	# For debug print
	def __repr__(self):
		return "<Tag {}>".format(self.tag_id)

	def __str__(self):
		info = self.__repr__() + '\n'
		info += utils.str_row('tag_id', self.tag_id)
		info += utils.str_row('tag_name', self.tag_name)
		info += utils.str_row('description', self.description)
		return info

class Account(UserMixin, db.Model):
	__tablename__  = 'account'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	uid = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	nickname = db.Column(db.String(30), nullable=False, unique=False)
	password = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	permLevel = db.Column(db.Integer, nullable=False)
	signUpTime = db.Column(db.DateTime, nullable=False) # 註冊時間
	lastLoginTime = db.Column(db.DateTime, nullable=False) # 最後登入時間
	icon = db.Column(db.Text, nullable=True) # 保留給頭像用

	# Relation
	submission = db.relationship('Submission', backref='account', lazy="dynamic") # one to many

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def get_id(self):
		return self.uid

	def is_active(self):
		return True

	def is_authenticated(self):
		return True

	def is_anoymous(self):
		return False
	# For debug print
	def __repr__(self):
		return "<Account '{}'>".format(self.username)
	def __str__(self):
		info = self.__repr__()+'\n'
		info += utils.str_row('uid', self.uid)
		info += utils.str_row('username', self.username)
		info += utils.str_row('nickname', self.nickname)
		info += utils.str_row('password', self.password)
		info += utils.str_row('email', self.email)
		info += utils.str_row('permLevel', self.permLevel)
		info += utils.str_row('signUpTime', self.signUpTime)
		info += utils.str_row('lastLoginTime', self.lastLoginTime)
		info += utils.str_row('icon', self.icon)
		info += utils.str_row('submission', self.submission)
		return info

class Submission(db.Model):
	__tablename__  = 'submission'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	submit_id     = db.Column(db.Integer, primary_key=True, nullable=False)# 提交題號

	problem_id = db.Column(db.Integer, db.ForeignKey('problem.problem_id'), nullable=True)
	account_id = db.Column(db.Integer, db.ForeignKey('account.uid'), nullable=False)

	result  = db.Column(db.String(10), nullable=False)               # 結果
	result_msg = db.Column(db.Text, nullable=True)                   # 結果訊息
	resTime = db.Column(db.Float, nullable=False)                    # 執行時間
	resMem  = db.Column(db.Float, nullable=False)                    # 執行記憶體
	code    = db.Column(db.Text, nullable=False)                     # 程式碼長度
	lang    = db.Column(db.String(10), nullable=False)               # 語言
	rank    = db.Column(db.Integer, nullable=False)                  # 排名
	time    = db.Column(db.DateTime, nullable=False)                 # 繳交時間

	# For debug print
	def __repr__(self):
		return "<Submission {}>".format(self.submit_id)
	def __str__(self):
		info = self.__repr__() + '\n'
		info += utils.str_row('submit_id', self.submit_id)
		info += utils.str_row('problem_id', self.problem_id)
		info += utils.str_row('account_id', self.account_id)
		info += utils.str_row('result', self.result)
		info += utils.str_row('resTime', self.resTime)
		info += utils.str_row('resMem', self.resMem)
		info += utils.str_row('lang', self.lang)
		info += utils.str_row('rank', self.rank)
		info += utils.str_row('time', self.time)
		info += utils.str_row('code', '')
		info += self.code
		return info

# announce
class Announce(db.Model):
	__tablename__ = 'announce'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}

	announce_id = db.Column(db.Integer, primary_key=True, nullable=False) #公告編號
	title = db.Column(db.String(100), nullable=False) 			  # 標題
	name = db.Column(db.String(100), nullable=False)              # 作者名字
	content = db.Column(db.Text, nullable=False)                  # 內容
	time = db.Column(db.DateTime, nullable=False)                 # 發布時間

# contest
class Contest(db.Model):
	"""
	.. module:: Contest
		:synopsis: A Database Model for Contest
	"""
	__tablename__ = 'contest'
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}

	# Contest ID
	contest_id = db.Column(db.Integer, primary_key=True, nullable=False)
	# Contest Title
	problem_id = db.Column(db.String(50), nullable=False)
	# Contest Owner - uid
	owner = db.Column(db.String(50), nullable=False)
	# Contest Start-Time
	start_time = db.Column(db.DateTime, nullable=False)
	# Contest End-Time
	end_time = db.Column(db.DateTime, nullable=False)
	# Contest Paticipant
	paticipant = db.Column(db.String(200), nullable=True)
	# Contest Status
	statuc = db.Column(db.Integer, nullable=False)