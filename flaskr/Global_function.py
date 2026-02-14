from . import global_value as g
import configparser

def set_global():
    # --------------------------------------------------
    # configparserの宣言とiniファイルの読み込み
    # --------------------------------------------------
    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')
    # --------------------------------------------------
    # config,iniから値取得
    # --------------------------------------------------
    g.Cup_Name = config_ini['DEFAULT']['Cup_Name']
