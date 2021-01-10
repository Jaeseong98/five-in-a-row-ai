from game.enum import PygameStateEnum
from game.config import PygameColor

import pygame
import math

pygame.init()

PygameColor.COLOR_RED = (255, 0, 0)
PygameColor.COLOR_BLACK = (0, 0, 0)
PygameColor.COLOR_BOARD = (240, 220, 165)
PygameColor.COLOR_GRAY = (180, 180, 180)
PygameColor.COLOR_UNSELECTABLE_BG = (255, 175, 175)
PygameColor.COLOR_WHITE = (255, 255, 255)
PygameColor.COLOR_YELLOW = (255, 255, 0)

cell_count = 15
cell_size = 30

radius = 13
diff = 7

board_start_w = 40
board_start_h = 40
board_end_w = board_start_w + cell_size * (cell_count - 1)
board_end_h = board_start_h + cell_size * (cell_count - 1)

btn_bg_w = 280
btn_bg_h = 50
btn_bg_start_w = 125
btn_bg_start_h = 200

size = [500, 500]

def _GetPygamePos(pos):
    i, j = pos
    return (board_start_w + i * cell_size, board_start_h + j * cell_size)

def _DrawHoverZone(pos):
    pygame.draw.circle(screen, PygameColor.COLOR_YELLOW, _GetPygamePos(pos), radius - 10, width = 0)
    return

def _EraseHoverZone(pos):
    pygame.draw.circle(screen, PygameColor.COLOR_BOARD, _GetPygamePos(pos), radius - 10, width = 0)
    
    w, h = pos
    w_line = board_start_w + cell_size * w
    h_line = board_start_h + cell_size * h
    w_start = 0.5 if w > 0 else 0
    w_end = 0.5 if w < 14 else 0
    h_start = 0.5 if h > 0 else 0
    h_end = 0.5 if h < 14 else 0
    pygame.draw.line(screen, PygameColor.COLOR_BLACK, (w_line - w_start * cell_size, h_line), (w_line + w_end * cell_size , h_line), width = 2)
    pygame.draw.line(screen, PygameColor.COLOR_BLACK, (w_line, h_line - h_start * cell_size), (w_line, h_line + h_end * cell_size), width = 2)
    return

def _DrawBlackStone(pos):
    pygame.draw.circle(screen, PygameColor.COLOR_BLACK, _GetPygamePos(pos), radius, width = 0)
    return

def _DrawWhiteStone(pos):
    pygame.draw.circle(screen, PygameColor.COLOR_WHITE, _GetPygamePos(pos), radius, width = 0)
    pygame.draw.circle(screen, PygameColor.COLOR_BLACK, _GetPygamePos(pos), radius, width = 1)
    return

def _DrawUnseletable(pos):
    pg_pos = _GetPygamePos(pos)
    pygame.draw.circle(screen, PygameColor.COLOR_UNSELECTABLE_BG, pg_pos, radius, width = 0)
    pygame.draw.circle(screen, PygameColor.COLOR_RED, pg_pos, radius, width = 2)

    pg_pos_w, pg_pos_h = pg_pos
    pygame.draw.line(screen, PygameColor.COLOR_RED, (pg_pos_w - diff, pg_pos_h - diff), (pg_pos_w + diff, pg_pos_h + diff), width = 3)
    pygame.draw.line(screen, PygameColor.COLOR_RED, (pg_pos_w + diff, pg_pos_h - diff), (pg_pos_w - diff, pg_pos_h + diff), width = 3)
    return

def _IsButtonCollision(pos):
    for i in range(3):
        w, h = pos
        cur_btn_bg_start_w = btn_bg_start_w
        cur_btn_bg_start_h = btn_bg_start_h + (3 / 2 * btn_bg_h * i)
        if (cur_btn_bg_start_w <= w and w <= cur_btn_bg_start_w + btn_bg_w) and (cur_btn_bg_start_h <= h and h <= cur_btn_bg_start_h + btn_bg_h):
            return i
    return -1

def _IsCellCollision(pos):
    w, h = pos
    div_w, mod_w = divmod((w - board_start_w + 0.5 * cell_size), cell_size)
    div_h, mod_h = divmod((h - board_start_h + 0.5 * cell_size), cell_size)

    if ((3 < mod_w and mod_w < 27) and (3 < mod_h and mod_h < 27)):
        return (int(div_w), int(div_h))
    return (-1, -1)

screen = pygame.display.set_mode(size)

title_name = "Five In A Row"
pygame.display.set_caption(title_name)

done = False
clock = pygame.time.Clock()

state = PygameStateEnum.STATE_MENU

is_first_draw_menu = True
is_first_draw_game = True
cur_hover_w, cur_hover_h = -1, -1
hover_w, hover_h = -1, -1
click_w, click_h = -1, -1

array = [ [ 0 for i in range(cell_count) ] for j in range(cell_count)]

is_black_turn = True

