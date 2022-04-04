competition_type = 'playoff'

board_size = 19
komi = 5.5

import os

players = {
    'gnugo': Player('/usr/games/gnugo --mode=gtp --chinese-rules --level=9'),
    'hugging': Player('docker run --rm -i ' + os.getenv('HUGGING_GO_SHA'))
}

matchups = {
    Matchup('hugging', 'gnugo', number_of_games=100, alternating=True)
}
