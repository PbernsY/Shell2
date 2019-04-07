import sys
import shlex
import myshell
from invoker import start

# Flags are as follows, [background_exec, output]


def set_flags(string):
	global flags
	global output
	global parseable
	flags = []
	output = []
	parseable = shlex.split(string)
	if parseable[-1] == "&":
		flags.append(parseable.pop())

	if ">>" in string or ">" in string:
		flags.append(parseable.pop())
		output.append(parseable.pop())

	return flags, parseable, output




def checkwrite(output_list):
	return "a" if ">>" in output_list else "w"

def runner(string):
	set_flags(string)
	shellins.stdout_param = sys.__stdout__
	exece = parseable[0]
	args = " ".join(parseable[1:])

	#if len(flags) > 1:
	#	command = parseable[0]
	#	args = " ".join(parseable[1:])

	if len(flags) == 2:
		with open(flags[-1], checkwrite(output)) as current_file:
			shellins.stdout_param = current_file
			shellins.commands["sp"](shellins.commands[exece], args)

	elif len(flags) == 1:
		if not len(output):
			if len(args):
				shellins.commands["sp"](shellins.commands[exece], args)
			else:
				shellins.commands["sp"](shellins.commands[exece])
				"this bit calls the spawn"  "this bit is the command"       "this bit is the arg"
		else:
			with open(flags[0], checkwrite(output)) as current_file:
				shellins.stdout_param = current_file
				shellins.commands[exece](args)

	else:
		exece = parseable[0]
		args = " ".join(parseable[1:])
		if len(args):
			shellins.commands[exece](args)
		else:
			shellins.commands[exece]()








#	if len(flags) == 1 and "&" not in flags:
#
#		command = parseable[0]
#		args = " ".join(parseable[1:])
#		return shellins.commands[command](args)

#	else:
#		command = string
#		return shellins.commands[command]

#print(set_flags("dir >> hello.txt"))

shellins = start()
if shellins.stdin_param is None:
	while True:
		runner(input())

else:
	with open(shellins.stdin_param, "r") as reader:
		for line in reader:
			runner(line)
