import random

from snake import Snake


class Board:
    def __init__(
        self,
        width=10,
        height=10
    ):
        self.width = width
        self.height = height

        self.snake = self.create_random_snake()

        self.green_apples = []
        self.red_apple = None

        self.spawn_apples()

    def get_random_empty_cell(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            position = (x, y)

            if position in self.snake.body:
                continue

            if position in self.green_apples:
                continue

            if position == self.red_apple:
                continue

            return position

    def spawn_apples(self):
        self.green_apples = [
            self.get_random_empty_cell(),
            self.get_random_empty_cell()
        ]

        self.red_apple = self.get_random_empty_cell()

    def check_wall_collision(self):
        x, y = self.snake.get_head()

        return (
            x < 0
            or x >= self.width
            or y < 0
            or y >= self.height
        )

    def check_self_collision(self):
        head = self.snake.get_head()

        return head in self.snake.body[1:]

    def check_apples(self):
        head = self.snake.get_head()

        for apple in self.green_apples[:]:
            if head == apple:

                print("GREEN APPLE EATEN")

                self.snake.grow()

                print(
                    "Current length:",
                    len(self.snake.body)
                )

                self.green_apples.remove(apple)

                self.green_apples.append(
                    self.get_random_empty_cell()
                )

                return 200

        if head == self.red_apple:
            print("RED APPLE EATEN")
            self.snake.shrink()

            self.red_apple = self.get_random_empty_cell()
            print(
                    "Current length:",
                    len(self.snake.body)
                )

            return -25

        return -1.5

    def look_direction(self, dx, dy):
        head_x, head_y = self.snake.get_head()

        x = head_x
        y = head_y

        distance = 0

        while True:
            x += dx
            y += dy
            distance += 1

            if (
                x < 0
                or x >= self.width
                or y < 0
                or y >= self.height
            ):
                return (1, 0, 0, distance)

            if (x, y) in self.snake.body[1:]:
                return (1, 0, 0, distance)

            if (x, y) in self.green_apples:
                return (0, 1, 0, distance)

            if (x, y) == self.red_apple:
                return (0, 0, 1, distance)

    def get_state(self):

        up = self.look_direction(0, -1)
        left = self.look_direction(-1, 0)
        down = self.look_direction(0, 1)
        right = self.look_direction(1, 0)

        return (
            *up,
            *left,
            *down,
            *right
        )


    def update(self, direction):
        self.snake.move(direction)

        if self.check_wall_collision():
            return None, -200, True

        if self.check_self_collision():
            return None, -300, True

        reward = self.check_apples()

        if len(self.snake.body) == 0:
            return None, -200, True

        next_state = self.get_state()

        return next_state, reward, False

    def draw_terminal(self):
        grid = [
            ["." for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for x, y in self.green_apples:
            grid[y][x] = "G"

        red_x, red_y = self.red_apple
        grid[red_y][red_x] = "R"

        for x, y in self.snake.body:
            if (
                0 <= x < self.width
                and 0 <= y < self.height
            ):
                grid[y][x] = "S"

        head_x, head_y = self.snake.get_head()

        if (
            0 <= head_x < self.width
            and 0 <= head_y < self.height
        ):
            grid[head_y][head_x] = "H"

        print(f"\nLength: {len(self.snake.body)}")

        for row in grid:
            print(" ".join(row))

        print()

    def create_random_snake(self):

        orientation = random.choice(
            ["RIGHT", "LEFT", "UP", "DOWN"]
        )

        if orientation == "RIGHT":

            x = random.randint(2, self.width - 1)
            y = random.randint(0, self.height - 1)

            body = [
                (x, y),
                (x - 1, y),
                (x - 2, y)
            ]

        elif orientation == "LEFT":

            x = random.randint(
                0,
                self.width - 3
            )

            y = random.randint(
                0,
                self.height - 1
            )

            body = [
                (x, y),
                (x + 1, y),
                (x + 2, y)
            ]

        elif orientation == "DOWN":

            x = random.randint(
                0,
                self.width - 1
            )

            y = random.randint(
                2,
                self.height - 1
            )

            body = [
                (x, y),
                (x, y - 1),
                (x, y - 2)
            ]

        else:  # UP

            x = random.randint(
                0,
                self.width - 1
            )

            y = random.randint(
                0,
                self.height - 3
            )

            body = [
                (x, y),
                (x, y + 1),
                (x, y + 2)
            ]
        
        return Snake(
            body,
            orientation
        )

    def look_direction_full(self, dx, dy):
        head_x, head_y = self.snake.get_head()

        x = head_x
        y = head_y

        vision = []

        while True:

            x += dx
            y += dy

            if (
                x < 0
                or x >= self.width
                or y < 0
                or y >= self.height
            ):
                vision.append("W")
                break

            elif (x, y) in self.snake.body[1:]:
                vision.append("S")

            elif (x, y) in self.green_apples:
                vision.append("G")

            elif (x, y) == self.red_apple:
                vision.append("R")

            else:
                vision.append("0")

        return vision

    def get_vision(self):
        return (
            self.look_direction_full(0, -1),   # UP
            self.look_direction_full(-1, 0),   # LEFT
            self.look_direction_full(0, 1),    # DOWN
            self.look_direction_full(1, 0)     # RIGHT
        )