class Snake:
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
        self.should_grow = False

    def get_head(self):
        return self.body[0]

    def move(self, direction):
        head_x, head_y = self.get_head()

        if direction == "UP":
            new_head = (head_x, head_y - 1)

        elif direction == "DOWN":
            new_head = (head_x, head_y + 1)

        elif direction == "LEFT":
            new_head = (head_x - 1, head_y)

        elif direction == "RIGHT":
            new_head = (head_x + 1, head_y)

        self.direction = direction

        self.body.insert(0, new_head)

        if self.should_grow:
            self.should_grow = False
        else:
            self.body.pop()

        print("REQUESTED:", direction)
        print("HEAD:", self.get_head())

    def grow(self):
        self.should_grow = True

    def shrink(self):
        if len(self.body) > 0:
            self.body.pop()