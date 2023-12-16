from cached_requests import cached_get


def get_syncshare_solution(args):
	r_json = cached_get(args)
	return r_json


if __name__ == "__main__":
	aaa = [('host', 'elearn.urfu.ru'), ('courseId', '7072'), ('quizId', '200118'), ('attemptId', '968122'),
		   ('moodleId', '75021'), ('questionId', '3025539'), ('questionType', 'multichoice')]
	ar = {}
	for k, v in aaa:
		ar[k] = v
	print(get_syncshare_solution(ar))
