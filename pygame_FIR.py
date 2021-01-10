from game.enum import PygameStateEnum
from game.config import PygameConfig

import pygame
import math

class PygameFIR(object):
    def __init__(self, mode):
        self.title_name = "Five In A Row"

        self.is_finished_pygame = False

        self.state = PygameStateEnum.STATE_MENU

        self.is_first_draw_menu = True
        self.is_first_draw_game = True
        self.cur_hover_w, self.cur_hover_h = -1, -1
        self.hover_w, self.hover_h = -1, -1
        self.click_w, self.click_h = -1, -1

        self.array = [ [ 0 for i in range(PygameConfig.CELL_COUNT) ] for j in range(PygameConfig.CELL_COUNT)]

        self.is_black_turn = True
        
    def _GetPygamePos(self, pos):
        i, j = pos
        return (PygameConfig.BOARD_START_W + i * PygameConfig.CELL_SIZE, PygameConfig.BOARD_START_H + j * PygameConfig.CELL_SIZE)

    def _DrawHoverZone(self, pos):
        pygame.draw.circle(self.screen, PygameConfig.COLOR_YELLOW, self._GetPygamePos(pos), PygameConfig.STONE_RADIUS - 10, width = 0)
        return

    def _EraseHoverZone(self, pos):
        pygame.draw.circle(self.screen, PygameConfig.COLOR_BOARD, self._GetPygamePos(pos), PygameConfig.STONE_RADIUS - 10, width = 0)
        
        w, h = pos
        w_line = PygameConfig.BOARD_START_W + PygameConfig.CELL_SIZE * w
        h_line = PygameConfig.BOARD_START_H + PygameConfig.CELL_SIZE * h
        w_start, w_end = 0.5 if w > 0 else 0, 0.5 if w < 14 else 0
        h_start, h_end = 0.5 if h > 0 else 0, 0.5 if h < 14 else 0
        pygame.draw.line(self.screen, PygameConfig.COLOR_BLACK, (w_line - w_start * PygameConfig.CELL_SIZE, h_line), (w_line + w_end * PygameConfig.CELL_SIZE , h_line), width = 2)
        pygame.draw.line(self.screen, PygameConfig.COLOR_BLACK, (w_line, h_line - h_start * PygameConfig.CELL_SIZE), (w_line, h_line + h_end * PygameConfig.CELL_SIZE), width = 2)
        return

    def _DrawBlackStone(self, pos):
        pygame.draw.circle(self.screen, PygameConfig.COLOR_BLACK, self._GetPygamePos(pos), PygameConfig.STONE_RADIUS, width = 0)
        return

    def _DrawWhiteStone(self, pos):
        pygame.draw.circle(self.screen, PygameConfig.COLOR_WHITE, self._GetPygamePos(pos), PygameConfig.STONE_RADIUS, width = 0)
        pygame.draw.circle(self.screen, PygameConfig.COLOR_BLACK, self._GetPygamePos(pos), PygameConfig.STONE_RADIUS, width = 1)
        return

    def _DrawUnseletable(self, pos):
        pg_pos = self._GetPygamePos(pos)
        pygame.draw.circle(self.screen, PygameConfig.COLOR_UNSELECTABLE_BG, pg_pos, PygameConfig.STONE_RADIUS, width = 0)
        pygame.draw.circle(self.screen, PygameConfig.COLOR_RED, pg_pos, PygameConfig.STONE_RADIUS, width = 2)

        pg_pos_w, pg_pos_h = pg_pos
        pygame.draw.line(self.screen, PygameConfig.COLOR_RED, (pg_pos_w - PygameConfig.STONE_DIFF, pg_pos_h - PygameConfig.STONE_DIFF), (pg_pos_w + PygameConfig.STONE_DIFF, pg_pos_h + PygameConfig.STONE_DIFF), width = 3)
        pygame.draw.line(self.screen, PygameConfig.COLOR_RED, (pg_pos_w + PygameConfig.STONE_DIFF, pg_pos_h - PygameConfig.STONE_DIFF), (pg_pos_w - PygameConfig.STONE_DIFF, pg_pos_h + PygameConfig.STONE_DIFF), width = 3)
        return

    def _IsButtonCollision(self, pos):
        for i in range(3):
            w, h = pos
            cur_btn_bg_start_w = PygameConfig.BUTTON_START_W
            cur_btn_bg_start_h = PygameConfig.BUTTON_START_H + (3 / 2 * PygameConfig.BUTTON_H * i)
            if (cur_btn_bg_start_w <= w and w <= cur_btn_bg_start_w + PygameConfig.BUTTON_W) and (cur_btn_bg_start_h <= h and h <= cur_btn_bg_start_h + PygameConfig.BUTTON_H):
                return i
        return -1

    def _IsCellCollision(self, pos):
        w, h = pos
        div_w, mod_w = divmod((w - PygameConfig.BOARD_START_W + 0.5 * PygameConfig.CELL_SIZE), PygameConfig.CELL_SIZE)
        div_h, mod_h = divmod((h - PygameConfig.BOARD_START_H + 0.5 * PygameConfig.CELL_SIZE), PygameConfig.CELL_SIZE)

        if ((3 < mod_w and mod_w < 27) and (3 < mod_h and mod_h < 27)):
            return (int(div_w), int(div_h))
        return (-1, -1)

    def _SetMenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_finished_pygame = True
            if event.type == pygame.MOUSEMOTION:
                self.buttonHoverIndex = self._IsButtonCollision(event.pos)
                # print(self.buttonHoverIndex)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.buttonClickIndex = self._IsButtonCollision(event.pos)
                print(self.buttonClickIndex)

        if self.is_first_draw_menu:
            self.is_first_draw_menu = False
            self.buttonHoverIndex = -1
            self.buttonClickIndex = -1
            self.isButtonHoverList = []

            self.screen.fill(PygameConfig.COLOR_BOARD)

            self.fontObj = pygame.font.Font(None, 60)
            textObj = self.fontObj.render('Five in a Row', True, PygameConfig.COLOR_BLACK)
            self.screen.blit(textObj, (135, 70))


            self.fontObj = pygame.font.Font(None, 30)
            self.strList = ['Human vs Human', 'Human vs AI(Rule-Base)', 'Human vs AI(RL)']
            buttonPosList = []
            for i in range(3):
                cur_btn_bg_start_w = PygameConfig.BUTTON_START_W
                cur_btn_bg_start_h = PygameConfig.BUTTON_START_H + (3 / 2 * PygameConfig.BUTTON_H * i)

                textBG = pygame.draw.rect(self.screen, PygameConfig.COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, PygameConfig.BUTTON_W, PygameConfig.BUTTON_H), width=0)
                
                background_center_w = cur_btn_bg_start_w + PygameConfig.BUTTON_W / 2
                background_center_h = cur_btn_bg_start_h + PygameConfig.BUTTON_H / 2

                textObj = self.fontObj.render(self.strList[i], True, PygameConfig.COLOR_BLACK)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                self.screen.blit(textObj, (text_x, text_y))
            
                buttonPosList.append((text_x, text_y))
                self.isButtonHoverList.append(False)
            pygame.display.flip()

        buttonUpdateList = []
        for i in range(3):
            if self.buttonHoverIndex != i and self.isButtonHoverList[i] == True:
                cur_btn_bg_start_w = PygameConfig.BUTTON_START_W
                cur_btn_bg_start_h = PygameConfig.BUTTON_START_H + (3 / 2 * PygameConfig.BUTTON_H * i)

                textBG = pygame.draw.rect(self.screen, PygameConfig.COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, PygameConfig.BUTTON_W, PygameConfig.BUTTON_H), width=0)
                
                background_center_w = cur_btn_bg_start_w + PygameConfig.BUTTON_W / 2
                background_center_h = cur_btn_bg_start_h + PygameConfig.BUTTON_H / 2

                textObj = self.fontObj.render(self.strList[i], True, PygameConfig.COLOR_BLACK)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                self.screen.blit(textObj, (text_x, text_y))

                buttonUpdateList.append((cur_btn_bg_start_w, cur_btn_bg_start_h, PygameConfig.BUTTON_W, PygameConfig.BUTTON_H))
                self.isButtonHoverList[i] = False

            if self.buttonHoverIndex == i and self.isButtonHoverList[i] == False:
                cur_btn_bg_start_w = PygameConfig.BUTTON_START_W
                cur_btn_bg_start_h = PygameConfig.BUTTON_START_H + (3 / 2 * PygameConfig.BUTTON_H * i)

                textBG = pygame.draw.rect(self.screen, PygameConfig.COLOR_GRAY, (cur_btn_bg_start_w, cur_btn_bg_start_h, PygameConfig.BUTTON_W, PygameConfig.BUTTON_H), width=0)
                
                background_center_w = cur_btn_bg_start_w + PygameConfig.BUTTON_W / 2
                background_center_h = cur_btn_bg_start_h + PygameConfig.BUTTON_H / 2

                textObj = self.fontObj.render(self.strList[i], True, PygameConfig.COLOR_WHITE)
                (x, y, w, h) = textObj.get_rect()
                text_x = background_center_w - w / 2
                text_y = background_center_h - h / 2
                self.screen.blit(textObj, (text_x, text_y))

                buttonUpdateList.append((cur_btn_bg_start_w, cur_btn_bg_start_h, PygameConfig.BUTTON_W, PygameConfig.BUTTON_H))
                self.isButtonHoverList[i] = True

        if len(buttonUpdateList) > 0:
            pygame.display.update(buttonUpdateList)

        if self.buttonClickIndex > -1:
            self.state = PygameStateEnum.STATE_GAME

    def _SetGame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_finished_pygame = True
            if event.type == pygame.MOUSEMOTION:
                self.hover_w, self.hover_h = self._IsCellCollision(event.pos)
                print((self.hover_w, self.hover_h))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_w, self.click_h = self._IsCellCollision(event.pos)

        if self.is_first_draw_game:
            self.is_first_draw_game = False
            self.screen.fill(PygameConfig.COLOR_BOARD)

            for i in range(PygameConfig.CELL_COUNT):
                pygame.draw.line(self.screen, PygameConfig.COLOR_BLACK, (PygameConfig.BOARD_START_W + PygameConfig.CELL_SIZE * i , PygameConfig.BOARD_START_H), (PygameConfig.BOARD_START_W + PygameConfig.CELL_SIZE * i , PygameConfig.BOARD_END_H), width = 2)
                pygame.draw.line(self.screen, PygameConfig.COLOR_BLACK, (PygameConfig.BOARD_START_W, PygameConfig.BOARD_START_H + PygameConfig.CELL_SIZE * i), (PygameConfig.BOARD_END_W, PygameConfig.BOARD_START_H + PygameConfig.CELL_SIZE * i), width = 2)

            self._DrawUnseletable((5, 7))
            self.array[5][7] = 1
            
            pygame.display.flip()

        updateRectList = []
        if ((0 <= self.hover_w and self.hover_w <= 14) and (0 <= self.hover_h and self.hover_h <= 14)):
            if self.array[self.hover_w][self.hover_h] == 0:
                if((0 <= self.cur_hover_w and self.cur_hover_w <= 14) and (0 <= self.cur_hover_h and self.cur_hover_h <= 14)):
                    self._EraseHoverZone((self.cur_hover_w, self.cur_hover_h))
                    updateRectList.append(pygame.Rect(PygameConfig.BOARD_START_W + PygameConfig.CELL_SIZE * (self.cur_hover_w - 0.5), PygameConfig.BOARD_START_H + PygameConfig.CELL_SIZE * (self.cur_hover_h - 0.5), PygameConfig.CELL_SIZE, PygameConfig.CELL_SIZE))

                self.cur_hover_w, self.cur_hover_h = self.hover_w, self.hover_h
                self._DrawHoverZone((self.cur_hover_w, self.cur_hover_h))
                updateRectList.append(pygame.Rect(PygameConfig.BOARD_START_W + PygameConfig.CELL_SIZE * (self.cur_hover_w - 0.5), PygameConfig.BOARD_START_H + PygameConfig.CELL_SIZE * (self.cur_hover_h - 0.5), PygameConfig.CELL_SIZE, PygameConfig.CELL_SIZE))

        if ((0 <= self.click_w and self.click_w <= 14) and (0 <= self.click_h and self.click_h <= 14)):
            if self.array[self.click_w][self.click_h] == 0:
                if self.is_black_turn:
                    self._DrawBlackStone((self.click_w, self.click_h))
                    self.array[self.click_w][self.click_h] = 2
                    self.cur_hover_w, self.cur_hover_h = -1, -1
                else:
                    self._DrawWhiteStone((self.click_w, self.click_h))
                    self.array[self.click_w][self.click_h] = 3
                    self.cur_hover_w, self.cur_hover_h = -1, -1

                self.is_black_turn = not self.is_black_turn

                updateRectList.append(pygame.Rect(PygameConfig.BOARD_START_W + PygameConfig.CELL_SIZE * (self.click_w - 0.5), PygameConfig.BOARD_START_H + PygameConfig.CELL_SIZE * (self.click_h - 0.5), PygameConfig.CELL_SIZE, PygameConfig.CELL_SIZE))


        if len(updateRectList) > 0:
                    pygame.display.update(updateRectList)

    def start(self):
        pygame.init()

        self.screen = pygame.display.set_mode(PygameConfig.SCREEN_SIZE)

        pygame.display.set_caption(self.title_name)

        self.clock = pygame.time.Clock()

        while not self.is_finished_pygame:
            self.clock.tick(10)

            if self.state == PygameStateEnum.STATE_MENU:
                self._SetMenu()

            elif self.state == PygameStateEnum.STATE_GAME:
                self._SetGame()

if __name__ == "__main__":
    pygame_FIR = PygameFIR("")
    pygame_FIR.start()