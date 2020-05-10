import json
import sys
import os
import time
from collections import defaultdict

def wait_key():
	result = None
	if os.name == 'nt':
		import msvcrt
		result = msvcrt.getch()
	else:
		import termios
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		try:
			result = sys.stdin.read(1)
		except IOError:
			pass
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	return result

with open('./JEOPARDY_QUESTIONS1.json') as f:
	  data = json.load(f)

values = ["$200", "$400", "$600", "$800", "$1000"]

questions = defaultdict(list)
scores = defaultdict(list)
scores['n'] = 0
scores['s'] = 0

for entry in data[800:]:
	value = entry["value"]
	if len(questions[value]) < 5 and value  in values:
		questions[value].append(entry)

print('press a key to begin')
wait_key()

for dollars in questions.values():
	for question in dollars:
		print('Category: ' + question["category"])
		print(question["question"])
		time.sleep(1)
		for i in range(0,4):
			print('-', end="", flush=True)
			time.sleep(1)
		print('FUCKIN BUZZ YOU NERDS')
		buzzer_timer = time.perf_counter()
		buzz = wait_key()
		if buzz == 'z':
			msg = 'Sierra answers'
			answerer = 's'
		elif buzz == 'l':
			msg = 'Niko answers'
			answerer = 'n'
		else:
			msg = 0
		if time.perf_counter() < buzzer_timer + 5:
			print(msg)
			time.sleep(7)
			print('time\'s up')
			print('the answer was ' + question['answer'])
			print('did you get it?')
			success = wait_key()
			if success == 'y':
				scores[answerer] += int(question["value"][1:])
		else:
			print('nobody got it in time')
			print('the answer was ' + question['answer'])
		print('Nikolai: $' + str(scores['n']))
		print('Sierra: $' + str(scores['s']))
		print('\n\n\n')
		wait_key()


print('final scores!')
print('Nikolai: $' + str(scores['n']))
print('Sierra: $' + str(scores['s']))
