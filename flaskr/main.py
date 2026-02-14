import re
import hashlib
import sqlite3
from flaskr import app
from flask import render_template, request, redirect, url_for, session

from . import global_value as g

from .modules import db_user
from .modules import etc_user
from .modules import db_functions
from .modules import etc_functions
from .modules import etc_date

#--- ログイン認証実装 ---#

@app.route('/')
def index():
  userID = etc_user.userID_session(session, 'user')
  nexts = db_functions.next_all_lst()
  return render_template('index.html', g=g, userID=userID, nexts=nexts)

@app.route('/login')
def login():
  return render_template('login.html', g=g, userID=None)

@app.route('/add')
def add():
  return render_template('add.html', g=g, userID=None)

@app.route('/check', methods=['POST', 'GET'])
def check():
  if request.method == 'POST':
    userID = request.form['userID']
    password1 = request.form['password1']
    password2 = request.form['password2']
    mail = request.form['mail']

    password_pattern = r'^(?=.*[0-9a-zA-Z\W]).{6,}$'
    mail_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    existing_user, existing_mail = db_user.user_mail_lst(userID, mail)
    if userID and password1 and password2 and mail and password1 == password2 and re.match(password_pattern, password1) and re.match(mail_pattern, mail) and not(existing_user) and not(existing_mail):
      user = {
        'userID' : userID,
        'password' : password1,
        'mail' : mail
      }
      session['user'] = user
      return render_template('check.html', g=g, user=user, userID=userID)
    elif password1 != password2:
      error = "入力されたパスワードと確認用のパスワードが異なります"
    elif not(userID and password1 and password2 and mail):
      error = "全ての項目を入力してください"
    elif not(re.match(password_pattern, password1)):
      error = "パスワードは次の条件を満たしている必要があります。半角英数字記号を使用、6文字以上"
    elif not(re.match(mail_pattern, mail)):
      error = "正しいメールアドレスの形式ではありません。"
    elif existing_user:
      error = "ユーザーIDが既に存在します。別のユーザーIDを設定してください。"
    elif existing_mail:
      error = "このメールアドレスは既に登録されています。"
    # if文の外に記述すること
    return render_template('add.html', g=g, error=error, userID=None)
  else:
    return redirect(url_for('index'))
 
@app.route('/comp', methods=['POST', 'GET'])
def comp():
  if request.method == 'POST':
    user = session.get('user')
    hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
    db_user.user_insert(user['userID'], hashed_password, user['mail'])
    return render_template('comp.html', g=g)
  else:
    return redirect(url_for('index'))
 
@app.route('/top', methods=['GET', 'POST'])
def top():
  if request.method == 'POST':
    userID = request.form['userID']
    hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    existing = db_user.user_passwd_lst(userID, hashed_password)
    if existing:
      session['userID'] = userID
      nexts = db_functions.next_all_lst()
      return render_template('top.html', g=g, userID=userID, nexts=nexts)
    else:
      error = 'ユーザーIDかパスワードが間違っています。'
      return render_template('login.html', g=g, error=error, userID=None)
  else:
    if 'userID' in session:
      userID = session['userID']
      nexts = db_functions.next_all_lst()
      return render_template('top.html', g=g, userID=userID)
    else:
      error = '長時間操作が行われなかったため、ログアウトしました。'
      return render_template('login.html', g=g, error=error, userID=None)
  
@app.route('/logout')
def logout():
  session.pop('userID', None)
  return redirect(url_for('login'))

#--- アプリ実装 ---#

@app.route('/pairs_lst')
def pairs_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  next_info = db_functions.next_info(None)
  pairs, person = db_functions.pairs_lst()
  return render_template('pairs.html', g=g, userID=userID, next_info=next_info, pairs=pairs, person=person)

