import sqlite3

from ..import global_value as g

from . import etc_date
from . import etc_functions

DATABASE = "storage.sqlite"

def next_all_lst():
    yyyy = "2026"
    query = "SELECT * from trn_next WHERE substr(open_dt,1,4) = ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    nexts = db.execute(query, (yyyy,)).fetchall()
    db.close()

    ret = []
    for item in nexts:
        jp_date = etc_date.jp_date_md_week(item['open_dt'])
        row = {'title' : item['title'], 'open_dt' : item['open_dt'], 'jp_date' : jp_date, 'place' : item['place'], 'pairs' : item['pairs']}
        ret.append(row)
    return ret

def next_one_lst():
    yyyy = etc_date.this_year()
    query = "SELECT * from trn_next WHERE substr(open_dt,1,4) >= ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    nexts = db.execute(query, (yyyy,)).fetchone()
    db.close()

    ret = []
    for item in nexts:
        jp_date = etc_date.jp_date_md_week(item['open_dt'])
        row = {'title' : item['title'], 'open_dt' : item['open_dt'], 'jp_date' : jp_date, 'place' : item['place'], 'pairs' : item['pairs']}
        ret.append(row)
    return ret

def next_day():
    today = etc_date.today()
    query = "SELECT open_dt from trn_next WHERE open_dt >= ?"
    db = sqlite3.connect(DATABASE)
    row = db.execute(query, (today,)).fetchone()
    db.close()
    ret = ""
    if row:
        ret = row[0]
    return ret

def all_users():
    query = "SELECT * from mst_user"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    ret = db.execute(query).fetchall()
    db.close()
    return ret

def all_hdcps(detail):
    day = next_day()
    base_ym = etc_date.hdcp_start_ym(day, 0)
    if detail is None:
        query = "SELECT * from trn_hdcp WHERE base_ym = ? AND cnt = 0"
    else:
        query = "SELECT * from trn_hdcp WHERE base_ym = ?"
    db = sqlite3.connect(DATABASE)
    ret = db.execute(query, (base_ym,)).fetchall()
    db.close()
    return ret

def all_places():
    query = "SELECT * from trn_place WHERE ORDER BY open_dt"
    db = sqlite3.connect(DATABASE)
    ret = db.execute(query).fetchall()
    db.close()
    return ret

def all_open_dt(kind):
    if kind is None:
        kind = g.Kind_mc
    query = "SELECT open_dt from trn_place WHERE kind = ? ORDER BY open_dt"
    db = sqlite3.connect(DATABASE)
    rows = db.execute(query, (kind,)).fetchall()
    db.close()
    ret = []
    for item in rows:
        ret.append(item[0])
    return ret

def next_info(ymd):
    if ymd is None:
        ymd = next_day()
    query = "SELECT * from trn_next WHERE open_dt = ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    row = db.execute(query, (ymd,)).fetchone()
    db.close()
    jp_date = etc_date.jp_date_ymd_week(row['open_dt'])
    ret = {'kind' : g.Kind_mc, 'open_dt' : row['open_dt'], 'jp_date' : jp_date, 'place' : row['place'], 'title' : row['title'], 'pairs' : row['pairs']}
    return ret

def place_info(ymd):
    if ymd is None:
        ymd = next_day()
    query = "SELECT * from trn_place WHERE open_dt = ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    row = db.execute(query, (ymd,)).fetchone()
    db.close()
    jp_date = etc_date.jp_date_ymd_week(row['open_dt'])
    ret = {'kind' : row['kind'], 'open_dt' : row['open_dt'], 'jp_date' : jp_date, 'place' : row['place'], 'name' : row['name'], 'cose1' : row['cose1'], 'cose2' : row['cose2']}
    return ret

def place_lst(year, kind):
    query = "SELECT * from trn_place WHERE SUBSTR(open_dt,1,4) = ? AND kind = ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    rows = db.execute(query, (year, kind)).fetchall()
    db.close()
    users = all_users()
    ret = []
    for item in rows:
        jp_date = etc_date.jp_date_ymd(item['open_dt'])
        victor_nm = etc_functions.name_num2name(users, item['victor'])
        row = {'kind' : item['kind'], 'open_dt' : item['open_dt'], 'jp_date' : jp_date, 'place' : item['place'], \
            'name' : item['name'], 'cose1' : item['cose1'], 'cose2' : item['cose2'], 'victor' : item['victor'], 'victor_nm' : victor_nm}
        ret.append(row)
    return ret

def score_info(place, gross):
    query = "SELECT S.* from trn_score S, trn_place P WHERE S.open_dt = P.open_dt AND P.place = ? AND gross = ? ORDER BY open_dt, num"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    ret = db.execute(query, (place, gross)).fetchall()
    db.close()
    return ret

