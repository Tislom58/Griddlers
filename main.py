import pygame

pygame.init()

# Set window
WIDTH, HEIGHT = 800, 670
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTER = (WIDTH // 2, HEIGHT // 2)

pygame.display.set_caption("Griddles")

# Set the size of grid in 5x5 boxes ; (4, 4) == (20, 20) in cells
GRID_SIZE = (5, 5)

# Color presets
WHITE = (229, 222, 207)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

# Cell state presets
FILL = WHITE
EMPTY = BLACK
HOVER = BLUE
DOT = (229, 222, 206)

# Cell size presets
CELL_SIDE = 20
CELL_BORDER = int(CELL_SIDE / 10)
CELL_GAP = CELL_BORDER


class Cell:
    def __init__(self, x, y):
        # Define init coordinates
        self.coordinates = x, y
        self.fill_coordinates = x + CELL_BORDER + CELL_GAP, y + CELL_BORDER + CELL_GAP

        # Filling parameters
        self.filled_side = CELL_SIDE - 2 * (CELL_BORDER + CELL_GAP)
        self.is_filled = False

        # Define coordinates for sides
        self.left_side = (x, y), (x, y + (CELL_SIDE - CELL_BORDER))
        self.right_side = (x + (CELL_SIDE - CELL_BORDER), y), (x + (CELL_SIDE - CELL_BORDER), y + (CELL_SIDE - CELL_BORDER))
        self.upper_side = (x, y), (x + (CELL_SIDE - CELL_BORDER), y)
        self.bottom_side = (x, y + (CELL_SIDE - CELL_BORDER)), (x + (CELL_SIDE - CELL_BORDER), y + (CELL_SIDE - CELL_BORDER))

    def draw_cell(self):
        #  Draws an empty cell
        pygame.draw.rect(WIN, WHITE, (*self.coordinates, CELL_SIDE, CELL_SIDE), CELL_BORDER)

    def draw_numcell(self, vertical=False):
        # Draws a cell with fill number
        # print(self.upper_side[0][0], self.upper_side[1][0])
        if not vertical:
            pygame.draw.line(WIN, WHITE, self.left_side[0], self.left_side[1], CELL_BORDER)
            pygame.draw.line(WIN, WHITE, self.right_side[0], self.right_side[1], CELL_BORDER)
            for i in range(0, (int(self.bottom_side[1][0]) - CELL_BORDER) - (int(self.bottom_side[0][0]) + CELL_BORDER), 4):
                pygame.draw.line(WIN, WHITE, (self.bottom_side[0][0] + CELL_BORDER + i + 1,
                                              self.bottom_side[0][1]),
                                 (self.bottom_side[0][0] + CELL_BORDER + i + CELL_GAP,
                                  self.bottom_side[0][1]), CELL_BORDER)
        else:
            pygame.draw.line(WIN, WHITE, self.upper_side[0], self.upper_side[1], CELL_BORDER)
            pygame.draw.line(WIN, WHITE, self.bottom_side[0], self.bottom_side[1], CELL_BORDER)
            for i in range(0, (int(self.right_side[1][1]) - CELL_BORDER) - (int(self.right_side[0][1]) + CELL_BORDER), 4):
                pygame.draw.line(WIN, WHITE, (self.right_side[0][0],
                                              self.right_side[0][1] + CELL_BORDER + i + 1),
                                 (self.right_side[0][0],
                                  self.right_side[0][1] + CELL_BORDER + i + CELL_GAP), CELL_BORDER)

    def cell_state(self, state):
        #  Changes the state of the cell - empty / filled / dotted / hovered over
        if state == DOT:
            pygame.draw.circle(WIN, state, (self.coordinates[0] + CELL_SIDE / 2, self.coordinates[1] +
                                            CELL_SIDE / 2), 2)
        else:
            pygame.draw.rect(WIN, state, (*self.fill_coordinates, self.filled_side, self.filled_side))

        if state == FILL or state == DOT:
            self.is_filled = True
        elif state == HOVER:
            pass
        else:
            self.is_filled = False

    def clickable_area(self):
        #  Defines coordinates for clicking the cell
        clickable_area = (*self.fill_coordinates, self.fill_coordinates[0] + self.filled_side, self.fill_coordinates[1]
                          + self.filled_side)
        return clickable_area

    def hover_area(self):
        #  Defines the area that appears blue when cell is hovered over
        hover_area = *self.fill_coordinates, self.filled_side, self.filled_side
        return hover_area


class Unit:
    # Creates a 5x5 unit of cells
    def __init__(self, x, y):
        # Define grid of 5x5 unit made up of cells
        self.unit = [[Cell(x + i * 18, y + j * 18) for j in range(5)] for i in range(5)]

        # Set thickness parameters
        self.unit_thickness = 2
        self.unit_side = 5 * (CELL_SIDE - CELL_BORDER) + CELL_BORDER

        # Define coordinates for sides
        self.left_side = ((x, y),
                          (x, y + (self.unit_side - 1)))
        self.right_side = ((x + (self.unit_side - 1), y),
                           (x + (self.unit_side - 1), y + (self.unit_side - 1)))
        self.upper_side = ((x, y),
                           (x + (self.unit_side - 1), y))
        self.lower_side = ((x, y + (self.unit_side - 1)),
                           (x + (self.unit_side - 1), y + (self.unit_side - 1)))

    def __iter__(self):
        # Flatten the 5x5 list of cells into a single list
        return iter([cell for row in self.unit for cell in row])

    def draw_unit(self):
        #  Draws the unit
        for row_index, row in enumerate(self.unit):
            for cell_index, cell in enumerate(row):
                cell.draw_cell()
                if cell_index == 0:
                    pygame.draw.line(WIN, WHITE, (cell.coordinates[0], cell.coordinates[1] - 2),
                                     (cell.coordinates[0] + CELL_SIDE - 1, cell.coordinates[1] - 2), 2)
                if cell_index == len(self.unit) - 1:
                    pygame.draw.line(WIN, WHITE, (cell.coordinates[0], cell.coordinates[1] + CELL_SIDE),
                                     (cell.coordinates[0] + CELL_SIDE - 1, cell.coordinates[1] + CELL_SIDE), 2)
                if row_index == 0:
                    pygame.draw.line(WIN, WHITE, (cell.coordinates[0] - 2, cell.coordinates[1] - 2),
                                     (cell.coordinates[0] - 2, cell.coordinates[1] + CELL_SIDE + 1), 2)
                if row_index == len(row) - 1:
                    pygame.draw.line(WIN, WHITE, (cell.coordinates[0] + CELL_SIDE, cell.coordinates[1] - 2),
                                     (cell.coordinates[0] + CELL_SIDE, cell.coordinates[1] + CELL_SIDE + 1), 2)

    def unit_hover(self):
        #  Draws the blue area for each cell
        for row in self.unit:
            for cell in row:
                cell_size = pygame.Rect(cell.hover_area())
                if not cell.is_filled:
                    if cell_size.collidepoint(pygame.mouse.get_pos()):
                        cell.cell_state(HOVER)
                    else:
                        cell.cell_state(EMPTY)

    # def get_unit_coords(self):
    #     coords = (self.unit[0][0].coordinates, self.unit[4][4].coordinates)
    #     return coords


class NumUnit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_unit_hor = [[Cell(x + i * 18, y + j * 18) for j in range(3)] for i in range(5)]
        self.num_unit_ver = [[Cell(x + i * 18, y + j * 18) for j in range(5)] for i in range(3)]

    def draw_num_unit_horizontal(self):
        # Draws horizontal units of numbered cells
        for row in self.num_unit_hor:
            for cell in row:
                cell.draw_numcell()

    def draw_num_unit_vertical(self):
        # Draws vertical units of numbered cells
        for row in self.num_unit_ver:
            for cell in row:
                cell.draw_numcell(True)


def grid(rows, cols):
    # Stores grid coordinates
    x, y = CENTER
    _grid = [[Unit(x - (rows * 92) / 2 + i * 92, y - (cols * 92) / 2 + j * 92) for i in range(rows)] for j in
             range(cols)]
    return _grid


def draw_grid(rows, cols):
    # Draws grid
    draw = grid(rows, cols)
    for row_index, row in enumerate(draw):
        for unit_index, unit in enumerate(row):
            unit.draw_unit()
            # print(unit.left_side[0][0], unit.left_side[0][1])
            # print(unit.left_side[0][0], unit.left_side[0][1] - 3 * CELL_SIDE - CELL_BORDER)
            if row_index == 0:
                num_unit = NumUnit(unit.left_side[0][0], unit.left_side[0][1]
                                   - (3 * (CELL_SIDE - CELL_BORDER) + CELL_BORDER))
                num_unit.draw_num_unit_horizontal()
                if unit_index == 0:
                    pygame.draw.line(WIN, WHITE, (unit.left_side[0][0] - unit.unit_thickness,
                                     unit.left_side[0][1] - unit.unit_thickness - 3 * (CELL_SIDE - CELL_BORDER)),
                                     (unit.left_side[0][0] - unit.unit_thickness,
                                     unit.left_side[0][1]), 2)
                if unit_index == len(row) - 1:
                    pygame.draw.line(WIN, WHITE, (unit.right_side[0][0] + unit.unit_thickness - 1,
                                        unit.right_side[0][1] - unit.unit_thickness - 3 * (CELL_SIDE - CELL_BORDER)),
                                     (unit.right_side[0][0] - 1 + unit.unit_thickness,
                                      unit.right_side[0][1]), 2)
            if unit_index == 0:
                num_unit = NumUnit(unit.left_side[0][0] - (3 * (CELL_SIDE - CELL_BORDER) + CELL_BORDER),
                                   unit.left_side[0][1])
                num_unit.draw_num_unit_vertical()
                if row_index == 0:
                    pygame.draw.line(WIN, WHITE, (unit.left_side[0][0] - unit.unit_thickness,
                                     unit.left_side[0][1] - unit.unit_thickness),
                                     (unit.left_side[0][0] - unit.unit_thickness - 3 * (CELL_SIDE - CELL_BORDER),
                                     unit.left_side[0][1] - unit.unit_thickness), 2)
                if row_index == len(draw) - 1:
                    pygame.draw.line(WIN, WHITE, (unit.left_side[1][0] - unit.unit_thickness,
                                                  unit.left_side[1][1] + 3 - unit.unit_thickness),
                                     (unit.left_side[1][0] - unit.unit_thickness - 3 * (CELL_SIDE - CELL_BORDER),
                                      unit.left_side[1][1] + 3 - unit.unit_thickness), 2)


class Button:
    smallfont = pygame.font.SysFont('Corbel', 20)
    is_pressed = False

    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self):
        # Draws the initial button
        pygame.draw.rect(WIN, WHITE, (self.x, self.y, self.width, self.height))
        rendertext = self.smallfont.render(self.text, True, BLUE)
        WIN.blit(rendertext, (self.x + 5, self.y + self.height / 2 - 5))

        self.is_pressed = False

    def press_button(self):
        # Draws pressed button
        pygame.draw.rect(WIN, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(WIN, BLACK, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 3)
        rendertext = self.smallfont.render(self.text, True, BLUE)
        WIN.blit(rendertext, (self.x + 5, self.y + self.height / 2 - 5))

        self.is_pressed = True


def main():
    run = True
    clock = pygame.time.Clock()

    grid1 = grid(*GRID_SIZE)
    manual_button = Button(20, 20, 80, 40, 'Manual')
    automatic_button = Button(20, 70, 80, 40, 'Automatic')

    manual_button.draw_button()
    automatic_button.draw_button()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                for unit in grid1:
                    for row in unit:
                        for cell in row:

                            # Get the position of the click
                            x, y = event.pos

                            if manual_button.is_pressed:
                                # Check if the click is within the clickable area
                                if (cell.clickable_area()[0] <= x <= cell.clickable_area()[2] and
                                        cell.clickable_area()[1]
                                        <= y <= cell.clickable_area()[3]):
                                    if event.button == 1:  # Left click
                                        if not cell.is_filled:
                                            cell.cell_state(FILL)
                                        else:
                                            cell.cell_state(EMPTY)
                                            cell.cell_state(DOT)
                                    if event.button == 3:  # Right click
                                        cell.cell_state(EMPTY)

                            if (manual_button.x <= x <= manual_button.x + manual_button.width and
                                    manual_button.y <= y <= manual_button.y + manual_button.height):
                                if event.button == 1:
                                    manual_button.press_button()
                                    automatic_button.draw_button()

                            if (automatic_button.x <= x <= automatic_button.x + automatic_button.width and
                                    automatic_button.y <= y <= automatic_button.y + automatic_button.height):
                                if event.button == 1:
                                    automatic_button.press_button()
                                    manual_button.draw_button()

        draw_grid(*GRID_SIZE)
        for row in grid1:
            for unit in row:
                if manual_button.is_pressed:
                    unit.unit_hover()

        pygame.display.update()

    pygame.quit()


main()
