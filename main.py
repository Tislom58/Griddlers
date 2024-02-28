import pygame
import random
import grid

pygame.init()
clock = pygame.time.Clock()

# Next steps
# TODO: Proceed with the algorithm

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
        self.rect = pygame.Rect(x, y, width, height)

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

    def has_been_pressed(self, event, mouse_pos):
        """Returns boolean value whether the cursor is inside the area of the cell"""
        return self.rect.collidepoint(mouse_pos) and event.button == 1


def hover(instance):
    """Renders hover effect on cells"""
    if not instance.is_filled:
        if instance.inner_rect.collidepoint(pygame.mouse.get_pos()):
            instance.draw(BLUE)
        else:
            instance.draw(WHITE)
    elif instance.is_filled and not instance.has_dot:
        instance.draw(BLACK)
    elif instance.is_filled and instance.has_dot:
        instance.draw_dot(BLACK)


def render_button(instance, refresh=False):
    """Keeps buttons rendered"""
    instance.draw()
    if refresh:
        instance.set_state(Button.unpressed)


def button_handler(event, pos, buttons):
    """Handles button clicks"""
    if buttons[0].has_been_pressed(event, pos):  # Press + button
        buttons[0].set_state(Button.pressed)
        grid.Cell.init_size += 10
    if buttons[1].has_been_pressed(event, pos):  # Press - button
        buttons[1].set_state(Button.pressed)
        grid.Cell.init_size -= 10
    if buttons[2].has_been_pressed(event, pos) and not buttons[2].is_pressed:
        buttons[2].set_state(Button.pressed)
        buttons[3].set_state(Button.unpressed)
        buttons[4].set_state(Button.unpressed)
    elif buttons[2].has_been_pressed(event, pos) and buttons[2].is_pressed:
        buttons[2].set_state(Button.unpressed)
    if buttons[3].has_been_pressed(event, pos) and not buttons[3].is_pressed:
        buttons[3].set_state(Button.pressed)
        buttons[2].set_state(Button.unpressed)
        buttons[4].set_state(Button.unpressed)
    elif buttons[3].has_been_pressed(event, pos) and buttons[3].is_pressed:
        buttons[3].set_state(Button.unpressed)
    if buttons[4].has_been_pressed(event, pos) and not buttons[4].is_pressed:
        buttons[4].set_state(Button.pressed)
        buttons[2].set_state(Button.unpressed)
        buttons[3].set_state(Button.unpressed)
    elif buttons[4].has_been_pressed(event, pos) and buttons[4].is_pressed:
        buttons[4].set_state(Button.unpressed)

    for button in buttons:
        print(button.has_been_pressed(event, pos))


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


def pan():
    """Pans the screen"""
    movement = pygame.mouse.get_rel()
    # print(CENTER, movement)
    if -100 < movement[0] < 100 and -100 < movement[1] < 100:
        CENTER[0] += movement[0]
        CENTER[1] += movement[1]


def fps_counter():
    rect = pygame.Rect(WIDTH - 200, 50, 200, 50)
    pygame.draw.rect(WINDOW, WHITE, rect)
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont("Corbel", 50)
    fps_text = font.render(f"FPS: {fps}", True, BLACK)
    WINDOW.blit(fps_text, (WIDTH - 200, 50))


def main():
    """Executed code"""

    pan_active = False
    run = True

    grid.get_center(CENTER)

    # Initialization of static instances
    plus_button = Button(20, 20, 50, 50, " +")
    minus_button = Button(20, 90, 50, 50, " -")
    manual_button = Button(20, 160, 200, 50, "Manual")
    automatic_button = Button(20, 230, 200, 50, "Automatic")
    pan_button = Button(20, 300, 80, 50, "Pan")

    buttons = (plus_button, minus_button, manual_button, automatic_button, pan_button)

    rows = 20
    columns = 30

    current_grid = grid.Grid(WINDOW, rows, columns)
    top_nums = grid.Grid(WINDOW, 5, columns)
    left_nums = grid.Grid(WINDOW, rows, 8)
    mirror_grid = current_grid.mirror_grid()
    top_numbers_mirror = top_nums.mirror_grid()
    left_numbers_mirror = left_nums.mirror_grid()
    current_grid.init_top_nums(top_numbers_mirror)
    current_grid.init_left_nums(left_numbers_mirror)

    WINDOW.fill(WHITE)

    render_button(plus_button, Button.refresh)
    render_button(minus_button, Button.refresh)
    render_button(manual_button)
    render_button(automatic_button)
    render_button(pan_button)

    outer_cells = current_grid.init_grid(mirror_grid)
    top_num_cells = top_nums.init_top_grid(top_numbers_mirror)
    left_num_cells = left_nums.init_left_grid(left_numbers_mirror)

    while run:
        clock.tick(60)

        fps_counter()

        grid.get_center(CENTER)

        # Draw and initialize each instance upon made changes
        if grid.MirrorCell.last_size is None or not grid.MirrorCell.last_size == grid.Cell.init_size or pan_active:
            outer_cells = current_grid.init_grid(mirror_grid)
            top_num_cells = top_nums.init_top_grid(top_numbers_mirror)
            left_num_cells = left_nums.init_left_grid(left_numbers_mirror)

            current_grid.draw_grid(outer_cells)
            current_grid.draw_grid(top_num_cells)
            current_grid.draw_grid(left_num_cells)
            current_grid.draw_numbers(left_num_cells)
            current_grid.draw_numbers(top_num_cells)

        grid.MirrorCell.last_size = grid.Cell.init_size

        # Update buttons
        for button in buttons:
            # pygame.draw.rect(WINDOW, BLUE, button.rect)
            if button.is_pressed:
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

        if not pan_button.is_pressed:
            pan_active = False

        # Load frame
        pygame.display.update()

        # Safely destruct the updating drawings
        if grid.MirrorCell.last_size is None or not grid.MirrorCell.last_size == grid.Cell.init_size or pan_active:
            current_grid.erase_grid(outer_cells)
            current_grid.erase_grid(left_num_cells)
            current_grid.erase_grid(top_num_cells)
            current_grid.erase_numbers(WINDOW, left_num_cells)
            current_grid.erase_numbers(WINDOW, top_num_cells)

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
    pygame.quit()


main()
