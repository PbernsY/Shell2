import sys
import os
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


def launch(args):
	# time to execute your input
	# use os.fork to get the process ID
	pid = os.fork()

	# if pid > 0 -> Parent process control
	# else -> Child process control
	if pid > 0:
		wpid = os.waitpid(pid, 0)
	else:
		# try to execeute in the form (command, command_args)
		# generate exception if command does not exist
		try:
			os.execvp(args[0], args)
		except Exception as e:
			print("myshell: command not found: " + args)



def checkwrite(output_list):
	return "a" if ">>" in output_list else "w"

def runner(string):
	set_flags(string)
	shellins.stdout_param = sys.__stdout__
	exece = parseable[0]
	args = " ".join(parseable[1:])
	if exece not in shellins.commands:
		launch(parseable)
	
	elif len(flags) == 2:
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
			try:
				shellins.commands[exece](args)
			except:
				shellins.commands[exece](parseable[1], parseable[2])
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
		runner(input("[" + shellins.path + "]" + " $ "))

else:
	with open(shellins.stdin_param, "r") as reader:
		for line in reader:
			runner(line)
