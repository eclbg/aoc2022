ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissor'

WIN = 'win'
DRAW = 'draw'
LOSE = 'lose'

PLAYS = [ROCK, PAPER, SCISSORS]

PLAY_SCORES = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}

RESULT_SCORES = {
    WIN: 6,
    DRAW: 3,
    LOSE: 0,
}

WIN_SCENARIOS = [(SCISSORS, ROCK), (ROCK, PAPER), (PAPER, SCISSORS)]


def parse_play(item):
    if item in ('A', 'X'):
        return ROCK
    elif item in ('B', 'Y'):
        return PAPER
    elif item in ('C', 'Z'):
        return SCISSORS


def parse_result(item):
    if item in ('X'):
        return LOSE
    elif item in ('Y'):
        return DRAW
    elif item in ('Z'):
        return WIN


def compute_game_result(play1, play2):
    if play1 == play2:
        return DRAW
    elif (play1, play2) in WIN_SCENARIOS:
        return WIN
    else:
        return LOSE


def part1():
    def parse_row(row):
        items = row.split()
        play1 = parse_play(items[0])
        play2 = parse_play(items[1])
        return play1, play2

    def get_plays(row):
        play1, play2 = parse_row(row)
        return play1, play2

    with open('input.txt') as f:
        total_score = 0
        for row in f:
            row = row.strip()
            play1, play2 = get_plays(row)
            play_score = PLAY_SCORES[play2]
            score = (
                play_score + RESULT_SCORES[compute_game_result(play1, play2)]
            )
            total_score += score
    return total_score


def part2():
    def parse_row(row):
        items = row.split()
        elf_play = parse_play(items[0])
        result = parse_result(items[1])
        return elf_play, result

    def get_elf_play_and_result(row):
        elf_play, result = parse_row(row)
        return elf_play, result

    def compute_play(elf_play, result):
        if result == DRAW:
            play = elf_play
        elif result == WIN:
            play = PLAYS[(PLAYS.index(elf_play) + 1) % 3]
        elif result == LOSE:
            play = PLAYS[(PLAYS.index(elf_play) - 1) % 3]
        return play

    with open('input.txt') as f:
        total_score = 0
        for row in f:
            row = row.strip()
            play1, result = parse_row(row)
            play2 = compute_play(play1, result)

            play_score = PLAY_SCORES[play2]
            score = (
                play_score + RESULT_SCORES[result]
            )
            total_score += score
    return total_score


if __name__ == '__main__':
    print(part1())
    print(part2())
