import pickle


def save_model(q_table, filename):
    with open(filename, "wb") as file:
        pickle.dump(q_table, file)


def load_model(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)