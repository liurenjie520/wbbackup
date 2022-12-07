import requests
import json

# login manually and get cookie
headers = {
    'cookie': "SINAGLOBAL=68859984.1666950652257; UOR=www.v2ex.com,weibo.com,cn.bing.com; ULV=1668131274309:2:1:1:7643010017930.01.1668131274300:1666950652271; XSRF-TOKEN=f1s11rf9yc6Dm5q2HjTrKE_y; ALF=1701308650; SSOLoginState=1669775459; SUB=_2A25OgrAzDeRhGeFL6lsS8SrIyzuIHXVtjNB7rDV8PUJbkNAKLUHnkW1NQktl1Wt4gFE_iI4jND5WbXID1gTFB7sE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W58NqxCVfxqd_328SkjezuL5NHD95QNSK24e02XSh5NWs4Dqcj_i--fi-i8iKnRi--fi-2XiKLWi--ciK.Ni-27i--fi-z7i-i8i--NiKnciKyW; WBPSESS=6OY2iffQpK-MDjkFBVewqOnDOtuw7gMD0OYZr16Qc5mnjrUoXoaZw5dBTPjixpW1pv0yXxGH_IhNX9f1u6XE0OESKjRZCWM2ZiG1Ql1w2IfP33CTAwImFsYZ6PkxO9t_Q94gSm0vtOtgm9YZgv6Weg=="
}

def get_follow_pages():
    content = requests.get("https://weibo.com/ajax/profile/followContent?sortType=all",
                           headers=headers).text
    content_json = json.loads(content)
    total_follow = content_json['data']['total_number']
    return int(int(total_follow) / 50) + 1

def get_follow_list(pages):
    content = requests.get("https://weibo.com/ajax/profile/followContent?page=" + str(pages) + "&next_cursor=50",
                           headers = headers).text
    content_json = json.loads(content)
    return content_json

def write_txt(content):
    with open('follow.txt','w') as file:
        file.write(str(content))
    return 1


if __name__ == '__main__':
    total_pages = get_follow_pages()
    follow_id_list = []
    for i in range(1,total_pages+1):
        page_data = get_follow_list(i)
        users_number = len(page_data['data']['follows']['users'])
        for j in range(0,users_number):
            follow_id_list.append(page_data['data']['follows']['users'][j]['id'])
    write_txt(follow_id_list)

