import sys
import os
import shlex
import myshell
from invoker import start
import subprocess

# Flags are as follows, [background_exec, output]


def set_flags(string):
	global flags
	global output
	global parseable
	flags = []
	output = []
	parseable = shlex.split(string)
	if not len(string):
		return
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
			print("myshell: command not found: " + args[0])



def bothflags(exece, args):
	with open(flags[-1], checkwrite(output)) as current_file:
		shellins.stdout_param = current_file
		shellins.spawn_subprocess(shellins.commands[exece], args)

def oneflag(exece, args):
	current_command = shellins.commands[exece]
	if not len(output):
		if len(args):
			shellins.spawn_subprocess(current_command, args)
		else:
			shellins.spawn_subprocess(current_command)
			"this bit calls the spawn"  "this bit is the command"       "this bit is the arg"
	else:
		with open(flags[0], checkwrite(output)) as current_file:
			shellins.__stdout__param = current_file
			current_command(args)

		
def checkwrite(output_list):
	return "a" if ">>" in output_list else "w"

def runner(string):
	if len(string) is 0:
		return
	set_flags(string)
	shellins.stdout_param = sys.__stdout__
	exece = parseable[0]
	args = " ".join(parseable[1:])

	try:
		if exece not in shellins.commands :
			try:
				subprocess.run(exece)
			except FileNotFoundError:
				print("myshell: command not found " + string)
			return
		if len(flags) == 2:
			bothflags(exece, args)

		elif len(flags) == 1:
			oneflag(exece, args)
		else:
			exece = parseable[0]
			args = " ".join(parseable[1:])
			if len(args):
				try:
					shellins.commands[exece](args)
				except TypeError:
					shellins.commands[exece](parseable[1], parseable[2])
			else:
				shellins.commands[exece]()
	except KeyError:
		print("command not found " + string)
	except TypeError:
		print("Incorrect amount of args supplied to " + exece)

	








shellins = start()
if shellins.stdin_param is None:
	while True:
		runner(input("[" + shellins.path + "]" + " $ "))

	

else:
	with open(shellins.stdin_param, "r") as reader:
		for line in reader:
			runner(line)
