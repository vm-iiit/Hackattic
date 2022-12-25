from pyzbar.pyzbar import decode
from PIL import Image
import requests
import sys
import json

access_token="access_token="  #Insert your access code here
hackattic_challenges_url="https://hackattic.com/challenges/"
problem_name="reading_qr/"

problem_url = hackattic_challenges_url+problem_name+"problem?"+access_token
submission_url = hackattic_challenges_url+problem_name+"solve?"+access_token

def get_problem_json(key, problem_url):
	problem_object = requests.get(problem_url)
	problem_json = problem_object.json()
	return problem_json[key]

def solve(key_having_problem_object):
	generic_problem_obj = get_problem_json(key_having_problem_object, problem_url)
	solution = solve_particular_problem(generic_problem_obj)
	submit_ans(solution)

def submit_ans(answer):
	print("sending "+answer+" as the answer")
	ans_dict = { "code" : answer }
	response = requests.post(submission_url, json.dumps(ans_dict))
	print("submission response code "+str(response.status_code))
	print("submission resply - "+str(response.text))

def solve_particular_problem(image_url):
	response = requests.get(image_url)
	# print("response object")
	# print(response.status_code)
	# print(response.content)
	# print("-*-*-*-*-*-*-*-")
	# print(response.text)
	if response.status_code == 200:
		fp = open('QR_code.png', 'wb')
		fp.write(response.content)
		fp.close()
	else:
		sys.exit("non 200 status code - "+str(response.status_code))

	decodeQR = decode(Image.open('QR_code.png'))
	print("decoded QR")
	print(decodeQR)
	code = decodeQR[0].data.decode('ascii')
	print("returning ans "+code)
	return code

solve("image_url")
