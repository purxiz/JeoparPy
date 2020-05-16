import pyglet
import json
from enum import Enum
from collections import defaultdict

with open('./JEOPARDY_QUESTIONS1.json') as f:
	  data = json.load(f)

jeopardy_values = ["$200", "$400", "$600", "$800", "$1000"]

jeopardy_questions = {'$200': [], '$400': [], '$600': [], '$800': [], '$1000': []}
d_jeopardy_questions = {'$400': [], '$800': [], '$1200': [], '$1600': [], '$2000': []}

for entry in data:
	value = entry["value"]
	seen = 'seen' in entry.keys()
	if not seen and value in jeopardy_questions.keys() and len(jeopardy_questions[value]) < 5 and not '<a' in entry['question']:
		jeopardy_questions[value].append(entry)
		entry['seen'] = True
	elif not seen and value in d_jeopardy_questions.keys() and len(d_jeopardy_questions[value]) < 5 and not '<a' in entry['question']:
		d_jeopardy_questions[value].append(entry)
		entry['seen'] = True

with open('./JEOPARDY_QUESTIONS1.json', 'w') as f:
	json.dump(data, f)

print(jeopardy_questions)
print(d_jeopardy_questions)

window = pyglet.window.Window(fullscreen=True)

class GameStates(Enum):
	SPLASH = 0
	JEOPARDY = 1
	DOUBLE_JEOPARDY = 2
	END = 3
	CATEGORY_SPLASH = 5

buzz = False
gameState = GameStates.SPLASH
player1_score = 0
player2_score = 0
active_player = 0

class Game:
	def __init__(self):
		self.index = 0
		self.value = '$200'

	def getValue(self):
		if gameState == GameStates.JEOPARDY:
			return int(jeopardy_questions[self.value][self.index]['value'][1:])
		elif gameState == GameStates.DOUBLE_JEOPARDY:
			return int(d_jeopardy_questions[self.value][self.index]['value'][1:])
	def getCategory(self):
		if gameState == GameStates.JEOPARDY:
			return jeopardy_questions[self.value][self.index]['category']
		elif gameState == GameStates.DOUBLE_JEOPARDY:
			return d_jeopardy_questions[self.value][self.index]['category']
	def getQuestion(self):
		if gameState == GameStates.JEOPARDY:
			return jeopardy_questions[self.value][self.index]['question']
		elif gameState == GameStates.DOUBLE_JEOPARDY:
			return d_jeopardy_questions[self.value][self.index]['question']
	def getYear(self):
		if gameState == GameStates.JEOPARDY:
			return jeopardy_questions[self.value][self.index]['air_date'][0:4]
		elif gameState == GameStates.DOUBLE_JEOPARDY:
			return d_jeopardy_questions[self.value][self.index]['air_date'][0:4]
	def getAnswer(self):
		if gameState == GameStates.JEOPARDY:
			return jeopardy_questions[self.value][self.index]['answer']
		elif gameState == GameStates.DOUBLE_JEOPARDY:
			return d_jeopardy_questions[self.value][self.index]['answer']
	def nextQuestion(self):
		global gameState
		if self.index < 4:
			self.index += 1
			return
		self.index = 0
		if self.value == '$1000':
			gameState = GameStates.DOUBLE_JEOPARDY
			self.value = '$400'
			return
		if self.value == '$2000':
			gameState = GameStates.END
			return
		if gameState == GameStates.JEOPARDY:
			self.value = '$' + str(int(self.value[1:]) + 200)
		elif gameState == GameStates.DOUBLE_JEOPARDY:
			self.value = '$' + str(int(self.value[1:]) + 400)

game = Game()

print(str(game.getCategory()))


label = pyglet.text.Label('Welcome to Jeopardy~ press any key to continue...',
						font_name = 'Times new Roman',
						font_size=128,
						x=window.width/2,
						y=window.height/2,
						width=int(window.width*.8),
						anchor_x='center',
						anchor_y='center',
						multiline=True,
						align='center')

label_score1 = pyglet.text.Label('Player 1: $' + str(player1_score), x=0, y=10, font_size=48)
label_score2 = pyglet.text.Label('Player 2: $' + str(player2_score), x=window.width, y=10, anchor_x='right', font_size=48)

label_timer = pyglet.text.Label('', x=window.width/2, y=window.height, anchor_x='center', anchor_y='top', font_size=48)

label_buzzer = pyglet.text.Label('', x=window.width/2, y=window.height-96, anchor_x='center', anchor_y='top', font_size=48)

