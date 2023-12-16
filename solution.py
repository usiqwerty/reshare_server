# true_ans="славянофилы выступали против революции как способа обновления общества и государства"
# a=[{'anchor': ['славянофилы выступали против революции как способа обновления общества и государства'], 'suggestions': [{'correctness': 2, 'confidence': 0.99, 'label': 'славянофилы выступали против революции как способа обновления общества и государства', 'data': {'anchor': ['славянофилы выступали против революции как способа обновления общества и государства']}}], 'submissions': [{'correctness': 0, 'count': 68, 'label': 'славянофилы были антизападниками. Они не признавали цивилизационного значения европейской культуры', 'data': {'anchor': ['славянофилы были антизападниками. Они не признавали цивилизационного значения европейской культуры']}}, {'correctness': 2, 'count': 3851, 'label': 'славянофилы выступали против революции как способа обновления общества и государства', 'data': {'anchor': ['славянофилы выступали против революции как способа обновления общества и государства']}}, {'correctness': 0, 'count': 14, 'label': 'Россия, по мнению славянофилов, стремится быть самой сильной и богатой страной', 'data': {'anchor': ['Россия, по мнению славянофилов, стремится быть самой сильной и богатой страной']}}, {'correctness': 0, 'count': 7, 'label': 'российская цивилизация – это восточная цивилизация, для которой характерно неприятие любых западных ценностей', 'data': {'anchor': ['российская цивилизация – это восточная цивилизация, для которой характерно неприятие любых западных ценностей']}}]}]
# b=a[0]

def generate_item(syncshare_item_data):

	print(syncshare_item_data)
	if type(syncshare_item_data)==str:
		return {
			"label": syncshare_item_data,
			"data": {
			"text": syncshare_item_data}
		}

	if "anchor" in syncshare_item_data:
		true_ans = syncshare_item_data["anchor"]
	else:
		true_ans = syncshare_item_data["checked"]
	return {
		"label": true_ans,
		"data": {
			"sign": true_ans
		}
	}


def generate_suggestions(syncshare_suggestions):
	suggestions = []
	for ss_sugg in syncshare_suggestions:
		sugg = {
			"correctness": ss_sugg["correctness"],
			"confidence": ss_sugg["confidence"],
			"item": generate_item(ss_sugg["data"])
		}
		suggestions.append(sugg)
	return suggestions[:7]


def generate_submissions(syncshare_submissions):
	submissions = []
	for ss_subm in syncshare_submissions:
		subm = {
			"correctness": ss_subm["correctness"],
			"count": ss_subm["count"],
			"item": generate_item(ss_subm["data"])
		}
		submissions.append(subm)
	return submissions[:7]


def generate_solution(ss_solution):
	solutions = []
	if type(ss_solution)==dict:
		print(ss_solution)
		return
	for b in ss_solution:

		# b=ss_solution[0]
		print(b)
		if b["anchor"]:
			true_ans = b["anchor"][0]
		else:
			true_ans=""
		solution = {
			"anchor": [true_ans + ";"],
			"suggestions": generate_suggestions(b["suggestions"]),
			"submissions": generate_submissions(b["submissions"])
		}
		solutions.append(solution)
	return solutions

# def translate():
#
# print(b)
# translate()
# print(generate_solution())
