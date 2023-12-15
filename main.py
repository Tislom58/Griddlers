import pygame

pygame.init()

# Set window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CENTER = (WIDTH // 2, HEIGHT // 2)
pygame.display.set_caption("Griddles")

# Color presets
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)


class Cell:
    side = 20
    width = 2
    is_filled = False

    def __init__(self, x, y):
        self.coordinates = x, y

    def draw_cell(self):
        pygame.draw.rect(WIN, WHITE, (*self.coordinates, self.side, self.side), self.width)

    def fill_cell(self):
        pygame.draw.rect(WIN, WHITE,
                         (self.coordinates[0] + (self.width + 2), self.coordinates[1] + (self.width + 2), self.side
                          - (2 * (self.width + 2)), self.side - (2 * (self.width + 2))))
        self.is_filled = True

    def empty_cell(self):
        pygame.draw.rect(WIN, BLACK,
                         (self.coordinates[0] + (self.width + 2), self.coordinates[1] + (self.width + 2), self.side
                          - (2 * (self.width + 2)), self.side - (2 * (self.width + 2))))
        self.is_filled = False

    def hover_cell(self):
        pygame.draw.rect(WIN, BLUE,
                         (self.coordinates[0] + (self.width + 2), self.coordinates[1] + (self.width + 2), self.side
                          - (2 * (self.width + 2)), self.side - (2 * (self.width + 2))))

    def clickable_area(self):
        clickable_area = *self.coordinates, self.coordinates[0] + self.side, self.coordinates[1] + self.side
        return clickable_area

    def hover_area(self):
        hover_area = *self.coordinates, self.side, self.side
        return hover_area


def main():
    run = True
    clock = pygame.time.Clock()

    box = Cell(*CENTER)
    box.draw_cell()
    cell_size = pygame.Rect(*box.hover_area())

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Get the position of the click
                x, y = event.pos

                # Check if the click is within the clickable area
                if (box.clickable_area()[0] <= x <= box.clickable_area()[2] and box.clickable_area()[1]
                        <= y <= box.clickable_area()[3]):
                    if event.button == 1:  # Left click
                        print("Left click detected at position", event.pos)
                        box.fill_cell()
                    if event.button == 3:  # Right click
                        print("Right click detected at position", event.pos)
                        box.empty_cell()

        if not box.is_filled:
            if cell_size.collidepoint(pygame.mouse.get_pos()):
                box.hover_cell()
            else:
                box.empty_cell()

        pygame.display.update()

    pygame.quit()


main()
