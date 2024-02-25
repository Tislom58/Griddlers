import pygame

class Cell:
    def __init__(self, x, y):
        # Define init coordinates
        self.coordinates = x, y
        self.fill_coordinates = x + CELL_BORDER + CELL_GAP, y + CELL_BORDER + CELL_GAP

        # Filling parameters
        self.filled_side = CELL_SIDE - 2 * (CELL_BORDER + CELL_GAP)
        self.is_filled = False
        self.input_rect = pygame.Rect(x + 2, y + 2, CELL_SIDE - 4, CELL_SIDE - 4)

        # Default values for number input
        self.input_text = ''
        self.active = False

        # Define coordinates for sides
        self.left_side = (x, y), (x, y + (CELL_SIDE - CELL_BORDER))
        self.right_side = (x + (CELL_SIDE - CELL_BORDER), y), (x + (CELL_SIDE - CELL_BORDER), y + (CELL_SIDE - CELL_BORDER))
        self.upper_side = (x, y), (x + (CELL_SIDE - CELL_BORDER), y)
        self.bottom_side = (x, y + (CELL_SIDE - CELL_BORDER)), (x + (CELL_SIDE - CELL_BORDER), y + (CELL_SIDE - CELL_BORDER))

    def draw_cell(self):
        #  Draws an empty cell
        pygame.draw.rect(WINDOW, WHITE, (*self.coordinates, CELL_SIDE, CELL_SIDE), CELL_BORDER)

    def draw_numcell(self, vertical=False):
        # Draws a cell with fill number
        # print(self.upper_side[0][0], self.upper_side[1][0])
        if not vertical:
            pygame.draw.line(WINDOW, WHITE, self.left_side[0], self.left_side[1], CELL_BORDER)
            pygame.draw.line(WINDOW, WHITE, self.right_side[0], self.right_side[1], CELL_BORDER)
            for i in range(0, (int(self.bottom_side[1][0]) - CELL_BORDER) - (int(self.bottom_side[0][0]) + CELL_BORDER), 4):
                pygame.draw.line(WINDOW, WHITE, (self.bottom_side[0][0] + CELL_BORDER + i + 1,
                                                 self.bottom_side[0][1]),
                                 (self.bottom_side[0][0] + CELL_BORDER + i + CELL_GAP,
                                  self.bottom_side[0][1]), CELL_BORDER)
        else:
            pygame.draw.line(WINDOW, WHITE, self.upper_side[0], self.upper_side[1], CELL_BORDER)
            pygame.draw.line(WINDOW, WHITE, self.bottom_side[0], self.bottom_side[1], CELL_BORDER)
            for i in range(0, (int(self.right_side[1][1]) - CELL_BORDER) - (int(self.right_side[0][1]) + CELL_BORDER), 4):
                pygame.draw.line(WINDOW, WHITE, (self.right_side[0][0],
                                                 self.right_side[0][1] + CELL_BORDER + i + 1),
                                 (self.right_side[0][0],
                                  self.right_side[0][1] + CELL_BORDER + i + CELL_GAP), CELL_BORDER)

    def cell_state(self, state):
        #  Changes the state of the cell - empty / filled / dotted / hovered over
        if state == DOT:
            pygame.draw.circle(WINDOW, state, (self.coordinates[0] + CELL_SIDE / 2, self.coordinates[1] +
                                               CELL_SIDE / 2), 2)
        else:
            pygame.draw.rect(WINDOW, state, (*self.fill_coordinates, self.filled_side, self.filled_side))

        if state == FILL or state == DOT:
            self.is_filled = True
        elif state == HOVER:
            pass
        else:
            self.is_filled = False

    def clickable_area(self, x, y):
        #  Defines coordinates for clicking the cell
        return (self.fill_coordinates[0] <= x <= self.fill_coordinates[0] + self.filled_side and self.fill_coordinates[1]
                <= y <= self.fill_coordinates[1] + self.filled_side)

    def hover_area(self):
        #  Defines the area that appears blue when cell is hovered over
        hover_area = *self.fill_coordinates, self.filled_side, self.filled_side
        return hover_area

    # def set_text(self, active, input_text):
    #     self.input_text = input_text

    def display_num(self):
        # Displays instruction number

        # pygame.draw.rect(WIN, BLUE, self.input_rect)
        # pygame.draw.rect(WIN, DOT, self.input_rect)

        # Set color
        # color_active = BLUE
        # color_passive = BLACK
        # color = color_active if self.active else color_passive

        # pygame.draw.rect(WIN, color, self.input_rect)

        if self.active:
            pygame.draw.rect(WINDOW, BLUE, self.input_rect)
        else:
            pygame.draw.rect(WINDOW, BLACK, self.input_rect)
        print(self.active)

        text_surface = default_font.render(self.input_text, True, WHITE)

        if len(self.input_text) == 2:
            WINDOW.blit(text_surface, (self.input_rect.x + 1, self.input_rect.y + 2))
        else:
            WINDOW.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 2))