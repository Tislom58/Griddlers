import pygame

pygame.init()

# Set window
WIDTH, HEIGHT = 800, 670
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTER = (WIDTH // 2, HEIGHT // 2)

pygame.display.set_caption("Griddles")

# Color presets
WHITE = (229, 222, 207)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

FILL = WHITE
EMPTY = BLACK
HOVER = BLUE
DOT = (229, 222, 206)


class Cell:
    # Set parameters of the cell
    side = 20  # size of the cell side
    width = 2  # width of the cell's border
    gap = 2  # width of the gap between cell's border and filled cell
    fill_side = side - 2 * (width + gap)  # size of the filled cell size

    is_filled = False  # checks if the cell is filled

    def __init__(self, x, y):
        self.coordinates = x, y
        self.fill_coordinates = x + self.width + self.gap, y + self.width + self.gap

    #  Draws an outline of a cell
    def draw_cell(self):
        pygame.draw.rect(WIN, WHITE, (*self.coordinates, self.side, self.side), self.width)

    #  Changes the state of a cell
    def cell_state(self, state):
        if state == DOT:
            pygame.draw.circle(WIN, state, (self.coordinates[0] + self.side / 2, self.coordinates[1] +
                                            self.side / 2), 2)
        else:
            pygame.draw.rect(WIN, state, (*self.fill_coordinates, self.fill_side, self.fill_side))

        if state == FILL or state == DOT:
            self.is_filled = True
        elif state == HOVER:
            pass
        else:
            self.is_filled = False

    #  Defines area that can be clicked
    def clickable_area(self):
        clickable_area = (*self.fill_coordinates, self.fill_coordinates[0] + self.fill_side, self.fill_coordinates[1]
                          + self.fill_side)
        return clickable_area

    #  Defines the area that appears blue
    def hover_area(self):
        hover_area = *self.fill_coordinates, self.fill_side, self.fill_side
        return hover_area


class Grid:
    def __init__(self, cols, rows, cell_side):
        self.cols = cols
        self.rows = rows
        self.grid = [[Cell((CENTER[0] - cols / 2 * cell_side) + i * cell_side, (CENTER[1] - rows / 2 * cell_side) + j *
                           cell_side) for j in range(cols)] for i in range(rows)]

    #  Draws the whole grid
    def draw_grid(self):
        for row in self.grid:
            for cell in row:
                cell.draw_cell()

    #  Draws the blue area for each cell
    def grid_hover(self):
        for row in self.grid:
            for cell in row:
                cell_size = pygame.Rect(cell.hover_area())
                if not cell.is_filled:
                    if cell_size.collidepoint(pygame.mouse.get_pos()):
                        cell.cell_state(HOVER)
                    else:
                        cell.cell_state(EMPTY)


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
        pygame.draw.rect(WIN, WHITE, (self.x, self.y, self.width, self.height))
        rendertext = self.smallfont.render(self.text, True, BLUE)
        WIN.blit(rendertext, (self.x + 5, self.y + self.height / 2 - 5))

        self.is_pressed = False

    def press_button(self):
        pygame.draw.rect(WIN, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(WIN, BLACK, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 3)
        rendertext = self.smallfont.render(self.text, True, BLUE)
        WIN.blit(rendertext, (self.x + 5, self.y + self.height / 2 - 5))

        self.is_pressed = True


def main():
    run = True
    clock = pygame.time.Clock()

    grid = Grid(20, 20, 18)
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

                for row in grid.grid:
                    for cell in row:

                        # Get the position of the click
                        x, y = event.pos

                        if manual_button.is_pressed:
                            # Check if the click is within the clickable area
                            if (cell.clickable_area()[0] <= x <= cell.clickable_area()[2] and cell.clickable_area()[1]
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

        grid.draw_grid()
        if manual_button.is_pressed:
            grid.grid_hover()

        pygame.display.update()

    pygame.quit()


main()
