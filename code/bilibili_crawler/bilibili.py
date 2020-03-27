import concurrent

import requests
import re
import os
import sys
import json
from lxml import etree
from pandas import DataFrame
import time
import math
import binascii
from datetime import date

# RELATIVE PATH
# from .Spider import Spider
from Spider import Spider
import concurrent.futures
from datetime import datetime

head = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}
S = Spider()


# mid: Up id, num_page: number of pages
def getmetainfo(mid, label):
	url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + str(mid)
	req = requests.get(url)
	text = req.text
	json_text = json.loads(text)
	num_page = json_text['data']['pages']
	meta_infos = [] # Meta-info (title and video id) of all videos under the Up
	tile_list = []
	aid_list = []
	for page in range(1, num_page + 1):
		url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + str(mid) + "&page=" + str(page)
		req = requests.get(url)
		text = req.text
		json_text = json.loads(text)
		for item in json_text["data"]["vlist"]:
			meta_info = {'id': item['aid'], 'title': item['title']}
			meta_infos.append(meta_info)
			tile_list.append(item['title'])
			aid_list.append(item['aid'])
	if label is 'video':
		return aid_list
	elif label is 'title':
		return tile_list
	else:
		return None


# aid: video id
def getcomment(aid):
	row_no_list = []
	no_list = []
	created_time_list = []
	converted_time_list = []
	time_interval_list = []
	device_list = []
	dislike_list = []
	floor_list = []
	like_list = []
	comment_original_list = []
	YISI_list = []
	comment_simplified_list = []
	parent_id_list = []
	root_id_list = []
	rp_count_list = []
	rp_id_list = []
	user_level_list = []
	user_id_list = []
	user_name_list = []
	video_id_list = []
	url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=1&type=1&oid={}&sort=0'.format(str(int(aid)))
	print('comment url: {0}'.format(url))
	req = requests.get(url)
	text = req.text
	json_text_list = json.loads(text)
	comment_count = json_text_list["data"]["page"]["count"]
	num_page = math.ceil(int(comment_count)/json_text_list["data"]["page"]["size"])
	print('Number of comments: {0}'.format(comment_count))
	row_no = 0
	for page in range(num_page):
		url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn={}&type=1&oid={}&sort=0'.format(str(page + 1), str(aid))
		req = requests.get(url)
		text = req.text
		json_text_list = json.loads(text)
		for item in json_text_list["data"]["replies"]:
			row_no = row_no + 1
			created_time = item["ctime"]
			converted_time = timestamp_datetime_moment(int(created_time))
			time_interval = Time_interval(timestamp_datetime_date(int(created_time)))
			dislike = 1 if item["action"] == 2 else 0
			floor = item["floor"]
			like = item["like"]
			comment_original = item["content"]["message"]
			parent_id = item["parent_str"]
			root_id = item["root_str"]
			rp_count = item["rcount"]
			rp_id = item["rpid"]
			user_level = item["member"]["level_info"]["current_level"]
			user_id = item["member"]["mid"]
			user_name = item["member"]["uname"]
			video_id = aid
			row_no_list.append(row_no)
			no_list.append(None)
			created_time_list.append(created_time)
			converted_time_list.append(converted_time)
			time_interval_list.append(time_interval)
			device_list.append(None)
			dislike_list.append(dislike)
			floor_list.append(floor)
			like_list.append(like)
			comment_original_list.append(comment_original)
			YISI_list.append(None)
			comment_simplified_list.append(None)
			parent_id_list.append(parent_id)
			root_id_list.append(root_id)
			rp_count_list.append(rp_count)
			rp_id_list.append(rp_id)
			user_level_list.append(user_level)
			user_id_list.append(user_id)
			user_name_list.append(user_name)
			video_id_list.append(video_id)
			if rp_count != 0: # Have child replies
				url_child = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn=1&type=1&oid={}&root={}'.format(str(aid), str(rp_id))
				# print('child comment url: {0}'.format(url_child))
				req_child = requests.get(url_child)
				text_child = req_child.text
				json_text_child_list = json.loads(text_child)
				comment_child_count = json_text_child_list["data"]["page"]["count"]
				num_page_child = math.ceil(int(comment_child_count)/json_text_child_list["data"]["page"]["size"])
				# print('Number of child comments: {0}'.format(comment_child_count))
				for page in range(num_page_child):
					url_child = 'https://api.bilibili.com/x/v2/reply/reply?&jsonp=jsonp&pn={}&type=1&oid={}&root={}'.format(str(page + 1), str(aid), str(rp_id))
					req_child = requests.get(url_child)
					text_child = req_child.text
					json_text_child_list = json.loads(text_child)
					for item_child in json_text_child_list["data"]["replies"]:
						row_no = row_no + 1
						created_time = item_child["ctime"]
						converted_time = timestamp_datetime_moment(int(created_time))
						time_interval = Time_interval(timestamp_datetime_date(int(created_time)))
						dislike = 1 if item_child["action"] == 2 else 0
						floor = item_child["floor"]
						like = item_child["like"]
						comment_original = item_child["content"]["message"]
						parent_id = item_child["parent_str"]
						root_id = item_child["root_str"]
						rp_count = item_child["rcount"]
						rp_id = item_child["rpid"]
						user_level = item_child["member"]["level_info"]["current_level"]
						user_id = item_child["member"]["mid"]
						user_name = item_child["member"]["uname"]
						video_id = aid
						row_no_list.append(row_no)
						no_list.append(None)
						created_time_list.append(created_time)
						converted_time_list.append(converted_time)
						time_interval_list.append(time_interval)
						device_list.append(None)
						dislike_list.append(dislike)
						floor_list.append(floor)
						like_list.append(like)
						comment_original_list.append(comment_original)
						YISI_list.append(None)
						comment_simplified_list.append(None)
						parent_id_list.append(parent_id)
						root_id_list.append(root_id)
						rp_count_list.append(rp_count)
						rp_id_list.append(rp_id)
						user_level_list.append(user_level)
						user_id_list.append(user_id)
						user_name_list.append(user_name)
						video_id_list.append(video_id)
	frame = DataFrame({'Row_no': row_no_list, 'No': no_list, 'Created_time': created_time_list, 'Converted_time': converted_time_list, 'Time_interval': time_interval_list, 'Device': device_list, 'Dislike': dislike_list, 'Floor': floor_list, \
		'Like': like_list, 'Comments_original': comment_original_list, 'YISI': YISI_list, 'Comments_simplified': comment_simplified_list, 'Parent_id': parent_id_list, 'Root_id': root_id_list, \
		'Rp_count': rp_count_list, 'Rp_id': rp_id_list, 'User_level': user_level_list, 'User_id': user_id_list, 'User_name': user_name_list, 'VideoID': video_id_list})
	frame = frame[['Row_no', 'No', 'Created_time', 'Converted_time', 'Time_interval', 'Device', 'Dislike', 'Floor', 'Like', 'Comments_original', 'YISI', 'Comments_simplified', 'Parent_id', 'Root_id', 'Rp_count', \
	'Rp_id', 'User_level', 'User_id', 'User_name', 'VideoID']]
	frame.to_excel(str(aid) + '_comment.xlsx', sheet_name='All', index = False)


