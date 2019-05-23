import pygame
import time
import string

#piece codes
#0 - black king
#1 - black queen
#2 - black rook
#3 - black bishop
#4 - black knight
#5 - black pawn
#6 - white king
#7 - white queen
#8 - white rook
#9 - white bishop
#10 - white knight
#11 - white pawn

pygame.init()

# INITIALISING THE GAME CONSTANTS
display_width = 750
display_height = 700
board_height = 560
board_width = 560
cell_height = 70
cell_width = 70
boardX = 40
boardY = 40
black = (0, 0, 0)
green = (13, 99, 5)
white = (226, 195, 147)
red = (204 , 28, 12)
bg = (255, 255, 255)
d = 15	#Distance between board and board label
l = list(string.ascii_uppercase[0:8]) 	#Uppercase alphabet list for board labelling

chess_pieces = ['blackKing.png','blackQueen.png','blackRook.png','blackBishop.png','blackKnight.png','blackPawn.png','whiteKing.png','whiteQueen.png','whiteRook.png','whiteBishop.png','whiteKnight.png','whitePawn.png']
piece_img =[]
for piece in chess_pieces:
	p = pygame.image.load('images/'+piece)
	p = pygame.transform.scale(p,(cell_width, cell_height))
	piece_img.append(p)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("CHESS AI")

#FUNCTION WHICH DRAWS THE CHESSBOARD ON THE DISPLAY
def draw_board():
	t = 1
	for y in range(boardY, board_height, cell_height):
		for x in range(boardX, board_width, cell_width):
			if t == -1:
				pygame.draw.rect(gameDisplay, green, [x, y, cell_width, cell_height])
			else:
				pygame.draw.rect(gameDisplay, white, [x, y, cell_width, cell_height])

			t*=-1
		t*=-1	

	font = pygame.font.Font('freesansbold.ttf',15)

	#VERTICAL LABELLING
	for y in range(1, 9):
		text = font.render(str(9-y), True, black)
		textRect = text.get_rect()
		textRect.center = (boardX-d, boardY+(2*y-1)*cell_height//2) 
		gameDisplay.blit(text, textRect)

	#HORIZONTAL LABELLING
	for x in range(1, 9):
		text = font.render(l[x-1], True, black)
		textRect = text.get_rect()
		textRect.center = (boardX+(2*x-1)*cell_width//2, boardY+board_height+d) 
		gameDisplay.blit(text, textRect)

#FUNCTION WHICH MAPS THE INDEX NO OF A CELL TO ITS CORRESPONDING (TOP LEFT) SCREEN COORDINATE
def index_to_coordinate(x,y):
	pieceX = boardX + x*cell_width
	pieceY = boardY + y*cell_height
	return pieceX, pieceY

#FUNCTION WHICH CONVERTS THE SCREEN COORDINATES TO ITS CORRESPONDING INDEX NUMBER
def coordinate_to_index(pieceX,pieceY):
	x = (pieceX-boardX)//cell_width
	y = (pieceY-boardY)//cell_height
	return x,y

#FUNCTION WHICH DRAWS A CHESS PIECE ON THE BOARD
def draw_piece(piece_code, x, y):
	pieceX, pieceY = index_to_coordinate(x,y)
	gameDisplay.blit(piece_img[piece_code], (pieceX, pieceY))

#FUNCTION TO SET ALL THE CHESS PIECES ON THE BOARD
def set_pieces():
	draw_piece(0, 4, 0)
	draw_piece(1, 3, 0)
	draw_piece(2, 0, 0)
	draw_piece(2, 7, 0)
	draw_piece(3, 2, 0)
	draw_piece(3, 5, 0)
	draw_piece(4, 1, 0)
	draw_piece(4, 6, 0)
	draw_piece(6, 4, 7)
	draw_piece(7, 3, 7)
	draw_piece(8, 0, 7)
	draw_piece(8, 7, 7)
	draw_piece(9, 2, 7)
	draw_piece(9, 5, 7)
	draw_piece(10, 1, 7)
	draw_piece(10, 6, 7)
	for i in range(0,8):
		draw_piece(5, i, 1)
		draw_piece(11, i, 6)

#FUNCTION THAT HIGHLIGHTS A CELL
def highlight_cell(x, y, color):
	pieceX,pieceY = index_to_coordinate(x,y)
#	print(pieceX, pieceY)
	pygame.draw.rect(gameDisplay, red, [pieceX, pieceY, cell_width, cell_height])

#FUNCTION THAT SHOWS POSSIBLE MOVES FOR A CHESS PIECE
def show_moves(mouse):
	x,y = coordinate_to_index(mouse[0], mouse[1])
	highlight_cell(x,y,red)
	
# GAME LOOP
def game_loop():

	gameExit = False
	while not gameExit:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(bg)
		draw_board()
		set_pieces()
		mouse = pygame.mouse.get_pos()
		if (boardX < mouse[0] < boardX+board_width) and (boardY < mouse[1] < boardY+board_height):
			show_moves(mouse)
		pygame.display.update()

game_loop()
