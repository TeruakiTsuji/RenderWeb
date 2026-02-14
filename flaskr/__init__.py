from flask import Flask
app = Flask(__name__)
import flaskr.main

import os
app.secret_key = os.urandom(24) # セッションキーの設定

from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1) # データを保持する時間の設定

from flaskr import db
db.create_expenses_table()

from . import Global_function
Global_function.set_global()