# aid: video id
def getbarrage(aid,timeout):
	row_no_list = []
	no_list = []
	showing_time_list = []
	mode_list = []
	font_size_list = []
	font_color_list = []
	created_time_list = []
	converted_time_list = []
	time_interval_list = []
	danmaku_pool_list = []
	user_id_encrypt_list = []
	user_id_crack_list = []
	row_id_list = []
	barrage_original_list = []
	barrage_simplified_list = []
	video_id_list = []
	url = 'http://www.bilibili.com/video/av{}'.format(str(aid))
	# print('url: {0}'.format(url))
	html = requests.get(url, headers = head)
	cids = re.findall(r'cid=(\d+)&aid', html.text)[0]
	barrage_url = 'https://comment.bilibili.com/{}.xml'.format(cids)
	print('barrage url: {0}'.format(barrage_url))
	barrage_text = requests.get(barrage_url, timeout=timeout, headers = head)
	barrage_selector = etree.HTML(barrage_text.content)
	barrage_content = barrage_selector.xpath('//i')
	row_no = 0
	for barrage in barrage_content:
		barrages = barrage.xpath('//d/text()')
		times = barrage.xpath('//d/@p')
		for content in zip(barrages, times):
			row_no = row_no + 1
			print(content[1])
			showing_time = re.split('[,]', content[1])[0]
			mode = re.split('[,]', content[1])[1]
			font_size = re.split('[,]', content[1])[2]
			font_color = re.split('[,]', content[1])[3]
			created_time = re.split('[,]', content[1])[4]
			converted_time = timestamp_datetime_moment(int(created_time))
			time_interval = Time_interval(timestamp_datetime_date(int(created_time)))
			danmaku_pool = re.split('[,]', content[1])[5]
			user_id_encrypt = re.split('[,]', content[1])[6] # <class 'str'>
			# try:
				# user_id_crack = Crack(user_id_encrypt) # <class 'int'>
			# except ValueError:
				# user_id_crack = None
				# print('Crack Error')
				# filename = str(aid) + "_log.txt"
				# with open(filename, "a", encoding = 'utf-8') as file:
					# file.write(str(len(user_id_crack_list) + 2) + '\n')
				# file.close()
			row_id = re.split('[,]', content[1])[7]
			video_id = aid
			row_no_list.append(row_no)
			no_list.append(None)
			showing_time_list.append(showing_time)
			mode_list.append(mode)
			font_size_list.append(font_size)
			font_color_list.append(font_color)
			created_time_list.append(created_time)
			converted_time_list.append(converted_time)
			time_interval_list.append(time_interval)
			danmaku_pool_list.append(danmaku_pool)
			user_id_encrypt_list.append(user_id_encrypt)
			# user_id_crack_list.append(user_id_crack)
			row_id_list.append(row_id)
			barrage_original_list.append(content[0])
			barrage_simplified_list.append(None)
			video_id_list.append(video_id)
	frame = DataFrame({'Row_no': row_no_list, 'No': no_list, 'Showing_time': showing_time_list, 'Mode': mode_list, 'Font_size': font_size_list, 'Font_color': font_color_list, 'Created_time': created_time_list, \
		'Converted_time': converted_time_list, 'Time_interval': time_interval_list, 'Danmaku_pool': danmaku_pool_list, 'RowID': row_id_list, 'user_id_encrypt': user_id_encrypt_list,\
		'Barrages_original': barrage_original_list, 'Barrages_simplified': barrage_simplified_list, 'VideoID': video_id_list})
	frame = frame[['Row_no', 'No', 'Showing_time', 'Mode', 'Font_size', 'Font_color', 'Created_time', 'Converted_time', 'Time_interval', 'Danmaku_pool', 'RowID', 'user_id_encrypt', 'Barrages_original', 'Barrages_simplified', 'VideoID']]
	os.makedirs(f"../../data/{aid}",exist_ok=True)

	print(os.getcwd())
	now=datetime.now()
	# format of the file name
	filename=now.strftime("%m_%d_%H_%M_%S")
	print(filename)
	frame.to_csv(f'../../data/{aid}/{filename}_barrage.csv', index=False)
	# frame.to_csv(f'../../data/{aid}/ + {filename}_barrage.csv',index = False)
	return frame


