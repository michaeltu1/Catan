# TODO(mtu): figure out how imports work
from catan.config.Config import Config


class Board:

    def __init__(self, mode="standard"):
        """
        :param mode: determines the configuration of the game
        """
        self.config = Config().get_config(mode)

    def __str__(self):
        # TODO(mtu): print the board
        raise NotImplementedError


if __name__ == '__main__':
    b = Board()
    print(b)
