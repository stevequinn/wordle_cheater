#! /usr/bin/python3

import getch
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel

console = Console()

def log(*args, **kwargs):
    console.print(*args, **kwargs)

def generate_table(rows) -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("Choice")
    table.add_column("Result")

    for row in rows:
        table.add_row(
            f"{row[0]}", f"{row[1]}"
        )
    return table

def get_possibles(options, state, word):
    possibles = []

    for oidx, option in enumerate(options):
        if not option:
            continue

        opt = option.lower()

        possible = False
        for sidx, s in enumerate(state):
            if s == 1:
                if opt[sidx] == word[sidx]:
                    possible = True
                if opt[sidx] != word[sidx]:
                    possible = False
                    break
            if s == 2:
                if word[sidx] in opt:
                    possible = True
                    if opt.index(word[sidx]) == sidx:
                        possible = False
                        break
                if word[sidx] not in opt:
                    possible = False
                    break
            if s == 0:
                if word[sidx] in opt:
                    possible = False
                    break

            if opt in possibles:
                possible = False
                break

        if possible:
            possibles.append(opt)

    return possibles

def gen_opts(word_hist, state_hist):
    # base_list = [
    #     'first',
    #     'secon',
    #     'third',
    #     'forth'
    # ]
    # options = base_list

    with open('./words5.txt', 'r') as my_file:
        data = my_file.read()
        options = data.replace('\n', ' ').split(' ')
        opts = []

        for widx, word in enumerate(word_hist):

            if len(opts) == 0:
                # Only filter if there is something to filter.
                # If no letter matches where found then get_possibles will return an empty list.
                opts = options

            opts = get_possibles(opts, state_hist[widx], word)

        return opts


def get_key(key):
    if key == '\033':
        getch.getch() # skip the [
        key = getch.getch()
    return key

def get_result(state):
    emoji_exists = ':yellow_square:'
    emoji_yes = ':green_square:'
    emoji_no = ':white_large_square:'
    output = []

    for s in state:
        if s == 1:
            output.append(f'[{emoji_yes}]')
        if s == 2:
            output.append(f'[{emoji_exists}]')
        if s == 0:
            output.append(f'[{emoji_no}]')

    while len(output) < 5:
        output.append('[  ]')

    return output

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    return layout

def main():
    log('Wordle Solver', style='bold green')


    up = 'A'
    down = 'B'
    right = 'C'
    left = 'D'

    letters = 5
    turns = 6
    tpl_empty = '[  ] [  ] [  ] [  ] [  ]'

    rows = []
    rows.append(
        ("", tpl_empty, "")
    )
    table = generate_table(rows)

    word = [] # []
    state = [] # []
    word_hist = [] # [[]]
    state_hist = [] # [[]]
    opts = []

    layout = make_layout()

    with Live(layout, refresh_per_second=10, vertical_overflow='visible') as live:
        while True:

            layout['side'].update(Panel(generate_table(rows)))
            layout['body'].update(Panel(" ".join(opts)))
            time.sleep(0.5)

            if len(word) == 5:

                while len(state) < 5:
                    key = get_key(getch.getch())
                    # deal with setting state
                    if key == up:
                        state.append(1) # green
                    elif key == down:
                        state.append(2) # yellow
                    elif key == right:
                        state.append(0) # white

                    rows[-1] = ("".join(word), " ".join(get_result(state)))
                    layout['side'].update(Panel(generate_table(rows)))
                    layout['body'].update(Panel(" ".join(opts)))
                    time.sleep(0.5)

                word_hist.append(word.copy())
                state_hist.append(state.copy())

                word.clear()
                state.clear()

                # append new row
                opts = gen_opts(word_hist, state_hist)
                rows.append(
                    ("", tpl_empty)
                )
            else:
                key = get_key(getch.getch())
                if key not in [up, down, right, left]:
                    word.append(key)
                    rows[-1] = ("".join(word), tpl_empty)


    # while turns > 0:
    #     line = list(input("Word: "))
    #     choices.append(line)
    #     turns -= 1


if __name__ == '__main__':
    main()