def timestamp_datetime_moment(value):
	format = '%Y-%m-%d %H:%M:%S'
	value = time.localtime(value)
	dt = time.strftime(format, value)
	return dt


def timestamp_datetime_date(value):
	format = '%Y-%m-%d'
	value = time.localtime(value)
	dt = time.strftime(format, value)
	return dt


def Time_interval(time):
	first_date = date(2018, 5, 24)
	current_date = date(int(time.split('-')[0]), int(time.split('-')[1]), int(time.split('-')[2]))
	diff_date = current_date - first_date
	return diff_date.days


def Crack(user_id_encrypt):
	url = 'http://biliquery.typcn.com/api/user/hash/' + user_id_encrypt
	text = requests.get(url).text
	json_text_list = json.loads(text)
	user_id_crack = json_text_list['data'][0]['id']
	return user_id_crack


def Get_userinfo(user_id):
	userInfo = S.getUser(str(user_id))
	print('user_id: {0}'.format(userInfo['uid']))
	print('nick name: {0}'.format(userInfo['nickName']))
	print('sex: {0}'.format(userInfo['sex']))
	print('birthday: {0}'.format(userInfo['birthday']))
	print('level: {0}'.format(userInfo['level']['current_level']))
	print('Vip: {0}'.format(userInfo['isVip']))
	print('regTime: {0}'.format(userInfo['regTime']))
	print('number of fans: {0}'.format(userInfo['follower']))
	print('number of followings: {0}'.format(userInfo['following']))
	print('followings: {0}'.format(userInfo['atts']))
	print('submitVideos: {0}'.format(userInfo['submitVideos']))
	print('videoViewCount: {0}'.format(userInfo['videoViewCount']))
	print('articles: {0}'.format(userInfo['articles']))
	print('articleViewCount: {0}'.format(userInfo['articleViewCount']))
	print('bangumis: {0}'.format(userInfo['bangumis']))

# if __name__ == "__main__":
	'''
	# Get aid of all videos
	aid_list = getmetainfo(290526283, 'video') 
	print('Number of videos: {0}'.format(len(aid_list)))

	# Get comments and barrages of all videos
	for aid in aid_list:
		if os.path.exists(str(aid) + '_comment.xlsx') and os.path.exists(str(aid) + '_barrage.xlsx'):
			print(aid, 'already exists')
			continue
		print('##########################################')
		print('Downloading comments of video {0} ......'.format(aid))
		getcomment(aid)
		print('Downloading barrages of video {0} ......'.format(aid))
		getbarrage(aid)
	'''
	# getcomment(36214080)
	# getbarrage(36214080)
	# Get_userinfo(12953806)
	# getbarrage(83530891) # 原神
	# getbarrage(87976912) #大佬甜
	# getbarrage(87687323) # Jstar
	# getbarrage(88061096) # 巫师财经 疫情经济
	# getcomment(83530891)
	# getbarrage(91188408)
	# getbarrage(91688086) #基德
av_no = [
	90534559,
	91101531,
	91188408,
	90748352,
	90976388,
	85533470,
    87976912,
    86216616
]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
	# start the load operations and mark each future with its URL
	future_to_url = {executor.submit(getbarrage, av, 20): av for av in av_no}
	for future in concurrent.futures.as_completed(future_to_url):
		url = future_to_url[future]
		try:
			data = future.result()
		except Exception as exc:
			print('%r generated an  exception: %s' % (url, exc))
		# else:
		# 	print('%r page is %d bytes' % (url, len(data)))
# getbarrage(90534559)  # 2020年初电脑配件和配置单推荐