def pairs_lst():
    day = next_day()
    query = "SELECT * from trn_pairing WHERE open_dt = ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    rows = db.execute(query, (day,)).fetchall()
    db.close()
    users = all_users()
    hdcps = all_hdcps(None)
    menus = menu_lst(day)
    person = 0
    ret = []
    for item in rows:
        name_nm1 = etc_functions.name_num2name(users, item['name_num1'])
        name_nm2 = etc_functions.name_num2name(users, item['name_num2'])
        name_nm3 = etc_functions.name_num2name(users, item['name_num3'])
        name_nm4 = etc_functions.name_num2name(users, item['name_num4'])
        hdcp1 = round(float(etc_functions.name_num2hdcp(hdcps, item['name_num1'])),1)
        hdcp2 = round(float(etc_functions.name_num2hdcp(hdcps, item['name_num2'])),1)
        hdcp3 = round(float(etc_functions.name_num2hdcp(hdcps, item['name_num3'])),1)
        hdcp4 = round(float(etc_functions.name_num2hdcp(hdcps, item['name_num4'])),1)
        menu1 = etc_functions.get_menu_str(etc_functions.name_num2menu(menus, item['name_num1']))
        menu2 = etc_functions.get_menu_str(etc_functions.name_num2menu(menus, item['name_num2']))
        menu3 = etc_functions.get_menu_str(etc_functions.name_num2menu(menus, item['name_num3']))
        menu4 = etc_functions.get_menu_str(etc_functions.name_num2menu(menus, item['name_num4']))
        if not hdcp1:
            hdcp1 = '新ﾍﾟﾘ'
        if not hdcp2:
            hdcp2 = '新ﾍﾟﾘ'
        if not hdcp3:
            hdcp3 = '新ﾍﾟﾘ'
        if not hdcp4:
            hdcp4 = '新ﾍﾟﾘ'
        if name_nm1 == '(空き)':
            hdcp1 = ''
        if name_nm2 == '(空き)':
            hdcp2 = ''
        if name_nm3 == '(空き)':
            hdcp3 = ''
        if name_nm4 == '(空き)':
            hdcp4 = ''
        row = {'start_tm' : item['start_tm'], 'cose1' : item['cose1'], 'cose2' : item['cose2'], \
            'name_num1' : item['name_num1'], 'name_nm1' : name_nm1, \
            'name_num2' : item['name_num2'], 'name_nm2' : name_nm2, \
            'name_num3' : item['name_num3'], 'name_nm3' : name_nm3, \
            'name_num4' : item['name_num4'], 'name_nm4' : name_nm4, \
            'hdcp1' : hdcp1, \
            'hdcp2' : hdcp2, \
            'hdcp3' : hdcp3, \
            'hdcp4' : hdcp4, \
            'menu1' : menu1, \
            'menu2' : menu2, \
            'menu3' : menu3, \
            'menu4' : menu4, \
        }
        if name_nm1 != '(空き)':
            person +=1
        if name_nm2 != '(空き)':
            person +=1
        if name_nm3 != '(空き)':
            person +=1
        if name_nm4 != '(空き)':
            person +=1
        ret.append(row)
    return ret, person

def victor_lst(kind):
    query = "SELECT * from trn_place WHERE kind = ? ORDER BY open_dt DESC"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    rows = db.execute(query, (kind,)).fetchall()
    db.close()
    users = all_users()
    ret = []
    for item in rows:
        jp_date = etc_date.jp_date_ymd(item['open_dt'])
        victor_nm = etc_functions.name_num2name(users, item['victor'])
        row = {'kind' : item['kind'], 'open_dt' : item['open_dt'], 'jp_date' : jp_date, 'place' : item['place'], \
            'name' : item['name'], 'cose1' : item['cose1'], 'cose2' : item['cose2'], 'victor' : item['victor'], 'victor_nm' : victor_nm}
        ret.append(row)
    return ret

def ymd_lst(ymd):
    query = "SELECT * from trn_score WHERE open_dt = ? ORDER BY num"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    rows = db.execute(query, (ymd,)).fetchall()
    db.close()
    users = all_users()
    bg = etc_functions.best_gross(rows)
    ret = []
    for item in rows:
        name_nm = etc_functions.name_num2name(users, item['name_num'])
        bg_mark = etc_functions.bg_mark(item['gross'], bg)
        row = {'name_num' : item['name_num'], 'name_nm' : name_nm, 'score1' : item['score1'], 'score2' : item['score2'], \
            'gross' : item['gross'], 'hdcp' : item['hdcp'], 'net' : item['net'], 'bg_mark' : bg_mark}
        ret.append(row)
    return ret

