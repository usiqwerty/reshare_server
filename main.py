from flask import Flask, request
from solution import generate_solution
from syncshare_api import get_syncshare_solution
from cached_requests import load, save

load()
app = Flask(__name__)


@app.route("/api/get_solution")
def api_get_solution():
	args = list(request.args.items())
	# [('host', 'elearn.urfu.ru'), ('courseId', '7072'), ('quizId', '200118'), ('attemptId', '968122'), ('moodleId', '75021'), ('questionId', '3025539'), ('questionType', 'multichoice')]
	ar = {}
	for k, v in args:
		ar[k] = v
	# print(args)
	ss_sol = get_syncshare_solution(ar)
	return generate_solution(ss_sol)


@app.route("/save")
def save_db():
	return save()


app.run("127.0.0.1", 8000)  # , ssl_context='adhoc'
