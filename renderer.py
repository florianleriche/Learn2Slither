import pygame


class Renderer:

    CELL_SIZE = 50

    def __init__(self, width, height):

        pygame.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode(
            (
                width * self.CELL_SIZE,
                height * self.CELL_SIZE
            )
        )

        pygame.display.set_caption(
            "Learn2Slither"
        )

        self.vision_only = False

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_v:
                    self.vision_only = not self.vision_only


        return True

    def draw(self, board):

        if self.vision_only:
            self.draw_vision(board)
        else:
            self.draw_map(board)

    def draw_map(self, board):

        self.screen.fill((30, 30, 30))

        self.draw_board(board)

        pygame.display.flip()

    def draw_vision(self, board):

        self.screen.fill((0, 0, 0))

        head_x, head_y = board.snake.get_head()

        # Affiche uniquement la ligne
        for x in range(board.width):

            self.draw_cell(
                board,
                x,
                head_y
            )

        # Affiche uniquement la colonne
        for y in range(board.height):

            self.draw_cell(
                board,
                head_x,
                y
            )

        pygame.display.flip()

    def draw_board(self, board):

        for y in range(board.height):

            for x in range(board.width):

                self.draw_cell(
                    board,
                    x,
                    y
                )

    def draw_cell(
        self,
        board,
        x,
        y
    ):

        color = (60, 60, 60)

        # serpent
        if (x, y) in board.snake.body:

            color = (0, 0, 255)

        # pommes vertes
        if (x, y) in board.green_apples:

            color = (0, 255, 0)

        # pomme rouge
        if (x, y) == board.red_apple:

            color = (255, 0, 0)

        # tête du serpent
        if (x, y) == board.snake.get_head():

            color = (0, 200, 255)

        pygame.draw.rect(
            self.screen,
            color,
            (
                x * self.CELL_SIZE,
                y * self.CELL_SIZE,
                self.CELL_SIZE,
                self.CELL_SIZE
            )
        )

        pygame.draw.rect(
            self.screen,
            (20, 20, 20),
            (
                x * self.CELL_SIZE,
                y * self.CELL_SIZE,
                self.CELL_SIZE,
                self.CELL_SIZE
            ),
            1
        )