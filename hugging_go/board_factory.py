from collections import namedtuple

BoardSequence = namedtuple('BoardSequence', ['sequence', 'komi'])

class BoardFactory:
    def build(self, board_size, komi):
        assert board_size == 19, 'only 19×19 boards are supported'

        return BoardSequence(
            sequence=[],
            komi=komi
        )