label_year = pyglet.text.Label('', x=window.width/2, y=0, anchor_x='center', anchor_y='bottom', font_size=48)

label_value = pyglet.text.Label('', x=window.width/2, y=96, anchor_x='center', anchor_y='bottom', font_size=48)

question_status = 0
counter = 0

# CONSTANTS
FPS = 60
CATEGORY_DISPLAY_TIME = 5
QUESTION_READ_TIME = 5
BUZZ_TIME = 5
QUESTION_ANSWER_TIME = 5
BUZZ_STRING = 'BUZZ BUZZ BUZZ'

# question statuses
# 0 -> new question starting
# 1 -> category being displayed
# 2 -> question being displayed for reading
# 3 -> buzzer time
# 4 -> answer time
# 5 -> display answer
# 9 -> nobody buzzed

timer1 = False
timer2 = False

def update(dt):
	label_score1.text = 'Player 1: $' + str(player1_score)

	label_score2.text = 'Player 2: $' + str(player2_score) 
	global question_status, counter, buzz, timer1, timer2, timer
	if gameState == GameStates.SPLASH:
		label.text = 'Welcome to JeoparPY~ Press Any Key to Continue...'
	elif gameState == GameStates.END:
		label.text = 'Game Over'
	else:
		if(question_status == 0):
			counter = 0
			question_status = 1
			label.text = "Category:  " + game.getCategory()
			label_year.text = "Year: " + game.getYear()
			label_value.text = "Values: $" + str(game.getValue())
			label_buzzer.text = ''
			label_timer.text = str(CATEGORY_DISPLAY_TIME)
		if question_status == 2 and not timer1:
			timer1 = True
			label_year.text = ''
			label_value.text = ''
			label.text = game.getQuestion()
			label_timer.text = str(QUESTION_READ_TIME)
		if question_status == 3 and not buzz:
			buzz = True
			label_timer.text = str(BUZZ_TIME)
			label_buzzer.text = BUZZ_STRING
		if question_status == 4 and not timer2:
			timer2 = True
			label_timer.text = str(QUESTION_ANSWER_TIME)

		if question_status == 5:
			label.text = "Answer:  " + game.getAnswer()
			label_timer.text = "press y/n"
			return

		if question_status == 9:
			label.text = "Nobody got it!   The answer was  " + game.getAnswer()
			label_buzzer.text = "press any key to continue"
			return

		# Game Counter
		counter += 1
		if counter % FPS == 0:
			if question_status == 1:
				timer = CATEGORY_DISPLAY_TIME - int(counter/FPS)
			if question_status == 2:
				timer = QUESTION_READ_TIME - int(counter/FPS)
			if question_status == 3:
				timer = BUZZ_TIME - int(counter/FPS)
			if question_status == 4:
				timer = QUESTION_ANSWER_TIME - int(counter/FPS)

			if timer > 0:
				label_timer.text = str(timer)
			else:
				if question_status == 3:
					question_status = 9
					return
				question_status += 1
				label_timer.text = ''
				counter = 0
		
@window.event
def on_draw():
	window.clear()
	label.draw()
	label_score1.draw()
	label_score2.draw()
	label_timer.draw()
	label_buzzer.draw()
	label_year.draw()
	label_value.draw()

@window.event
def on_key_press(symbol, modifiers):
	global gameState, question_status, player1_score, player2_score, buzz, active_player, counter, timer1, timer2
	if gameState == GameStates.SPLASH:
		gameState = GameStates.JEOPARDY
	elif buzz and question_status == 3:
		if symbol == pyglet.window.key.Z:
			question_status = 4
			label_buzzer.text = 'SIERRA'
			active_player = 2
			buzz = False
			counter = 0
		elif symbol == pyglet.window.key.L:
			question_status = 4
			label_buzzer.text = 'NIKOLAI'
			active_player = 1
			buzz = False
			counter = 0
	elif question_status == 5:
		if symbol == pyglet.window.key.Y:
			if active_player == 1:
				player1_score += game.getValue()
			if active_player == 2:
				player2_score += game.getValue()
		game.nextQuestion()
		question_status = 0
		timer1 = False
		timer2 = False
	elif question_status == 9:
		game.nextQuestion()
		question_status = 0
		timer1 = False
		timer2 = False
		buzz = False
	


pyglet.clock.schedule_interval(update, 1/FPS)

if __name__ == '__main__':
	pyglet.app.run()
