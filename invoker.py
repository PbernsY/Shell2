import sys
def invoker():
	commands = sys.argv[1:]
	if len(commands):
		shellins = Shell(commands[0])
	else:
		shellins = Shell()
