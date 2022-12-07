import requests
import time

# login manually and get cookie
headers = {
    'cookie': "SINAGLOBAL=688599652257; UOR=www.v2ex.com,weibo.com,www.google.com; XSRF-TOKEN=DEflLXTw1jtCqHY27DHNHHld; login_sid_t=6fa0148b553c7f756633ff26a8ea909f; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=9934922632730.36.1670373906093; ULV=1670373906096:6:3:2:9934922632730.36.1670373906093:1670223758714; PC_TOKEN=aa53a272a3; WBtopGlobal_register_version=2022120709; appkey=; SCF=AhzuZhooC94L031klOPgtlsjNJ-JUIxMNzvHPK9a-WP0Bh6Mol1eisJJPW5LNPaVnftIR-0A7SpNWdGzcybXmuA.; SUB=_2A25Oi5azDeRhGeFJ7VcZ-CjEzTqIHXVt4I97rDV8PUNbmtAKLWvhkW9Nf1ozYgLVAY7G2cZehbQ5GBe18HH_fUkD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W58UamQaB0sHdkJ9jlEPkCf5JpX5KzhUgL.FoMNSo-R1hqRSoq2dJLoIEXLxK.L1hML12BLxKML1KBL1-qLxKqL1KMLBK5LxK-LBo5LB.-LxKML1hqL122t; ALF=1701911139; SSOLoginState=1670375139; WBPSESS=Dt2hbAUaXfkVprjyrAZT_B9I66FxBT9euLHIPjU1oRfVa5FkoeLEKvAC6xFaIxcmScq1LeGmNUMdDnT4FRz1YNqim80UOnn8zw5wgcRyZn3ZFhAZ5iBCnQQ75rHTwwV9PkA3UYC7Vr8LitBF37yz_zFhK3NCFGEUdAQhrrQci6iRNc-HrkuOGHkD7EFFTPnBtAlY1Srp4st7vgRTKaB4yQ==",
    'x-xsrf-token': "",
    "accept":"application/json, text/plain, */*"
}

payload = {
    "friend_uid":"7765886866",
    "page":"profile",
    "lpage":"profile"
}

def write_xsrf_from_cookie(cookie):
    c_list = cookie.split(';')
    for i in range(len(c_list)):
        if(c_list[i].find('XSRF') != -1):
            headers['x-xsrf-token'] = c_list[i].split('=')[-1]
            return 'SUCCESS'
    return 'NO XSRF TOKEN! WRONG!'

def post_follow_list():
    return requests.post("https://weibo.com/ajax/friendships/create",
                         json = payload,
                         headers = headers).text

def read_txt(file):
    with open(file,'r') as f:
        follow_list = list(eval(f.read()))
    return follow_list

if __name__ == '__main__':
    write_xsrf_from_cookie(headers['cookie'])
    follow_list = read_txt('D://IDEA//work//new//weibo-tool//follow.txt')
    for i in range(len(follow_list)):
        time.sleep(140)
        payload['friend_uid'] = str(follow_list[i])
        print(post_follow_list())
