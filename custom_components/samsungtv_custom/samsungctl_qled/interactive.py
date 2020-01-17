import curses


_mappings = [
    ["p",             "KEY_POWEROFF",      "P",         "Power off"],
    ["KEY_UP",        "KEY_UP",            "Up",        "Up"],
    ["KEY_DOWN",      "KEY_DOWN",          "Down",      "Down"],
    ["KEY_LEFT",      "KEY_LEFT",          "Left",      "Left"],
    ["KEY_RIGHT",     "KEY_RIGHT",         "Right",     "Right"],
    ["KEY_PPAGE",     "KEY_CHUP",          "Page Up",   "P Up"],
    ["KEY_NPAGE",     "KEY_CHDOWN",        "Page Down", "P Down"],
    ["\n",            "KEY_ENTER",         "Enter",     "Enter"],
    ["KEY_BACKSPACE", "KEY_RETURN",        "Backspace", "Return"],
    ["e",             "KEY_EXIT",          "E",         "Exit"],
    ["h",             "KEY_CONTENTS",      "H",         "Smart Hub"],
    ["l",             "KEY_CH_LIST",       "L",         "Channel List"],
    ["m",             "KEY_MENU",          "M",         "Menu"],
    ["s",             "KEY_SOURCE",        "S",         "Source"],
    ["g",             "KEY_GUIDE",         "G",         "Guide"],
    ["t",             "KEY_TOOLS",         "T",         "Tools"],
    ["i",             "KEY_INFO",          "I",         "Info"],
    ["z",             "KEY_RED",           "Z",         "A / Red"],
    ["x",             "KEY_GREEN",         "X",         "B / Green"],
    ["c",             "KEY_YELLOW",        "C",         "C / Yellow"],
    ["v",             "KEY_BLUE",          "V",         "D / Blue"],
    ["d",             "KEY_PANNEL_CHDOWN", "D",         "3D"],
    ["+",             "KEY_VOLUP",         "+",         "Volume Up"],
    ["-",             "KEY_VOLDOWN",       "-",         "Volume Down"],
    ["*",             "KEY_MUTE",          "*",         "Mute"],
    ["0",             "KEY_0",             "0",         "0"],
    ["1",             "KEY_1",             "1",         "1"],
    ["2",             "KEY_2",             "2",         "2"],
    ["3",             "KEY_3",             "3",         "3"],
    ["4",             "KEY_4",             "4",         "4"],
    ["5",             "KEY_5",             "5",         "5"],
    ["6",             "KEY_6",             "6",         "6"],
    ["7",             "KEY_7",             "7",         "7"],
    ["8",             "KEY_8",             "8",         "8"],
    ["9",             "KEY_9",             "9",         "9"],
    ["KEY_F(1)",      "KEY_DTV",           "F1",        "TV Source"],
    ["KEY_F(2)",      "KEY_HDMI",          "F2",        "HDMI Source"],
]


def run(remote):
    """Run interactive remote control application."""
    curses.wrapper(_control, remote)


def _control(stdscr, remote):
    height, width = stdscr.getmaxyx()

    stdscr.addstr("Interactive mode, press 'Q' to exit.\n")
    stdscr.addstr("Key mappings:\n")

    column_len = max(len(mapping[2]) for mapping in _mappings) + 1
    mappings_dict = {}
    for mapping in _mappings:
        mappings_dict[mapping[0]] = mapping[1]

        row = stdscr.getyx()[0] + 2
        if row < height:
            line = "  {}= {} ({})\n".format(mapping[2].ljust(column_len),
                                            mapping[3], mapping[1])
            stdscr.addstr(line)
        elif row == height:
            stdscr.addstr("[Terminal is too small to show all keys]\n")

    running = True
    while running:
        key = stdscr.getkey()

        if key == "q":
            running = False

        if key in mappings_dict:
            remote.control(mappings_dict[key])

            try:
                stdscr.addstr(".")
            except curses.error:
                stdscr.deleteln()
                stdscr.move(stdscr.getyx()[0], 0)
                stdscr.addstr(".")
