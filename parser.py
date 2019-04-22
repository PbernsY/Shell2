import sys
import os
import shlex
import myshell
from invoker import start
import subprocess

# Flags are as follows, [background_exec, output]


def set_flags(string):
	''' This is a function to set a list of flags. These flags are then used to perform tasks
	like background execution etc '''
	global flags
	global output
	global parseable
	# set up global variables so they can be passed to the other relevant parsing functions
	flags = []
	output = []
	parseable = shlex.split(string)
	if not len(string):
		return
		# this prevent us trying to index an empty string
	if parseable[-1] == "&":
		# we know, if the ampersand is present, it can only be the last character of the input string
		# if thats the case, append the ampersand to the flags list
		flags.append(parseable.pop())

	if ">>" in string or ">" in string:
		# append the redirection file name to the flags list

		flags.append(parseable.pop())
		# append the redirection symbol to the output list
		output.append(parseable.pop())

	return flags, parseable, output



def sys_binary(list):
	pid = os.fork()
	if pid > 0:
		wpid = os.waitpid(pid, 0)

	else:
		try:
			os.execvp(parseable[0], parseable)
		except:
			print("myshell: command not found " + parseable[0])
			sys.exit()

	
	


def bothflags(exece, args):
	''' this function is called when both flags are set [background_exec, outputfilename]'''
	with open(flags[-1], checkwrite(output)) as current_file:
		# open the file name with file mode depending on the checkwrite function
		shellins.stdout_param = current_file
		# modify the stdout of our shell based on file we opened
		# spawn a process for our shell to exec 
		shellins.spawn_subprocess(shellins.commands[exece], args)

def oneflag(exece, args):
	''' this function is called when one flag is set in our flags list'''
	current_command = shellins.commands[exece]
	
	if len(output) == 0:
		# if the length of the output list is 0, we just have to background exec
		if len(args):
			# this makes sure we dont try to pass a command that takes positional arguments 0 arguments
			shellins.spawn_subprocess(current_command, args)
		else:
			# do the opposite, call a single arrity command with no args
			shellins.spawn_subprocess(current_command)
			#"this bit calls the spawn"  "this bit is the command"       "this bit is the arg"
	else:
		# we have a redirection symbol but no ampersand
		if len(args):
			with open(flags[-1], checkwrite(output)) as current_file:
				# open the file in the appropriate mode
				shellins.stdout_param = current_file
				# execute the current command with args
				current_command(args)
		else:
			with open(flags[-1], checkwrite(output)) as current_file:
				# open the file in the appropriate mode
				shellins.stdout_param = current_file
				# execute the current command with args
				shellins.commands[exece]()


		
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
				sys_binary(parseable)
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
	

	








shellins = start()
if shellins.stdin_param is None:
	while True:
		runner(input("[" + shellins.path + "]" + " $ "))

	

else:
	with open(shellins.stdin_param, "r") as reader:
		for line in reader:
			runner(line)
