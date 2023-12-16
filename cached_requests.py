import sqlite3
import json
import requests

fn_cache = "cache.json"
fn_stat = "stat.json"
cache = {}
stat = {}
connection: sqlite3.Connection
cursor: sqlite3.Cursor

fn_db = 'my_database.db'
def gen_key(host, quizId, questionId):
	host_acr = ''.join(map(lambda x: x[0], host.split('.')))
	return f"{host_acr}-{quizId}-{questionId}"

def load():
	global connection, cursor
	connection = sqlite3.connect(fn_db, check_same_thread=False)
	cursor = connection.cursor()


def save():
	connection.close()
#[{'anchor': ['А. И. Покрышкин'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 3800, 'label': 'true', 'data': {'checked': True}}, {'correctness': 0, 'count': 207, 'label': 'false', 'data': {'checked': False}}]}, {'anchor': ['G. K. Zhukov'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 1, 'label': 'true', 'data': {'checked': True}}]}, {'anchor': ['Н. Ф. Гастелло'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'false', 'data': {'checked': False}}, {'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 3816, 'label': 'false', 'data': {'checked': False}}, {'correctness': 0, 'count': 84, 'label': 'true', 'data': {'checked': True}}]}, {'anchor': ['И. Н. Кожедуб'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 3774, 'label': 'true', 'data': {'checked': True}}, {'correctness': 0, 'count': 231, 'label': 'false', 'data': {'checked': False}}]}, {'anchor': ['Г. К. Жуков'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 3781, 'label': 'true', 'data': {'checked': True}}, {'correctness': 0, 'count': 223, 'label': 'false', 'data': {'checked': False}}]}, {'anchor': ['N. F. Gastello'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'false', 'data': {'checked': False}}], 'submissions': [{'correctness': -1, 'count': 1, 'label': 'false', 'data': {'checked': False}}]}, {'anchor': ['I. N. Kozhedub'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 1, 'label': 'true', 'data': {'checked': True}}]}, {'anchor': ['A. I. Pokryshkin'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'true', 'data': {'checked': True}}], 'submissions': [{'correctness': 2, 'count': 1, 'label': 'true', 'data': {'checked': True}}]}]


def save_to_cache(key, ss_solution):
	ss_solution=ss_solution.replace("\'", "\"")
	ss_solution=ss_solution.replace("True", "true")
	ss_solution = ss_solution.replace("False", "false")
	req=f"INSERT INTO tasks VALUES ('{key}', '{ss_solution}');"
	print("req:", req)
	cursor.execute(req)
	cursor.execute("COMMIT;");

def get_from_cache(key):
	a = cursor.execute(f"SELECT solution FROM tasks WHERE task_key = '{key}';")
	for r in a:
		return str(r[0])


def present_in_cache(key):
	a = get_from_cache(key)
	return bool(a)


def stat_add(ss: int, rs: int):
	# global stat
	# stat["ss-req-count"] += ss
	# stat["rs-req-count"] += rs
	pass


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

	if questionType == "unspecified":
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

	key = gen_key(host, quizId, questionId)
	if not present_in_cache(key):
		print(url)
		stat_add(1, 0)
		ss_solution = str(requests.get(url).json())
		print(ss_solution)
		save_to_cache(key, ss_solution)

	else:
		stat_add(0, 1)
	return get_from_cache(key)


if __name__ == "__main__":
	conn = sqlite3.connect(fn_db)
	cur = conn.cursor()
	for r in cur.execute("select * from tasks;"): print(r)
	cur.execute("insert into tasks values ('a', 'b');")
	cur.execute("commit;")
	#cmd = input("SQL: ")
	#while cmd != "exit":
	#	ans = cur.execute(cmd)
	#	for row in ans: print(row)
	#	cmd = input("SQL: ")
	conn.close()