import pygame
import math

ENUM_STATE_MENU = 0
ENUM_STATE_GAME = 1

pygame.init()

COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_BOARD = (240, 220, 165)
COLOR_GRAY = (180, 180, 180)
COLOR_WHITE = (255, 255, 255)
COLOR_UNSELECTABLE_BG = (255, 175, 175)

cell_count = 15
cell_size = 30

radius = 13
diff = 7

def _GetPygamePos(pos):
    i, j = pos
    return (board_start_w + i * cell_size, board_start_h + j * cell_size)

def _DrawBlackStone(pos):
    pygame.draw.circle(screen, COLOR_BLACK, _GetPygamePos(pos), radius, width = 0)
    return

def _DrawWhiteStone(pos):
    pygame.draw.circle(screen, COLOR_WHITE, _GetPygamePos(pos), radius, width = 0)
    pygame.draw.circle(screen, COLOR_BLACK, _GetPygamePos(pos), radius, width = 1)
    return

def _DrawUnseletable(pos):
    pg_pos = _GetPygamePos(pos)
    pygame.draw.circle(screen, COLOR_UNSELECTABLE_BG, pg_pos, radius, width = 0)
    pygame.draw.circle(screen, COLOR_RED, pg_pos, radius, width = 2)

    pg_pos_w, pg_pos_h = pg_pos
    pygame.draw.line(screen, COLOR_RED, (pg_pos_w - diff, pg_pos_h - diff), (pg_pos_w + diff, pg_pos_h + diff), width = 3)
    pygame.draw.line(screen, COLOR_RED, (pg_pos_w + diff, pg_pos_h - diff), (pg_pos_w - diff, pg_pos_h + diff), width = 3)
    return

board_start_w = 40
board_start_h = 40
board_end_w = board_start_w + cell_size * cell_count
board_end_h = board_start_h + cell_size * cell_count

size = [530, 530]
screen = pygame.display.set_mode(size)

title_name = "Five In A Row"
pygame.display.set_caption(title_name)

done = False
clock = pygame.time.Clock()

state = ENUM_STATE_MENU

while not done:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if state == ENUM_STATE_MENU:
        screen.fill(COLOR_BOARD)

        fontObj = pygame.font.Font(None, 32)
        textRect = pygame.draw.rect(screen, COLOR_GRAY, (200, 200, 125, 25), width=0)
        text = fontObj.render('Hello world!', True, COLOR_BLACK)
        screen.blit(text, textRect)

        pygame.display.flip()
    
    elif state == ENUM_STATE_GAME:
        screen.fill(COLOR_BOARD)

        for i in range(cell_count + 1):
            pygame.draw.line(screen, COLOR_BLACK, (board_start_w + cell_size * i , board_start_h), (board_start_w + cell_size * i , board_end_h), width = 2)
            pygame.draw.line(screen, COLOR_BLACK, (board_start_w, board_start_h + cell_size * i), (board_end_w, board_start_h + cell_size * i), width = 2)

        # Basic Test
        _DrawBlackStone((0, 0))
        _DrawWhiteStone((0, 1))
        _DrawWhiteStone((0, 2))

        # 33 Rule Test
        _DrawBlackStone((5, 5))
        _DrawBlackStone((5, 6))
        _DrawBlackStone((6, 7))
        _DrawBlackStone((7, 7))
        _DrawUnseletable((5, 7))
        
        pygame.display.flip()

