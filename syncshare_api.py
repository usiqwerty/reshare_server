from cached_requests import cached_get, load
from json import loads

def get_syncshare_solution(args):
	r = cached_get(args)
	print(f"{r=}")
	return loads(r)


if __name__ == "__main__":
	aaa = [('host', 'elearn.urfu.ru'), ('courseId', '7072'), ('quizId', '200118'), ('attemptId', '968122'),
		   ('moodleId', '75021'), ('questionId', '3025539'), ('questionType', 'multichoice')]
	load()
	ar = {}
	for k, v in aaa:
		ar[k] = v
	print(get_syncshare_solution(ar))
