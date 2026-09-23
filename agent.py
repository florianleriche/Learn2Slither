import random

from qlearning import QLearning


class Agent:

    ACTIONS = [
        "UP",
        "LEFT",
        "DOWN",
        "RIGHT"
    ]

    def __init__(self):
        self.qlearning = QLearning()

        self.epsilon = 0.9
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.008

    def choose_action(self, state):

        import random

        r = random.random()

        #print("RANDOM =", r)
        #print("EPSILON =", self.epsilon)

        if r < self.epsilon:
            action = random.choice(self.ACTIONS)

            print("EXPLORING :", action)

            return action

        best_action = self.ACTIONS[0]
        best_q = float("-inf")

        for action in self.ACTIONS:

            q = self.qlearning.get_q_value(
                state,
                action
            )

            print(action, "=", q)

            if q > best_q:
                best_q = q
                best_action = action

        #print("EXPLOITING :", best_action)

        return best_action

    def learn(
        self,
        state,
        action,
        reward,
        next_state
    ):
        self.qlearning.update(
            state,
            action,
            reward,
            next_state,
            self.ACTIONS
        )

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def print_q_values(self, state):

        #print("\nQ VALUES")

        for action in self.ACTIONS:

            q = self.qlearning.get_q_value(
                state,
                action
            )

            print(
                f"{action:<6} : {q:.3f}"
            )

        print()