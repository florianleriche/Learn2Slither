class QLearning:
    def __init__(self):
        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.95

    def get_q_value(self, state, action):

        if state not in self.q_table:
            self.q_table[state] = {}

        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0

        return self.q_table[state][action]

    def update(
        
        self,
        state,
        action,
        reward,
        next_state,
        actions
    ):
        current_q = self.get_q_value(
            state,
            action
        )

        if next_state == "TERMINAL":
            max_next_q = 0

        else:
            max_next_q = max(
                self.get_q_value(
                    next_state,
                    future_action
                )
                for future_action in actions
            )

        new_q = (
            current_q
            + self.alpha * (
                reward
                + self.gamma * max_next_q
                - current_q
            )
        )

        self.q_table[state][action] = new_q

    def save(self, filename):
        import pickle

        with open(filename, "wb") as file:
            pickle.dump(
                self.q_table,
                file
        )


    def load(self, filename):
        import pickle

        with open(filename, "rb") as file:
            self.q_table = pickle.load(
                file
            )