while not done:
    clock.tick(10)

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         done = True
    #     if event.type == pygame.MOUSEMOTION:
    #             print('Event1 Triggered!')
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #             print('Event2 Triggered!')

    if state == PygameStateEnum.STATE_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEMOTION:
                buttonHoverIndex = _IsButtonCollision(event.pos)
                # print(buttonHoverIndex)
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonClickIndex = _IsButtonCollision(event.pos)
                print(buttonClickIndex)

        if is_first_draw_menu:
            is_first_draw_menu = False
            buttonHoverIndex = -1
            buttonClickIndex = -1
            isButtonHoverList = []

            screen.fill(PygameColor.COLOR_BOARD)

            fontObj = pygame.font.Font(None, 60)
            textObj = fontObj.render('Five in a Row', True, PygameColor.COLOR_BLACK)
            screen.blit(textObj, (135, 70))


            fontObj = pygame.font.Font(None, 30)
            strList = ['Human vs Human', 'Human vs AI(Rule-Base)', 'Human vs AI(RL)']
            buttonPosList = []
            for i in range(3):
                cur_btn_bg_start_w = btn_bg_start_w
                cur_btn_bg_start_h = btn_bg_start_h + (3 / 2 * btn_bg_h * i)

                textBG = pygame.draw.rect(screen, PygameColor.COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, btn_bg_w, btn_bg_h), width=0)
                
                background_center_w = cur_btn_bg_start_w + btn_bg_w / 2
                background_center_h = cur_btn_bg_start_h + btn_bg_h / 2

                textObj = fontObj.render(strList[i], True, PygameColor.COLOR_BLACK)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                screen.blit(textObj, (text_x, text_y))
            
                buttonPosList.append((text_x, text_y))
                isButtonHoverList.append(False)
            pygame.display.flip()

        buttonUpdateList = []
        for i in range(3):
            if buttonHoverIndex != i and isButtonHoverList[i] == True:
                cur_btn_bg_start_w = btn_bg_start_w
                cur_btn_bg_start_h = btn_bg_start_h + (3 / 2 * btn_bg_h * i)

                textBG = pygame.draw.rect(screen, PygameColor.COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, btn_bg_w, btn_bg_h), width=0)
                
                background_center_w = cur_btn_bg_start_w + btn_bg_w / 2
                background_center_h = cur_btn_bg_start_h + btn_bg_h / 2

                textObj = fontObj.render(strList[i], True, PygameColor.COLOR_BLACK)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                screen.blit(textObj, (text_x, text_y))

                buttonUpdateList.append((cur_btn_bg_start_w, cur_btn_bg_start_h, btn_bg_w, btn_bg_h))
                isButtonHoverList[i] = False

            if buttonHoverIndex == i and isButtonHoverList[i] == False:
                cur_btn_bg_start_w = btn_bg_start_w
                cur_btn_bg_start_h = btn_bg_start_h + (3 / 2 * btn_bg_h * i)

                textBG = pygame.draw.rect(screen, PygameColor.COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, btn_bg_w, btn_bg_h), width=0)
                
                background_center_w = cur_btn_bg_start_w + btn_bg_w / 2
                background_center_h = cur_btn_bg_start_h + btn_bg_h / 2

                textObj = fontObj.render(strList[i], True, PygameColor.COLOR_WHITE)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                screen.blit(textObj, (text_x, text_y))

                buttonUpdateList.append((cur_btn_bg_start_w, cur_btn_bg_start_h, btn_bg_w, btn_bg_h))
                isButtonHoverList[i] = True

        if len(buttonUpdateList) > 0:
            pygame.display.update(buttonUpdateList)

        if buttonClickIndex > -1:
            state = PygameStateEnum.STATE_GAME

    elif state == PygameStateEnum.STATE_GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEMOTION:
                hover_w, hover_h = _IsCellCollision(event.pos)
                print((hover_w, hover_h))
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_w, click_h = _IsCellCollision(event.pos)

        if is_first_draw_game:
            is_first_draw_game = False
            screen.fill(PygameColor.COLOR_BOARD)

            for i in range(cell_count):
                pygame.draw.line(screen, PygameColor.COLOR_BLACK, (board_start_w + cell_size * i , board_start_h), (board_start_w + cell_size * i , board_end_h), width = 2)
                pygame.draw.line(screen, PygameColor.COLOR_BLACK, (board_start_w, board_start_h + cell_size * i), (board_end_w, board_start_h + cell_size * i), width = 2)

            _DrawUnseletable((5, 7))
            array[5][7] = 1
            
            pygame.display.flip()

        updateRectList = []
        if ((0 <= hover_w and hover_w <= 14) and (0 <= hover_h and hover_h <= 14)):
            if array[hover_w][hover_h] == 0:
                if((0 <= cur_hover_w and cur_hover_w <= 14) and (0 <= cur_hover_h and cur_hover_h <= 14)):
                    _EraseHoverZone((cur_hover_w, cur_hover_h))
                    updateRectList.append(pygame.Rect(board_start_w + cell_size * (cur_hover_w - 0.5), board_start_h + cell_size * (cur_hover_h - 0.5), cell_size, cell_size))

                cur_hover_w, cur_hover_h = hover_w, hover_h
                _DrawHoverZone((cur_hover_w, cur_hover_h))
                updateRectList.append(pygame.Rect(board_start_w + cell_size * (cur_hover_w - 0.5), board_start_h + cell_size * (cur_hover_h - 0.5), cell_size, cell_size))

        if ((0 <= click_w and click_w <= 14) and (0 <= click_h and click_h <= 14)):
            if array[click_w][click_h] == 0:
                if is_black_turn:
                    _DrawBlackStone((click_w, click_h))
                    array[click_w][click_h] = 2
                    cur_hover_w, cur_hover_h = -1, -1
                else:
                    _DrawWhiteStone((click_w, click_h))
                    array[click_w][click_h] = 3
                    cur_hover_w, cur_hover_h = -1, -1

                is_black_turn = not is_black_turn

                updateRectList.append(pygame.Rect(board_start_w + cell_size * (click_w - 0.5), board_start_h + cell_size * (click_h - 0.5), cell_size, cell_size))


        if len(updateRectList) > 0:
                    pygame.display.update(updateRectList)

