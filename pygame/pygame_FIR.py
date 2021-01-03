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

def _IsButtonCollision(pos):
    for i in range(3):
        w, h = pos
        cur_btn_bg_start_w = btn_bg_start_w
        cur_btn_bg_start_h = btn_bg_start_h + (3 / 2 * btn_bg_h * i)
        if (cur_btn_bg_start_w <= w and w <= cur_btn_bg_start_w + btn_bg_w) and (cur_btn_bg_start_h <= h and h <= cur_btn_bg_start_h + btn_bg_h):
            return i
    return -1

board_start_w = 40
board_start_h = 40
board_end_w = board_start_w + cell_size * cell_count
board_end_h = board_start_h + cell_size * cell_count

btn_bg_w = 280
btn_bg_h = 50
btn_bg_start_w = 125
btn_bg_start_h = 200

size = [530, 530]
screen = pygame.display.set_mode(size)

title_name = "Five In A Row"
pygame.display.set_caption(title_name)

done = False
clock = pygame.time.Clock()

state = ENUM_STATE_MENU

is_first_draw_menu = True

while not done:
    clock.tick(10)

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         done = True
    #     if event.type == pygame.MOUSEMOTION:
    #             print('Event1 Triggered!')
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #             print('Event2 Triggered!')

    if state == ENUM_STATE_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEMOTION:
                buttonHoverIndex = _IsButtonCollision(event.pos)
                # print(buttonHoverIndex)
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonClickIndex = _IsButtonCollision(event.pos)
                print(buttonClickIndex)

        if is_first_draw_menu == True:
            is_first_draw_menu = False
            buttonHoverIndex = -1
            buttonClickIndex = -1

            screen.fill(COLOR_BOARD)

            fontObj = pygame.font.Font(None, 60)
            textObj = fontObj.render('Five in a Row', True, COLOR_BLACK)
            screen.blit(textObj, (135, 70))


            fontObj = pygame.font.Font(None, 30)
            strList = ['Human vs Human', 'Human vs AI(Rule-Base)', 'Human vs AI(RL)']
            buttonPosList = []
            for i in range(3):
                cur_btn_bg_start_w = btn_bg_start_w
                cur_btn_bg_start_h = btn_bg_start_h + (3 / 2 * btn_bg_h * i)

                textBG = pygame.draw.rect(screen, COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, btn_bg_w, btn_bg_h), width=0)
                
                background_center_w = cur_btn_bg_start_w + btn_bg_w / 2
                background_center_h = cur_btn_bg_start_h + btn_bg_h / 2

                textObj = fontObj.render(strList[i], True, COLOR_BLACK)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                screen.blit(textObj, (text_x, text_y))
            
                buttonPosList.append((text_x, text_y))
            pygame.display.flip()

        if buttonClickIndex > -1:
            state = ENUM_STATE_GAME
            

    
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

