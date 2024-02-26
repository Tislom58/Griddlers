import pygame
import random

pygame.init()

# Next steps
# TODO: Create parent class
# TODO: Fix toggling numbers and fills

# Set window
WIDTH, HEIGHT = 1200, 950
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CENTER = [WIDTH // 2, HEIGHT // 2]

# Title
pygame.display.set_caption("Griddles")

# RGB color presets
BLACK = (47, 45, 52)
WHITE = (224, 214, 176)
BLUE = (100, 149, 237)


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:
    init_size = 20
    gap = 2

    def __init__(self, x, y, size, fill=False, dot=False, number=None):

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
        self.number = number

    def draw(self, color):
        """Draws a filled cell"""
        pygame.draw.rect(WINDOW, color, self.inner_rect)

    def draw_border(self, color):
        """Draws a border of a cell"""
        pygame.draw.rect(WINDOW, color, self.rect, self.border)

    def draw_dot(self, color):
        """Draws a dot inside the cell"""
        pygame.draw.circle(WINDOW, color, (self.inner_x + self.inner_size // 2, self.inner_y + self.inner_size // 2), self.inner_size // 10)

    def draw_number(self):
        """Draws a number inside the cell"""
        if self.number is not None:
            font = pygame.font.SysFont("Corbel", self.size - 5)
            text_surface = font.render(self.number, True, BLACK)

            if len(self.number) == 2:
                WINDOW.blit(text_surface, (self.inner_rect.x + 2, self.inner_rect.y + 2))
            elif len(self.number) == 1:
                WINDOW.blit(text_surface, (self.inner_rect.x + 5, self.inner_rect.y + 2))

    def is_in_area(self, mouse_pos):
        """Returns boolean value whether the cursor is inside the area of the cell"""
        return self.inner_rect.collidepoint(mouse_pos)


class MirrorCell:
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


class Button:
    pressed = True
    unpressed = False
    refresh = True

    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.smallfont = pygame.font.SysFont('Corbel', 50)
        self.is_pressed = False

    def draw(self):
        """Draws the button"""
        pygame.draw.rect(WINDOW, BLACK, (self.x, self.y, self.width, self.height))
        if self.is_pressed:
            pygame.draw.rect(WINDOW, WHITE, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 3)
        rendertext = self.smallfont.render(self.text, True, BLUE)
        WINDOW.blit(rendertext, (self.x + 5, self.y + 6))

    def set_state(self, pressed):
        """Sets the button state"""
        self.is_pressed = True if pressed else False

    def is_in_area(self, x, y):
        """Checks if the area is clicked"""
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def mirror_grid(self):
        """Mirrors the grid with values only"""
        return [[MirrorCell() for j in range(self.rows)] for i in range(self.columns)]

    def init_grid(self, mirror_grid):
        """Creates a 5x5 2D list"""
        outer_border = Cell.init_size // 10
        grid = []

        for i in range(self.columns):
            row = []
            for j in range(self.rows):
                cell = Cell(CENTER[0] + i * (Cell.init_size - outer_border),
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
                cell = Cell(CENTER[0] - (Cell.init_size - outer_border) - i * (Cell.init_size - outer_border),
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
                cell = Cell(CENTER[0] + i * (Cell.init_size - outer_border),
                            CENTER[1] - (Cell.init_size - outer_border) - j * (Cell.init_size - outer_border),
                            Cell.init_size,
                            number=mirror[i][j].number)
                row.append(cell)
            grid.append(row)

        return grid


def hover(instance):
    """Renders hover effect on cells"""
    if not instance.is_filled:
        if instance.rect.collidepoint(pygame.mouse.get_pos()):
            instance.draw(BLUE)
        else:
            instance.draw(WHITE)
    elif instance.is_filled and not instance.has_dot:
        instance.draw(BLACK)
    elif instance.is_filled and instance.has_dot:
        instance.draw_dot(BLACK)


def button_is_pressed(event, pos, instance):
    """Checks if button is pressed"""
    return instance.is_in_area(*pos) and event.button == 1


def render_button(instance, refresh=False):
    """Keeps buttons rendered"""
    instance.draw()
    if refresh:
        instance.set_state(Button.unpressed)


def button_handler(event, pos, buttons):
    """Handles button clicks"""
    if button_is_pressed(event, pos, buttons[0]):  # Press + button
        buttons[0].set_state(Button.pressed)
        Cell.init_size += 10
    if button_is_pressed(event, pos, buttons[1]):  # Press - button
        buttons[1].set_state(Button.pressed)
        Cell.init_size -= 10
    if button_is_pressed(event, pos, buttons[2]) and not buttons[2].is_pressed:
        buttons[2].set_state(Button.pressed)
        buttons[3].set_state(Button.unpressed)
        buttons[4].set_state(Button.unpressed)
    elif button_is_pressed(event, pos, buttons[2]) and buttons[2].is_pressed:
        buttons[2].set_state(Button.unpressed)
    if button_is_pressed(event, pos, buttons[3]) and not buttons[3].is_pressed:
        buttons[3].set_state(Button.pressed)
        buttons[2].set_state(Button.unpressed)
        buttons[4].set_state(Button.unpressed)
    elif button_is_pressed(event, pos, buttons[3]) and buttons[3].is_pressed:
        buttons[3].set_state(Button.unpressed)
    if button_is_pressed(event, pos, buttons[4]) and not buttons[4].is_pressed:
        buttons[4].set_state(Button.pressed)
        buttons[2].set_state(Button.unpressed)
        buttons[3].set_state(Button.unpressed)
    elif button_is_pressed(event, pos, buttons[4]) and buttons[4].is_pressed:
        buttons[4].set_state(Button.unpressed)


def cell_events(event, pos, instance):
    """Event handler for clicks on the cell"""

    if not instance.is_filled:
        if instance.is_in_area(pos) and event.button == 1:
            # instance.draw(SKETCHBOOK_WHITE)
            instance.is_filled = True

    elif instance.is_filled and not instance.has_dot:
        if instance.is_in_area(pos) and event.button == 1:
            instance.draw_dot(BLACK)
            instance.has_dot = True

    if instance.is_in_area(pos) and event.button == 3:
        instance.draw(WHITE)
        instance.is_filled = False
        instance.has_dot = False


def automatic(instance):
    state = random.randint(1, 3)
    if state == 1:
        instance.draw(BLACK)
    elif state == 2:
        instance.draw(WHITE)
    else:
        instance.draw_dot(BLACK)


def draw_grid(grid):
    """Draws grid"""
    [cell.draw_border(BLACK) for row in grid for cell in row]


def erase_grid(grid):
    """Erases grid"""
    [cell.draw_border(WHITE) for row in grid for cell in row]


def init_numbers(grid):
    for row in grid:
        for cell in row:
            number = str(random.randint(1, 99))
            cell.number = number


def draw_numbers(grid):
    [cell.draw_number() for row in grid for cell in row]


def erase_numbers(grid):
    [pygame.draw.rect(WINDOW, WHITE, cell.rect) for row in grid for cell in row]


def pan():
    """Pans the screen"""
    movement = pygame.mouse.get_rel()
    # print(CENTER, movement)
    if -100 < movement[0] < 100 and -100 < movement[1] < 100:
        CENTER[0] += movement[0]
        CENTER[1] += movement[1]


def main():
    """Executed code"""

    pan_active = False
    run = True
    clock = pygame.time.Clock()

    # Initialization of static instances
    plus_button = Button(20, 20, 50, 50, " +")
    minus_button = Button(20, 90, 50, 50, " -")
    manual_button = Button(20, 160, 200, 50, "Manual")
    automatic_button = Button(20, 230, 200, 50, "Automatic")
    pan_button = Button(20, 300, 80, 50, "Pan")

    buttons = (plus_button, minus_button, manual_button, automatic_button, pan_button)

    grid = Grid(20, 20)
    top_nums = Grid(3, 20)
    left_nums = Grid(20, 3)
    mirror_grid = grid.mirror_grid()
    top_numbers_mirror = top_nums.mirror_grid()
    left_numbers_mirror = left_nums.mirror_grid()
    init_numbers(top_numbers_mirror)
    init_numbers(left_numbers_mirror)

    WINDOW.fill(WHITE)

    while run:
        clock.tick(60)

        # Initialization of dynamic instances
        outer_cells = grid.init_grid(mirror_grid)
        top_num_cells = top_nums.init_top_grid(top_numbers_mirror)
        left_num_cells = left_nums.init_left_grid(left_numbers_mirror)

        # Draw each instance
        draw_grid(outer_cells)
        draw_grid(top_num_cells)
        draw_grid(left_num_cells)
        draw_numbers(left_num_cells)
        draw_numbers(top_num_cells)

        # Update buttons
        render_button(plus_button, Button.refresh)
        render_button(minus_button, Button.refresh)
        render_button(manual_button)
        render_button(automatic_button)
        render_button(pan_button)

        for row_index, row in enumerate(outer_cells):
            for cell_index, cell in enumerate(row):
                if manual_button.is_pressed:
                    hover(cell)
                elif automatic_button.is_pressed:
                    automatic(cell)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                cursor_pos = event.pos

                if pan_button.is_pressed and event.button == 1:
                    pan_active = True

                # Cell click handler
                for row in outer_cells:
                    for cell in row:
                        if manual_button.is_pressed:
                            cell_events(event, cursor_pos, cell)

                button_handler(event, cursor_pos, buttons)

            if event.type == pygame.MOUSEBUTTONUP:
                if pan_button.is_pressed and event.button == 1:
                    pan_active = False

            if event.type == pygame.MOUSEMOTION and pan_button.is_pressed and pan_active:
                pan()

        # Load frame
        pygame.display.update()

        # Safely destruct the updating drawings
        erase_grid(outer_cells)
        erase_grid(left_num_cells)
        erase_grid(top_num_cells)
        erase_numbers(left_num_cells)
        erase_numbers(top_num_cells)

        for row, mRow in zip(outer_cells, mirror_grid):
            for cell, mCell in zip(row, mRow):
                if cell.is_filled:
                    mCell.update("fill")
                    cell.draw(WHITE)
                else:
                    mCell.is_filled = False
                if cell.has_dot:
                    mCell.update("dot")
                    cell.draw(WHITE)
                else:
                    mCell.has_dot = False

        # Reset frame
        # WINDOW.fill(BLACK)

    pygame.quit()


main()
