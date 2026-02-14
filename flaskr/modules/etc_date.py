import datetime

def jp_date_md(ymd):
	ret = ymd[4:6] + "月" + ymd[6:8] + "日"
	return ret

def jp_date_ymd(ymd):
	ret = ymd[0:4] + "年" + ymd[4:6] + "月" + ymd[6:8] + "日"
	return ret

def jp_date_md_week(ymd):
	y = ["月","火","水","木","金","土","日"]
	w = datetime.datetime.strptime(ymd, "%Y%m%d")
	i = w.weekday()
	ret = jp_date_md(ymd) + "(" + y[i] + ")"
	return ret

def jp_date_ymd_week(ymd):
	y = ["月","火","水","木","金","土","日"]
	w = datetime.datetime.strptime(ymd, "%Y%m%d")
	i = w.weekday()
	ret = jp_date_ymd(ymd) + "(" + y[i] + ")"
	return ret

def this_year():
    today = datetime.date.today()
    return today.year

def now_dt():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, "JST")
    now = datetime.datetime.now(JST)
    ret = now.strftime("%Y%m%d%H%M%S")
    return ret

def today():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, "JST")
    now = datetime.datetime.now(JST)
    ret = now.strftime("%Y%m%d")
    return ret

def hdcp_start_ym(ymd, offset_m):
    iy = int(ymd[0:4]) - 1
    im = int(ymd[4:6]) + offset_m
    if im == 13:
        im = 1
        iy = iy + 1
    sy = str(iy)
    sm = str(im)
    ret = sy + sm.rjust(2, '0')
    return ret

def hdcp_start_ymd(ymd, offset_m):
	ymd = hdcp_start_ym(ymd, offset_m) + '01'
	return ret


