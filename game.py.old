import pygame
import pygame.freetype
from enum import Enum

class GameStates(Enum):
	CHOOSE_GAME = 1
	JEOPARDY = 2
	DOUBLE_JEOPARDY = 3
	FINAL_JEOPARDY = 4
	GAME_END = 5

class Game:

	def __init__(self):
		self.gameState = GameStates.CHOOSE_GAME

	def getGameState(self):
		return self.gameState

	def setGameState(self, newGameState):
		self.gameState = newGameState


class TextObject:

	def __init__(self, text):
		self.text = text

	def draw(self, x=int(screen.get_width/2), y=int(screen.get_height/2), color=(255,255,255)):
		self.rendered_text = font.render(self.text, True, color)
		self.text_rect = 

	

def main():
	pygame.init()
	pygame.display.set_caption('JeoparPy')

	screen = pygame.display.set_mode((1920, 1080))

	clock = pygame.time.Clock()

	running = True

	game = Game()

	print(game.getGameState())
	font = pygame.font.Font(None, 200)

	while running:

		# handle screen background 
		if game.getGameState() == GameStates.CHOOSE_GAME or game.getGameState() == GameStates.GAME_END: 
			screen.fill((0, 0, 0))
		else:
			screen.fill((6, 12, 233))

		# Main Game Loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				print('hi')

		h = screen.get_height()
		w = screen.get_width()

		text1 = font.render('test text', True, (255, 255, 255))

		text_rect = text1.get_rect(center=( int(w/2), int(h/2) ))
		screen.blit(text1, text_rect)

		pygame.display.update()

		clock.tick(60)

if __name__ == "__main__":
	main()
