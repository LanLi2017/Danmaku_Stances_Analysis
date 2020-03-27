import json
import time
import requests
import math


class Spider(object):
    PROP_KEY_LIST = [
        'uid',
        'nickName',
        'sex',
        'birthday',
        'level',
        'isVip',
        'regTime',
        'follower',
        'following',
        'atts',
        'submitVideos',
        'videoViewCount',
        'articles',
        'articleViewCount'
        'bangumis',
    ]

    def __init__(self):
        self.__header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': None,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

    def getUser(self, uid: str):
        '''
            uid str: The ID of User\n
            return dict: {uid, nickName, sex, birthday, level, isVip, regTime, follower, following, submitVideos, videoViewCount, articles, articleViewCount, bangumis}
        '''
        Info = self.__get_GetInfo(uid)
        stat = self.__get_stat(uid)
        submitVideos = self.__get_getSubmitVideos(uid)
        articles = self.__get_article(uid)
        upstat = self.__get_upstat(uid)
        bangumis = self.__get_getList(uid)
        atts = self.__get_attList(uid)

        userInfo = {
            'uid': uid,
            'nickName': Info['name'] if Info is not None else None,
            'sex': Info['sex'] if Info is not None else None,
            'birthday': Info['birthday'] if Info is not None else None,
            'level': Info['level_info'] if Info is not None else None,
            'isVip': Info['vip']['vipStatus'] if Info is not None else None,
            'regTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Info['regtime'])) if Info is not None else None,
            'follower': stat['follower'],
            'following': stat['following'],
            'atts': atts,
            'submitVideos': submitVideos,
            'videoViewCount': upstat['archive']['view'] if upstat is not None else None,
            'articles': articles,
            'articleViewCount': upstat['article']['view'] if upstat is not None else None,
            'bangumis': bangumis,
        }
        return userInfo

    # Get nickname, sex, birthday, level_info, vip_status and regtime
    def __get_GetInfo(self, uid: str):
        header = self.__header
        URL = 'https://space.bilibili.com/ajax/member/GetInfo'
        data = {
            'mid': '%s' % uid,
        }
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.post(URL, data=data, headers=header).text
            r = json.loads(res)
            r = r['data']
            if not 'birthday' in r.keys():
                r['birthday'] = None
            if not 'regtime' in r.keys():
                r['regtime'] = None
        except:
            r = None
        return r

    # Get number of followers and number of followings
    def __get_stat(self, uid: str):
        header = self.__header
        URL = 'https://api.bilibili.com/x/relation/stat?vmid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    def __get_upstat(self, uid: str):
        header = self.__header
        URL = 'https://api.bilibili.com/x/space/upstat?mid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    # Get article list
    def __get_article(self, uid: str):
        header = self.__header
        URL = 'https://api.bilibili.com/x/space/article?mid=%s&pn=1' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
            content_list = []
            for item in r["articles"]:
                content_list.append(item['title'] + ":" + item['summary'])
        except:
            r = None
            content_list = []
        return content_list

    # Get submitted videos
    def __get_getSubmitVideos(self, uid: str):
        header = self.__header
        URL = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
            num_page = r['pages']
            title_list = []
            for page in range(1, num_page + 1):
                url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + str(uid) + "&page=" + str(page)
                req = requests.get(url)
                text = req.text
                json_text = json.loads(text)
                for item in json_text["data"]["vlist"]:
                    title_list.append(item['title'])
        except:
            r = None
            title_list = []
        return title_list

    # Get bangumis
    def __get_getList(self, uid: str):
        header = self.__header
        URL = 'https://space.bilibili.com/ajax/Bangumi/getList?mid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
            num_page = r['pages']
            title_list = []
            for page in range(1, num_page + 1):
                url = "https://space.bilibili.com/ajax/Bangumi/getList?mid=" + str(uid) + "&page=" + str(page)
                req = requests.get(url)
                text = req.text
                json_text = json.loads(text)
                for item in json_text["data"]["result"]:
                    title_list.append(item['title'])
        except:
            r = None
            title_list = []
        return title_list

    # Get what they are followings
    def __get_attList(self, uid: str):
        header = self.__header
        URL = "https://api.bilibili.com/x/relation/followings?vmid=" + uid + "&pn=0"
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
            num_page = math.ceil(int(r['total'])/50)
            username_list = []
            for page in range(1, num_page + 1):
                url = "https://api.bilibili.com/x/relation/followings?vmid=" + str(uid) + "&pn=" + str(page)
                req = requests.get(url)
                text = req.text
                json_text = json.loads(text)['data']
                for i in range(len(json_text['list'])):
                    username_list.append(json_text['list'][i]['uname'])
        except:
            r = None
            username_list = []
        return username_list


if __name__ == '__main__':
    S = Spider()
    userInfo = S.getUser('392727281')
    print(userInfo)
 