@app.route('/victor_lst') # kind=kind_id
def victor_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  kind = request.args.get('kind')
  if kind is None:
    kind = g.Kind_mc
  kindNm = etc_functions.kind2name(kind)
  victor_lst = db_functions.victor_lst(kind)
  return render_template('victor.html', g=g, userID=userID, victor_lst=victor_lst, kindNm=kindNm, kind=kind)

@app.route('/ymd_lst')  # ymd=20260117
def ymd_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  next_val = request.args.get('next')
  kind = request.args.get('kind')
  ymd_val = request.args.get('ymd')
  all_ymd = db_functions.all_open_dt(kind)
  ymd = etc_functions.next_ymd(all_ymd, next_val, ymd_val)
  place_info = db_functions.place_info(ymd)
  if place_info is None:
    kind = g.Kind_mc
  else:
    kind = place_info['kind']
  kindNm = etc_functions.kind2name(kind)
  ymd_lst = db_functions.ymd_lst(ymd)
  return render_template('ymd.html', g=g, userID=userID, place_info=place_info, ymd_lst=ymd_lst, kind=kind, kindNm=kindNm)

@app.route('/year_lst')
def year_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  year = request.args.get('year')
  if year is not None:
    year = int(year)
  else:
    year = etc_date.this_year()
  prev_year = str(year - 1)
  next_year = str(year + 1)
  year = str(year)
  kind = request.args.get('kind')
  if kind is None:
    kind = g.Kind_mc
  places = db_functions.place_lst(year, kind)
  points = db_functions.point_lst(year, kind)
  return render_template('year.html', g=g, userID=userID, year=year, prev_year=prev_year, next_year=next_year, kind=kind, places=places, points=points)

@app.route('/menu_lst')
def menu_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  next_day = db_functions.next_day()
  next_info = db_functions.next_info(None)
  menu_lst = db_functions.menu_lst(next_info['open_dt'])
  str_dt = str(int(next_info['open_dt']) - 8)
  closing_dt = etc_date.jp_date_ymd_week(str_dt)
  return render_template('menu.html', g=g, userID=userID, next_info=next_info, closing_dt=closing_dt, menu_lst=menu_lst)

@app.route('/hdcp_lst')
def hdcp_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  detail = request.args.get('detail')
  next_info = db_functions.next_info(None)
  hdcp_lst = db_functions.hdcp_lst(next_info['open_dt'], detail)
  return render_template('hdcp.html', g=g, userID=userID, next_info=next_info, hdcp_lst=hdcp_lst, detail=detail)

@app.route('/text_pairing_lst')
def text_pairing_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  next_info = db_functions.next_info(None)
  pairs, person = db_functions.pairs_lst()
  return render_template('text_pairs.html', g=g, userID=userID, next_info=next_info, pairs=pairs, person=person)

@app.route('/bg_lst')
def bg_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  bg_lst = db_functions.bg_lst()
  return render_template('bg.html', g=g, userID=userID, bg_lst=bg_lst)

@app.route('/memo_lst')
def memo_lst():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  memo_lst = db_functions.memo_lst()
  return render_template('memo.html', g=g, userID=userID, memo_lst=memo_lst)

@app.route('/award_lst')
def award_lst():
  userID = etc_user.userID_session(session, 'user')
  num = request.args.get('num')
  if num is not None:
      num = int(num)
  else:
      num = 20
  #
  award = etc_functions.award_info(num)
  award_lst = etc_functions.awars_lst(award)
  return render_template('award.html', g=g, userID=userID, award_lst=award_lst, num=num)

@app.route('/pairs_upd')
def pairs_upd():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  return render_template('pairs_upd.html', g=g, userID=userID)

@app.route('/pay_upd')
def pay_upd():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  return render_template('pay_upd.html', g=g, userID=userID)

@app.route('/next_upd')
def next_upd():
  userID = etc_user.userID_session(session, 'user')
  if userID is None:
    return redirect(url_for('login'))
  return render_template('next_upd.html', g=g, userID=userID)

