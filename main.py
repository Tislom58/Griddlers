import pygame

pygame.init()

# Set window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTER = (WIDTH // 2, HEIGHT // 2)

pygame.display.set_caption("Griddles")

# Color presets
WHITE = (229, 222, 207)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)


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

    def draw_cell(self):
        pygame.draw.rect(WIN, WHITE, (*self.coordinates, self.side, self.side), self.width)

    def fill_cell(self):
        pygame.draw.rect(WIN, WHITE, (*self.fill_coordinates, self.fill_side, self.fill_side))
        self.is_filled = True

    def empty_cell(self):
        pygame.draw.rect(WIN, BLACK, (*self.fill_coordinates, self.fill_side, self.fill_side))
        self.is_filled = False

    def hover_cell(self):
        pygame.draw.rect(WIN, BLUE, (*self.fill_coordinates, self.fill_side, self.fill_side))

    def clickable_area(self):
        clickable_area = (*self.fill_coordinates, self.fill_coordinates[0] + self.fill_side, self.fill_coordinates[1]
                          + self.fill_side)
        return clickable_area

    def hover_area(self):
        hover_area = *self.fill_coordinates, self.fill_side, self.fill_side
        return hover_area


class Grid:
    def __init__(self, cols, rows, cell_side):
        self.cols = cols
        self.rows = rows
        self.grid = [[Cell(CENTER[0] + i * cell_side, CENTER[1] + j * cell_side) for j in range(cols)] for i in
                     range(rows)]

    def draw_grid(self):
        for row in self.grid:
            for cell in row:
                cell.draw_cell()

    def grid_hover(self):
        for row in self.grid:
            for cell in row:
                cell_size = pygame.Rect(cell.hover_area())
                if not cell.is_filled:
                    if cell_size.collidepoint(pygame.mouse.get_pos()):
                        cell.hover_cell()
                    else:
                        cell.empty_cell()


def main():
    run = True
    clock = pygame.time.Clock()

    grid = Grid(20, 20, 18)

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

                        # Check if the click is within the clickable area
                        if (cell.clickable_area()[0] <= x <= cell.clickable_area()[2] and cell.clickable_area()[1]
                                <= y <= cell.clickable_area()[3]):
                            if event.button == 1:  # Left click
                                print("Left click detected at position", event.pos)
                                cell.fill_cell()
                            if event.button == 3:  # Right click
                                print("Right click detected at position", event.pos)
                                cell.empty_cell()

        grid.draw_grid()
        grid.grid_hover()

        pygame.display.update()

    pygame.quit()


main()
