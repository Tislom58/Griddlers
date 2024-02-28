import pygame

# RGB color presets
BLACK = (47, 45, 52)
WHITE = (224, 214, 176)
BLUE = (100, 149, 237)

CENTER = (0, 0)


def get_center(center):
    global CENTER
    CENTER = center


class Cell:
    init_size = 20
    gap = 2

    def __init__(self, screen, x, y, size, fill=False, dot=False, number=None):

        self.screen = screen

        # Position
        self.size = size
        self.border = size // 10
        self.inner_size = size - 2 * (self.border + self.gap)

        self.x = x
        self.y = y
        self.inner_x = x + self.border + self.gap
        self.inner_y = y + self.border + self.gap

        self.rect = pygame.Rect(x, y, size, size)
        self.inner_rect = pygame.Rect(self.inner_x, self.inner_y, self.inner_size, self.inner_size)

        self.is_filled = fill
        self.has_dot = dot
        self.number = str(number)

    def draw(self, color):
        """Draws a filled cell"""
        pygame.draw.rect(self.screen, color, self.inner_rect)

    def draw_border(self, color):
        """Draws a border of a cell"""
        pygame.draw.rect(self.screen, color, self.rect, self.border)

    def draw_dot(self, color):
        """Draws a dot inside the cell"""
        pygame.draw.circle(self.screen, color,
                           (self.inner_x + self.inner_size // 2, self.inner_y + self.inner_size // 2),
                           self.inner_size // 10)

    def draw_number(self):
        """Draws a number inside the cell"""
        if self.number is not None and not self.number == "0":
            font = pygame.font.SysFont("Corbel", self.size - 5)
            text_surface = font.render(self.number, True, BLACK)

            if len(self.number) == 2:
                self.screen.blit(text_surface, (self.inner_rect.x + 2, self.inner_rect.y + 2))
            elif len(self.number) == 1:
                self.screen.blit(text_surface, (self.inner_rect.x + 5, self.inner_rect.y + 2))

    def is_in_area(self, mouse_pos):
        """Returns boolean value whether the cursor is inside the area of the cell"""
        return self.inner_rect.collidepoint(mouse_pos)


class MirrorCell:
    last_size = None

    def __init__(self):
        self.number = None
        self.is_filled = False
        self.has_dot = False

    def update(self, value):
        if type(value) is int:
            self.number = value
        elif value == "fill":
            self.is_filled = True
        elif value == "dot":
            self.has_dot = True
        else:
            pass


class Grid:
    def __init__(self, screen, rows, columns):
        self.rows = rows
        self.columns = columns
        self.screen = screen

    def mirror_grid(self):
        """Mirrors the grid with values only"""
        return [[MirrorCell() for _ in range(self.rows)] for _ in range(self.columns)]

    def init_grid(self, mirror_grid):
        """Creates a 5x5 2D list"""
        outer_border = Cell.init_size // 10
        grid = []

        for i in range(self.columns):
            row = []
            for j in range(self.rows):
                cell = Cell(self.screen,
                            CENTER[0] + i * (Cell.init_size - outer_border),
                            CENTER[1] + j * (Cell.init_size - outer_border),
                            Cell.init_size,
                            mirror_grid[i][j].is_filled,
                            mirror_grid[i][j].has_dot)
                row.append(cell)
            grid.append(row)

        return grid

    def init_left_grid(self, mirror):
        outer_border = Cell.init_size // 10
        grid = []

        for i in range(self.columns):
            row = []
            for j in range(self.rows):
                cell = Cell(self.screen,
                            CENTER[0] - (Cell.init_size - outer_border) - i * (Cell.init_size - outer_border),
                            CENTER[1] + j * (Cell.init_size - outer_border),
                            Cell.init_size,
                            number=mirror[i][j].number)
                row.append(cell)
            grid.append(row)

        return grid

    def init_top_grid(self, mirror):
        outer_border = Cell.init_size // 10
        grid = []

        for i in range(self.columns):
            row = []
            for j in range(self.rows):
                cell = Cell(self.screen,
                            CENTER[0] + i * (Cell.init_size - outer_border),
                            CENTER[1] - (Cell.init_size - outer_border) - j * (Cell.init_size - outer_border),
                            Cell.init_size,
                            number=mirror[i][j].number)
                row.append(cell)
            grid.append(row)

        return grid

    def draw_grid(self, grid):
        """Draws grid"""
        [cell.draw_border(BLACK) for row in grid for cell in row]

    def erase_grid(self, input_grid):
        """Erases grid"""
        [cell.draw_border(WHITE) for row in input_grid for cell in row]

    def init_left_nums(self, input_grid):
        numbers = set_left_nums()
        for i, row in enumerate(input_grid):
            for j, cell in enumerate(row):
                cell.number = numbers[j][i]

    def init_top_nums(self, input_grid):
        numbers = set_top_nums()
        for row, column in zip(input_grid, numbers):
            for cell, number in zip(row, column):
                cell.number = number

    def draw_numbers(self, grid):
        [cell.draw_number() for row in grid for cell in row]

    def erase_numbers(self, screen, grid):
        [pygame.draw.rect(screen, WHITE, cell.rect) for row in grid for cell in row]


def set_top_nums():
    """Sets top numbers"""
    top_nums = [
        [6, 0, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [2, 9, 0, 0, 0],
        [7, 2, 4, 0, 0],
        [2, 4, 2, 2, 2],
        [5, 3, 2, 0, 0],
        [3, 3, 2, 3, 0],
        [6, 1, 2, 4, 0],
        [2, 8, 2, 0, 0],
        [5, 2, 0, 0, 0],
        [3, 4, 0, 0, 0],
        [1, 5, 1, 0, 0],
        [5, 2, 0, 0, 0],
        [2, 4, 0, 0, 0],
        [7, 1, 0, 0, 0],
        [2, 5, 0, 0, 0],
        [2, 4, 2, 0, 0],
        [9, 5, 1, 0, 0],
        [2, 6, 4, 0, 0],
        [3, 7, 1, 1, 0],
        [2, 5, 1, 3, 1],
        [8, 2, 0, 0, 0],
        [2, 4, 1, 0, 0],
        [8, 0, 0, 0, 0],
        [7, 0, 0, 0, 0],
        [3, 4, 0, 0, 0],
        [7, 0, 0, 0, 0],
        [6, 0, 0, 0, 0],
        [1, 3, 0, 0, 0],
        [3, 0, 0, 0, 0],
    ]

    return top_nums


def set_left_nums():
    left_nums = [
        [1, 2, 0, 0, 0, 0, 0, 0],
        [3, 2, 0, 0, 0, 0, 0, 0],
        [6, 1, 0, 0, 0, 0, 0, 0],
        [5, 1, 2, 0, 0, 0, 0, 0],
        [2, 7, 2, 5, 0, 0, 0, 0],
        [9, 17, 0, 0, 0, 0, 0, 0],
        [6, 1, 3, 1, 2, 2, 2, 2],
        [7, 1, 1, 1, 3, 2, 2, 5],
        [1, 2, 4, 1, 3, 2, 1, 6],
        [3, 2, 1, 2, 1, 2, 5, 3],
        [4, 1, 1, 2, 3, 5, 0, 0],
        [8, 5, 5, 1, 0, 0, 0, 0],
        [9, 6, 1, 1, 0, 0, 0, 0],
        [1, 2, 7, 5, 1, 0, 0, 0],
        [1, 2, 2, 3, 1, 0, 0, 0],
        [4, 5, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 3, 0, 0, 0, 0],
        [1, 1, 2, 2, 0, 0, 0, 0],
        [1, 2, 2, 2, 0, 0, 0, 0],
        [1, 2, 2, 2, 0, 0, 0, 0],
    ]

    return left_nums
