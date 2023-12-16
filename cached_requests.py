import json

import requests

fn_cache = "cache.json"
fn_stat = "stat.json"
cache = {}
stat = {}


def load():
	global cache, stat
	try:
		with open(fn_cache) as f:
			print(f"Reading {fn_cache}")
			cache = json.load(f)
			print(len(cache.keys()), "entries read")
	except FileNotFoundError:
		cache = {}
	try:
		with open(fn_stat) as f:
			print(f"Reading {fn_stat}")
			stat = json.load(f)
	except FileNotFoundError:
		stat = {"ss-req-count": 0, "rs-req-count": 0}
	print(stat)


def save():
	with open(fn_cache, "w") as f:
		print(f"Saving to {fn_cache}")
		json.dump(cache, f)
		print("Done")
	with open(fn_stat, "w") as f:
		print(f"Saving to {fn_stat}")
		json.dump(stat, f)
		print("Done")
	return f"Saved {len(cache.keys())} entries"


def save_to_cache(key, ss_solution):
	global cache
	cache[key] = ss_solution


def get_from_cache(key):
	return cache[key]


def present_in_cache(key):
	return key in cache
def stat_add(ss:int, rs:int):
	global stat
	stat["ss-req-count"] += ss
	stat["rs-req-count"] += rs

def cached_get(args):
	global cache
	courseId = args['courseId']  # '7072'
	quizId = args["quizId"]  # '200118'
	attemptId = args["attemptId"]  # '968122'
	moodleId = args["moodleId"]  # '75021'
	questionId = args["questionId"]  # '3025537'
	questionType = args["questionType"]  # "multichoice"
	client = "1.1.6"
	host = args["host"]  # "elearn.urfu.ru"

	if questionType=="unspecified":
		return "Unspecified question type", 400

	api_base_url = "https://syncshare.naloaty.me/api/v2"
	url = (f"{api_base_url}/quiz/solution?"
		   f"{host=!s}&"
		   f"{courseId=!s}&"
		   f"{quizId=!s}&"
		   f"{attemptId=!s}&"
		   f"{moodleId=!s}&"
		   f"{questionId=!s}&"
		   f"{questionType=!s}&"
		   f"{client=!s}")

	key = f"{quizId}-{questionId}"
	if not present_in_cache(key):
		print(url)
		stat_add(1,0)
		ss_solution = requests.get(url).json()
		save_to_cache(key, ss_solution)

	else:
		stat_add(0, 1)
	return get_from_cache(key)