def point_lst(year, kind):
    query = "SELECT * from trn_score WHERE SUBSTR(open_dt,1,4) = ? ORDER BY open_dt, num"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    rows = db.execute(query, (year,)).fetchall()
    db.close()
    users = all_users()
    points = []
    for row in rows:
        point = 1
        mp1 = 0
        mp2 = 0
        mp3 = 0
        cnt = 1
        if row['num'] == 1:
            point = 11
            mp1 = 1
        elif row['num'] == 2:
            point = 8
            mp2 = 1
        elif row['num'] == 3:
            point = 6
            mp3 = 1
        #
        name_nm = etc_functions.name_num2name(users, row['name_num'])
        items = {'name_num' : row['name_num'], 'name_nm' : name_nm, 'point' : point, 'mp1' : mp1, 'mp2' : mp2, 'mp3' : mp3, 'cnt' : cnt}
        exist_fg = False
        for p in points:
            if p['name_num'] == row['name_num']:
                exist_fg = True
                p['mp1'] = p['mp1'] + mp1
                p['mp2'] = p['mp2'] + mp2
                p['mp3'] = p['mp3'] + mp3
                p['cnt'] = p['cnt'] + cnt
                p['point'] = p['mp1'] * 11 + p['mp2'] * 8 + p['mp3'] * 6 + p['cnt']
                break
            #
        #
        if exist_fg == False:
            points.append(items)
        #
    #
    ret = sorted(points, key=lambda x:x['point'], reverse=True)
    return ret

def menu_lst(ymd):
    query = "SELECT * from trn_menu WHERE open_dt = ?"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    rows = db.execute(query, (ymd,)).fetchall()
    db.close()
    users = all_users()
    ret = []
    for item in rows:
        name_nm = etc_functions.name_num2name(users, item['name_num'])
        menu_nm = item['name_num'] + 'menu'
        row = {'name_num' : item['name_num'], 'name_nm' : name_nm, 'menu_num' : item['menu_num'], 'menu_nm' : menu_nm}
        ret.append(row)
    return ret

def hdcp_lst(ymd, detail):
    hdcps = all_hdcps(detail)
    users = all_users()
    ret = []
    cnt = 0
    save_nm = ''
    for item in hdcps:
        name_nm = etc_functions.name_num2name(users, item[2])
        if name_nm != save_nm:
            cnt = 0
        cnt = cnt + 1
        hdcp = round(float(item[9]),1)
        if detail is None:
            row = {'name_num' : item[2], 'name_nm' : name_nm, 'num' : item[6], 'avr' : item[7], 'adjust' : item[8], 'hdcp' : hdcp}
        else:
            if item[6] != 99:
                jp_date = etc_date.jp_date_ymd_week(item[4])
            else:
                jp_date = ''
            row = {'name_num' : item[2], 'name_nm' : name_nm, 'num' : item[6], 'cnt' : cnt, 'gross' : item[5], \
                'avr' : item[7], 'adjust' : item[8], 'hdcp' : hdcp, 'jp_date' : jp_date}
        ret.append(row)
        save_nm = name_nm
    return ret

def bg_lst():
    ret = []
    w_bg_lst = []
    query = "SELECT P.kind,P.open_dt,P.place,S.score1,S.score2,S.gross FROM trn_place P, trn_score S WHERE P.open_dt=S.open_dt ORDER BY P.place, P.open_dt"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    union_rows = db.execute(query).fetchall()
    db.close()
    #
    s_kind = ''
    s_place = ''
    s_open_dt = ''
    s_score1 = 0
    s_score2 = 0
    s_gross = 999
    s_place = union_rows[0]['place']
    for row in union_rows:
        if row['place'] != s_place:
            item = {'kind' : s_kind, 'place' : s_place, 'open_dt' : s_open_dt, 'score1' : s_score1, 'score2' : s_score2, 'gross' : s_gross}
            w_bg_lst.append(item)
            s_kind = ''
            s_place = ''
            s_open_dt = ''
            s_score1 = 0
            s_score2 = 0
            s_gross = 999
        #
        if row['score1'] > 0 and row['score2'] > 0 and row['gross'] < s_gross:
            s_kind = row['kind']
            s_place = row['place']
            s_open_dt = row['open_dt']
            s_score1 = row['score1']
            s_score2 = row['score2']
            s_gross = row['gross']
        #
        s_place = row['place']
    #
    item = {'kind' : s_kind, 'place' : s_place, 'open_dt' : s_open_dt, 'score1' : s_score1, 'score2' : s_score2, 'gross' : s_gross}
    w_bg_lst.append(item)
    #
    users = all_users()
    for bg in w_bg_lst:
        scores = score_info(bg['place'], bg['gross'])
        for score in scores:
                place = place_info(score['open_dt'])
                jp_date = etc_date.jp_date_ymd_week(score['open_dt'])
                name_nm = etc_functions.name_num2name(users, score['name_num'])
                item = {'kind' : place['kind'], 'open_dt' : place['open_dt'], 'jp_date' : jp_date, \
                    'place' : place['place'], 'name' : place['name'], 'cose1' : place['cose1'], 'cose2' : place['cose2'], \
                    'name_num' : score['name_num'], 'name_nm' : name_nm, 'score1' : score['score1'], 'score2' : score['score2'], 'gross' : score['gross']}
                ret.append(item)
    #
    return ret

def memo_lst():
    query = "SELECT * from trn_memo"
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    ret = db.execute(query).fetchall()
    db.close()
    return ret