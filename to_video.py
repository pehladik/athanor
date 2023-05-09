import json
import argparse
import random
import time
import curses

def main(partition):
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()

    random.seed(None)

    f = open(partition, "r")
    data = json.load(f)

    start_time = time.time()
    txt = ""
    for p in data['partition']:
        rel_pos = 0
        txt = p['paragraphe']['texte'] + "\n"
        stdscr.clear()
        try:
            stdscr.addstr(0, 0, txt)
        except curses.error:
            pass
        stdscr.refresh()

        cstart = '\033[0;31m'
        cend = '\033[0m'
        for d in p['paragraphe']['didascalies']:
            next = start_time + d['debut']
            idx1 = rel_pos + int(d['position'])
            sword = int(d['taille'])
            while (True):
                if (time.time() > next):
                    break
            stdscr.clear()
            stdscr.addstr(txt[:idx1])
            stdscr.addstr(txt[idx1:idx1+sword:], curses.A_STANDOUT)
            stdscr.addstr(txt[idx1+sword:])
            stdscr.refresh()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'PyEagle',
                    description = 'Generate a video file from a partition')
    parser.add_argument("-i", "--partition", help="partition name (with extension)", nargs='?', const='work', default='work')
    args = parser.parse_args()
    main(args.partition)