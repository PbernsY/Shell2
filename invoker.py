import sys
import myshell


def start():
    commands = sys.argv[1:]
    if len(commands):
        return myshell.Shellins(commands[0])
    else:
        return myshell.Shellins()
