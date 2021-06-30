import json
import re


def read_cookies():
	try:
		with open('cookies.json', 'r', encoding='utf-8') as f:
			return json.load(f)
	except: return {}

def write_cookies(cookies):
	json.dump(cookies, open('cookies.json', 'w', encoding='utf-8'))

def update_cookies(cookies):
	if cookies != None and type(cookies) == list and cookies != []:
		raw_cookies = str(cookies[0], 'utf-8')
		matched = re.findall('chii_sid=[^;]*;', raw_cookies)
		if matched != []:
			new_cookies = read_cookies()
			new_cookies['chii_sid'] = matched[0][9:-1]
			write_cookies(new_cookies)
