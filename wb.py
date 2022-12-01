import datetime

import requests
import csv
import time
import json


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }
    cookies = {
        "cookie": "SINAGLOBAL=6850652257; UOR=www.v2ex.com,weibo.com,cn.bing.com; ULV=1669785439405:3:2:1:4844774339362.152.1669785439401:1668131274309; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W58NqxCVfxqd_328SkjezuL5JpX5KMhUgL.FoMfeK.0eKBXehM2dJLoIEXLxK-LB.-L1hnLxK-LBKBL1-2LxKqL1KMLBK5LxK-LBo5LB.-LxKML1hqL122t; ALF=1672456887; SSOLoginState=1669864887; SCF=AhzuZhooC94L031klOPgtlsjNJ-JUIxMNzvHPK9a-WP0fMpLEpWznmUjoIg5TQIw75AgoVD3A4L-nAa5inlpeYs.; SUB=_2A25OjG3nDeRhGeFL6lsS8SrIyzuIHXVt-NgvrDV8PUNbmtAKLVn2kW9NQktl1XtOkITirX6_ZaiajtMbSzgAtRAo; XSRF-TOKEN=LzjxB-ofFZXC8cx9jCu7VLi1; WBPSESS=6OY2iffQpK-MDjkFBVewqOnDOtuw7gMD0OYZr16Qc5mnjrUoXoaZw5dBTPjixpW1zcPMNUiMgRuy7JZfALdOoEWg8nYRze5APVyJfv0_L1NVkPyyNfEczWGr755BaPpsEMtpxePBwGdQ-cRFUmZG4Q=="
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(10)  # 加上3s 的延时防止被反爬
    return response.text


def save_data(data):
    title = ['原创微博正文', '原创微博附带图片', '原创微博livephoto', '原创微博发布时间', '原创微博type',
             '原创微博source', '原创微博发布地', '转发原博正文', '转发原博附带图片', '转发原博livephoto',
             '转发原博type', '转发原博source', '转发原博链接']
    with open("data.csv", "a", encoding="utf_8_sig", newline="") as fi:
        fi = csv.writer(fi)
        fi.writerow([data[i] for i in title])


def get_json_value_by_key(self, in_json, target_key, results=[]):
    """
    根据key值读取对应的value值
    :param in_json:传入的json
    :param target_key: 目标key值
    :param results:
    :return:
    """
    if isinstance(in_json, dict):  # 如果输入数据的格式为dict
        for key in in_json.keys():  # 循环获取key
            data = in_json[key]
            self.get_json_value_by_key(data, target_key, results=results)  # 回归当前key对于的value
            if key == target_key:  # 如果当前key与目标key相同就将当前key的value添加到输出列表
                results.append(data)
    elif isinstance(in_json, list) or isinstance(in_json, tuple):  # 如果输入数据格式为list或者tuple
        for data in in_json:  # 循环当前列表
            self.get_json_value_by_key(data, target_key, results=results)  # 回归列表的当前的元素
    return results


if __name__ == '__main__':

    uid = 7519314407
    #从1开始。断了继续
    page = 322
    while 1:

        print(page)
        url = 'https://weibo.com/ajax/statuses/mymblog?uid={}&page={}&feature=0'

        url = url.format(uid, page)
        print(url)
        html = get_html(url)
        responses = json.loads(html)
        blogs = responses['data']['list']
        if len(blogs) == 0:
            break
        data = {}  # 新建个字典用来存数据
        for blog in blogs:

            data['原创微博正文'] = blog['text_raw']  # 博文正文文字数据
            tu = []
            livephoto = []

            if 'pic_infos' in blog:
                pic_infos = blog['pic_infos'] if 'pic_infos' in blog else ''
                pic_infos = json.dumps(pic_infos)
                j = json.loads(pic_infos)

                for v in j:
                    jl = j[v]
                    tmpp = jl['large']['url']
                    tu.append(tmpp)
                    if 'video' in jl:
                        video = jl['video']

                        livephoto.append(video)


                    else:
                        livephoto.append("无livephoto")

            else:
                tu.append("无图片")

            data['原创微博附带图片'] = tu
            data['原创微博livephoto'] = livephoto

            data['原创微博发布时间'] = datetime.datetime.strptime(blog['created_at'],
                                                                  '%a %b %d %X %z %Y')  # 发布时间
            if 'object_type' in blog:
                data['原创微博type'] = blog['page_info']['object_type'] if 'page_info' in blog else ''  #
            else:
                data['原创微博type']="无"

            data['原创微博source'] = blog['source'] if 'source' in blog else ''  #
            data['原创微博发布地'] = blog['region_name'] if 'region_name' in blog else ''

            # 转发：
            if 'retweeted_status' in blog:
                data['转发原博正文'] = blog['retweeted_status']['text_raw'] if 'retweeted_status' in blog else ''
                zf_tu = []
                zf_livephoto = []
                if 'pic_infos' in blog['retweeted_status']:
                    zf_pic_infos = blog['retweeted_status']['pic_infos']if 'pic_infos' in blog['retweeted_status'] else ''
                    zf_pic_infos=json.dumps(zf_pic_infos)
                    zf_j=json.loads(zf_pic_infos)
                    for v in zf_j:
                        zf_jl=zf_j[v]
                        tmppp=zf_jl['large']['url']
                        zf_tu.append(tmppp)
                        if 'video' in zf_jl:
                            video=zf_jl['video']
                            zf_livephoto.append(video)
                        else:
                            zf_livephoto.append("无转发livephoto")
                else:
                    zf_tu.append("无转发图片")
                data['转发原博附带图片']=zf_tu
                data['转发原博livephoto']=zf_livephoto
                if 'object_type' in blog['retweeted_status']:
                    data['转发原博type'] = blog['retweeted_status']['page_info']['object_type'] if 'page_info' in blog['retweeted_status'] else ''  #
                else:
                    data['转发原博type'] ="无"


                data['转发原博source'] = blog['retweeted_status']['source'] if 'source' in blog['retweeted_status'] else ''

                data['转发原博链接'] = "https://m.weibo.cn/status/" +str(blog['retweeted_status']['id']) if 'id' in blog['retweeted_status'] else ''
            else:
                data['转发原博正文']="无"
                data['转发原博附带图片']="无"
                data['转发原博livephoto']="无"
                data['转发原博type'] = "无"
                data['转发原博source'] = "无"

                data['转发原博链接'] = "无"



            save_data(data)
        page += 1
