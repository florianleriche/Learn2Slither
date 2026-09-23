import argparse
import time

from board import Board
from agent import Agent
try:
    from renderer import Renderer
except ImportError:
    Renderer = None


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--width",
        type=int,
        default=10
    )

    parser.add_argument(
        "--height",
        type=int,
        default=10
    )

    parser.add_argument(
        "--sessions",
        type=int,
        default=100
    )

    parser.add_argument(
        "--load",
        type=str,
        default=None
    )

    parser.add_argument(
        "--save",
        type=str,
        default=None
    )

    parser.add_argument(
        "--dontlearn",
        action="store_true"
    )

    parser.add_argument(
        "--visual",
        choices=["on", "off"],
        default="on"
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=0.05
    )

    args = parser.parse_args()

    agent = Agent()

    if args.load:
        print(
            f"Loading model: {args.load}"
        )

        agent.qlearning.load(
            args.load
        )

    if args.dontlearn:
        agent.epsilon = 0.01

    best_length_ever = 0
    best_moves_ever = 0

    renderer = None

    for session in range(args.sessions):

        board = Board(
            args.width,
            args.height
        )

        state = board.get_state()

        game_over = False
        moves = 0
        max_length = len(board.snake.body)

        if (
            args.visual == "on"
            and Renderer is not None
        ):
            renderer = Renderer(
                board.width,
                board.height
            )


        while not game_over:

            if renderer:

                if not renderer.handle_events():
                    print("Window closed")
                    return

                renderer.draw(board)

                time.sleep(args.speed)

            old_state = state

            action = agent.choose_action(
                old_state
            )

            next_state, reward, game_over = (
                board.update(action)
            )

            moves += 1

            max_length = max(
                max_length,
                len(board.snake.body)
            )

            if not args.dontlearn:

                if game_over:

                    agent.learn(
                        old_state,
                        action,
                        reward,
                        "TERMINAL"
                    )

                else:

                    agent.learn(
                        old_state,
                        action,
                        reward,
                        next_state
                    )

            if not game_over:
                state = next_state

        best_length_ever = max(
            best_length_ever,
            max_length
        )

        best_moves_ever = max(
            best_moves_ever,
            moves
        )

        if session % 100 == 0:

            print(
                f"Session {session + 1}"
            )

            print(
                f"Moves: {moves}"
            )

            print(
                f"Max length: {max_length}"
            )

            print(
                f"Epsilon: {agent.epsilon:.6f}"
            )

            print(
                "Known states:",
                len(agent.qlearning.q_table)
            )

            print("-" * 40)

    print()
    print("TRAINING FINISHED")

    print(
        "FINAL KNOWN STATES:",
        len(agent.qlearning.q_table)
    )

    print(
        "BEST LENGTH EVER:",
        best_length_ever
    )

    print(
        "BEST MOVES EVER:",
        best_moves_ever
    )

    if args.save:

        print(
            f"Saving model: {args.save}"
        )

        agent.qlearning.save(
            args.save
        )

    elif not args.load:

        default_name = (
            f"models/{args.sessions}sess.pkl"
        )

        print(
            f"Saving model: {default_name}"
        )

        agent.qlearning.save(
            default_name
        )


if __name__ == "__main__":
    main()